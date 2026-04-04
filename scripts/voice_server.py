# /// script
# dependencies = [
#   "mcp[cli]",
#   "kokoro[en]",
#   "faster-whisper",
#   "sounddevice",
#   "numpy",
# ]
# ///
"""
career-voice — local MCP server for TTS and STT.

Tools:
  speak(text)                     — Kokoro TTS → sounddevice playback
  listen(duration_seconds=15)     — sounddevice record → faster-whisper STT

Run via Claude Desktop MCP (stdio transport). Models are lazy-loaded on first use.
"""

import numpy as np
import sounddevice as sd
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("career-voice")

_tts_pipeline = None
_stt_model = None

SAMPLE_RATE_TTS = 24000   # Kokoro native output rate
SAMPLE_RATE_STT = 16000   # faster-whisper / Whisper expected rate


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
def listen(duration_seconds: int = 15) -> str:
    """
    Record audio from the microphone and return a transcript.

    Args:
        duration_seconds: How long to record (default 15 s). Extend for longer answers.

    Returns the transcribed text, or "(no speech detected)" if nothing was recognized.
    """
    recording = sd.rec(
        int(duration_seconds * SAMPLE_RATE_STT),
        samplerate=SAMPLE_RATE_STT,
        channels=1,
        dtype="float32",
    )
    sd.wait()

    audio = recording.flatten()
    model = _get_stt()
    segments, _ = model.transcribe(audio, beam_size=5, language="en")
    transcript = " ".join(seg.text for seg in segments).strip()
    return transcript or "(no speech detected)"


if __name__ == "__main__":
    mcp.run()  # stdio transport — Claude Desktop connects via .mcp.json
