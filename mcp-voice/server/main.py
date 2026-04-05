# /// script
# dependencies = [
#   "mcp[cli]",
#   "kokoro",
#   "faster-whisper",
#   "sounddevice",
#   "numpy",
#   "webrtcvad",
# ]
# ///
"""
mcp-voice — local MCP server for TTS and STT.

Tools:
  speak(text)                     — Kokoro TTS → sounddevice playback
  listen(...)                     — sounddevice stream + webrtcvad end-of-utterance → faster-whisper STT

Run via Claude Desktop MCP (stdio transport). Models are lazy-loaded on first use.
"""

import math
import time

import numpy as np
import sounddevice as sd
import webrtcvad
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mcp-voice")

_tts_pipeline = None
_stt_model = None

SAMPLE_RATE_TTS = 24000   # Kokoro native output rate
SAMPLE_RATE_STT = 16000   # faster-whisper / Whisper expected rate; webrtcvad supports this rate

# VAD frame duration (webrtcvad requires 10 / 20 / 30 ms frames at 16 kHz)
_VAD_FRAME_MS = 30
_VAD_FRAME_SAMPLES = int(SAMPLE_RATE_STT * _VAD_FRAME_MS / 1000)  # 480


def _float32_to_pcm16_bytes(mono: np.ndarray) -> bytes:
    pcm = np.clip(mono.astype(np.float64, copy=False), -1.0, 1.0)
    return (pcm * 32767.0).astype(np.int16).tobytes()


def _get_tts():
    global _tts_pipeline
    if _tts_pipeline is None:
        from kokoro import KPipeline
        # lang_code='a' → American English (uses misaki phonemizer, no espeak-ng needed)
        _tts_pipeline = KPipeline(lang_code="a")
    return _tts_pipeline


def _get_stt():
    global _stt_model
    if _stt_model is None:
        from faster_whisper import WhisperModel
        # base.en: English-only, fast, accurate enough for interview contexts
        # int8 quantization keeps RAM usage low on CPU / Apple Silicon
        _stt_model = WhisperModel("base.en", device="cpu", compute_type="int8")
    return _stt_model


@mcp.tool()
def speak(text: str, voice: str = "af_heart", speed: float = 1.0) -> str:
    """
    Convert text to speech and play it through the local speaker.

    Args:
        text:  The text to speak aloud.
        voice: Kokoro voice ID. American English options: af_heart (default),
               af_sarah, af_sky, am_adam, am_michael.
        speed: Playback speed multiplier (0.5–2.0). Default 1.0.

    Returns a confirmation string when playback is complete.
    """
    pipeline = _get_tts()
    for _graphemes, _phonemes, audio in pipeline(text, voice=voice, speed=speed):
        sd.play(audio.numpy(), samplerate=SAMPLE_RATE_TTS)
        sd.wait()
    return "Speech complete."


@mcp.tool()
def listen(
    duration_seconds: int = 60,
    pause_seconds: float = 1.2,
    vad_mode: int = 2,
) -> str:
    """
    Record audio from the microphone and return a transcript.

    Uses webrtcvad on 30 ms frames: after speech starts, consecutive non-speech
    frames lasting ``pause_seconds`` end recording early (end-of-utterance).
    ``duration_seconds`` is a hard cap from the moment capture starts.

    Args:
        duration_seconds: Maximum recording length (default 60 s).
        pause_seconds: Stop after this much trailing silence once speech has begun (default 1.2 s).
        vad_mode: webrtcvad aggressiveness 0–3 (higher filters more non-speech; default 2).

    Returns the transcribed text, or "(no speech detected)" if nothing was recognized.
    """
    if not 0 <= vad_mode <= 3:
        return "Error: vad_mode must be 0–3."
    if pause_seconds <= 0:
        return "Error: pause_seconds must be positive."

    vad = webrtcvad.Vad(vad_mode)
    pause_frames = max(1, math.ceil(pause_seconds / (_VAD_FRAME_MS / 1000.0)))

    deadline = time.monotonic() + float(duration_seconds)
    chunks: list[np.ndarray] = []
    speech_started = False
    silent_run = 0

    with sd.InputStream(
        samplerate=SAMPLE_RATE_STT,
        channels=1,
        dtype="float32",
        blocksize=_VAD_FRAME_SAMPLES,
    ) as stream:
        while time.monotonic() < deadline:
            data, overflowed = stream.read(_VAD_FRAME_SAMPLES)
            if overflowed:
                pass
            chunk = np.asarray(data, dtype=np.float32).reshape(-1)
            if chunk.size < _VAD_FRAME_SAMPLES:
                continue

            pcm = _float32_to_pcm16_bytes(chunk)
            is_speech = vad.is_speech(pcm, SAMPLE_RATE_STT)

            if not speech_started:
                if is_speech:
                    speech_started = True
                    chunks.append(chunk.copy())
                    silent_run = 0
                continue

            chunks.append(chunk.copy())
            if is_speech:
                silent_run = 0
            else:
                silent_run += 1
                if silent_run >= pause_frames:
                    break

    if not chunks:
        return "(no speech detected)"

    audio = np.concatenate(chunks, dtype=np.float32)
    model = _get_stt()
    segments, _ = model.transcribe(audio, beam_size=5, language="en")
    transcript = " ".join(seg.text for seg in segments).strip()
    return transcript or "(no speech detected)"


if __name__ == "__main__":
    mcp.run()  # stdio transport — Claude Desktop connects via .mcp.json
