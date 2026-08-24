"""
mcp-transcribe — local MCP server for batch transcription of audio files.

One job, done reliably: take an audio file that already exists on disk and
return a transcript. No microphone, no speakers, no streaming, no VAD.
Those are the parts that make voice MCP servers fail to start; none of them
are needed to transcribe a recorded interview.

Tools:
  transcribe_file(path, ...)  — audio file -> transcript text + segments on disk
  backend_info()              — which STT backend is active, for diagnosis

Backends, auto-selected:
  1. mlx-whisper      (Apple Silicon, Metal-accelerated — by far the fastest)
  2. faster-whisper   (CPU, cross-platform fallback)

Run via Claude Desktop MCP (stdio transport). Models lazy-load on first use.
"""

import json
import os
import platform
import shutil
import subprocess
import time
from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mcp-transcribe")

# Apple Silicon default. large-v3-turbo is near-large accuracy at a fraction
# of the cost, and on an M-series chip runs many times faster than realtime.
MLX_DEFAULT_MODEL = "mlx-community/whisper-large-v3-turbo"
# CPU fallback default. medium.en is the accuracy floor that avoids the
# proper-noun and hedge-word errors small.en makes on interview audio.
FW_DEFAULT_MODEL = "medium.en"

AUDIO_SUFFIXES = {
    ".mp3", ".m4a", ".mp4", ".wav", ".flac", ".ogg", ".opus",
    ".aac", ".webm", ".mov", ".aiff", ".aif", ".wma",
}

_backend = None          # "mlx" | "faster-whisper"
_fw_model_cache = {}


# ── backend selection ────────────────────────────────────────────────────────

def _detect_backend() -> str:
    global _backend
    if _backend:
        return _backend
    if platform.system() == "Darwin" and platform.machine() == "arm64":
        try:
            import mlx_whisper  # noqa: F401
            _backend = "mlx"
            return _backend
        except Exception:
            pass
    import faster_whisper  # noqa: F401  (raises if genuinely unavailable)
    _backend = "faster-whisper"
    return _backend


def _probe_duration(path: Path):
    """Best-effort media duration in seconds. None if ffprobe is unavailable."""
    if not shutil.which("ffprobe"):
        return None
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
            capture_output=True, text=True, timeout=30,
        )
        return round(float(out.stdout.strip()), 2)
    except Exception:
        return None


# ── local vocabulary (gitignored, never committed) ───────────────────────────

VOCAB_PATH = Path(__file__).resolve().parent.parent / "vocabulary.local.json"


def load_vocabulary(group: str = ""):
    """
    Read proper nouns from vocabulary.local.json, which is gitignored so that
    employer, project, and people names stay out of the public repository.

    Shape:
        {"always": ["TermA", "TermB"],
         "groups": {"some-key": ["TermC", "TermD"]}}

    Returns (terms, note). Never raises — a missing or malformed file simply
    means no extra vocabulary.
    """
    if not VOCAB_PATH.exists():
        return [], "no vocabulary.local.json"
    try:
        data = json.loads(VOCAB_PATH.read_text(encoding="utf-8"))
    except Exception as e:
        return [], f"vocabulary.local.json unreadable ({type(e).__name__})"

    terms = [t for t in data.get("always", []) if isinstance(t, str)]
    if group:
        terms += [t for t in data.get("groups", {}).get(group, []) if isinstance(t, str)]

    seen, ordered = set(), []
    for t in terms:
        k = t.strip()
        if k and k.lower() not in seen:
            seen.add(k.lower())
            ordered.append(k)
    return ordered, f"{len(ordered)} term(s) loaded"


# ── tools ────────────────────────────────────────────────────────────────────

@mcp.tool()
def backend_info() -> str:
    """
    Report which transcription backend is active and whether ffmpeg is present.
    Call this first when transcription is misbehaving — it distinguishes
    "server is fine, file is bad" from "backend never loaded".
    """
    info = {
        "platform": f"{platform.system()}/{platform.machine()}",
        "ffmpeg": bool(shutil.which("ffmpeg")),
        "ffprobe": bool(shutil.which("ffprobe")),
    }
    _terms, vocab_note = load_vocabulary()
    info["vocabulary"] = vocab_note   # count only — terms are private, never echoed
    try:
        info["backend"] = _detect_backend()
        info["default_model"] = (
            MLX_DEFAULT_MODEL if info["backend"] == "mlx" else FW_DEFAULT_MODEL
        )
        info["ok"] = True
    except Exception as e:
        info["backend"] = None
        info["ok"] = False
        info["error"] = f"{type(e).__name__}: {e}"
    return json.dumps(info, indent=2)


@mcp.tool()
def transcribe_file(
    path: str,
    initial_prompt: str = "",
    vocabulary_group: str = "",
    language: str = "en",
    model: str = "",
    out_dir: str = "",
    write_files: bool = True,
) -> str:
    """
    Transcribe an audio file that already exists on disk.

    Args:
      path:           Absolute path to the audio file.
      initial_prompt: Proper nouns and jargon likely to appear — company names,
                      interviewer names, product names. Whisper mangles unusual
                      names badly without this — on real recordings it has turned
                      a four-letter vendor name into a common English word and a
                      surname into a different surname entirely. Seeding it is the
                      single cheapest accuracy win. Terms from vocabulary.local.json
                      (gitignored) are merged in automatically; see load_vocabulary.
      vocabulary_group: Optional key into the "groups" map of
                      vocabulary.local.json, for terms specific to one employer
                      or project. "always" terms are included regardless.
      language:       ISO language code. Default "en".
      model:          Override the backend default. Leave blank for the default.
      out_dir:        Where to write outputs. Defaults to the audio file's folder.
      write_files:    Write <name>.transcript.txt and <name>.segments.json.

    Returns JSON: backend, model, duration, elapsed, speed, segment count,
    output paths, and the full transcript text.

    Notes:
      - Runs synchronously. On Apple Silicon expect many times faster than
        realtime; a ~25 minute interview is typically well under a minute.
      - No voice-activity filtering is applied. VAD silently drops speech near
        silence boundaries, which has cost real content before. Whole file only.
    """
    src = Path(path).expanduser()
    if not src.exists():
        return json.dumps({"ok": False, "error": f"File not found: {src}"})
    if not src.is_file():
        return json.dumps({"ok": False, "error": f"Not a file: {src}"})
    if src.suffix.lower() not in AUDIO_SUFFIXES:
        return json.dumps({
            "ok": False,
            "error": f"Unrecognized audio extension '{src.suffix}'. "
                     f"Supported: {sorted(AUDIO_SUFFIXES)}",
        })
    if not shutil.which("ffmpeg"):
        return json.dumps({
            "ok": False,
            "error": "ffmpeg not found on PATH. Install with: brew install ffmpeg",
        })

    try:
        backend = _detect_backend()
    except Exception as e:
        return json.dumps({
            "ok": False,
            "error": f"No transcription backend available ({type(e).__name__}: {e}). "
                     f"On Apple Silicon: uv add mlx-whisper. Elsewhere: uv add faster-whisper.",
        })

    # Merge caller-supplied names with the gitignored local vocabulary.
    vocab_terms, vocab_note = load_vocabulary(vocabulary_group)
    prompt_parts = [p for p in (initial_prompt.strip(), ", ".join(vocab_terms)) if p]
    effective_prompt = ". ".join(prompt_parts)

    duration = _probe_duration(src)
    t0 = time.time()
    segments = []

    try:
        if backend == "mlx":
            import mlx_whisper
            repo = model or MLX_DEFAULT_MODEL
            result = mlx_whisper.transcribe(
                str(src),
                path_or_hf_repo=repo,
                language=language or None,
                initial_prompt=effective_prompt or None,
                condition_on_previous_text=True,
                verbose=None,
            )
            text = (result.get("text") or "").strip()
            for s in result.get("segments", []):
                segments.append({
                    "start": round(float(s["start"]), 2),
                    "end": round(float(s["end"]), 2),
                    "text": (s.get("text") or "").strip(),
                })
        else:
            from faster_whisper import WhisperModel
            name = model or FW_DEFAULT_MODEL
            if name not in _fw_model_cache:
                _fw_model_cache[name] = WhisperModel(
                    name, device="cpu", compute_type="int8",
                    cpu_threads=max(1, (os.cpu_count() or 2)),
                )
            seg_iter, _info = _fw_model_cache[name].transcribe(
                str(src),
                beam_size=5,
                language=language or None,
                initial_prompt=effective_prompt or None,
                condition_on_previous_text=True,
                vad_filter=False,   # deliberate: see docstring
            )
            for s in seg_iter:
                segments.append({
                    "start": round(s.start, 2),
                    "end": round(s.end, 2),
                    "text": s.text.strip(),
                })
            text = " ".join(s["text"] for s in segments).strip()
    except Exception as e:
        return json.dumps({
            "ok": False,
            "backend": backend,
            "error": f"Transcription failed: {type(e).__name__}: {e}",
        })

    elapsed = round(time.time() - t0, 1)
    model_used = model or (MLX_DEFAULT_MODEL if backend == "mlx" else FW_DEFAULT_MODEL)

    payload = {
        "ok": True,
        "backend": backend,
        "model": model_used,
        "source": str(src),
        "duration_seconds": duration,
        "elapsed_seconds": elapsed,
        "speed_x_realtime": round(duration / elapsed, 1) if duration and elapsed else None,
        "segment_count": len(segments),
        "vocabulary": vocab_note,   # count only — terms are private, never echoed
        "text": text,
    }

    if write_files:
        dest = Path(out_dir).expanduser() if out_dir else src.parent
        try:
            dest.mkdir(parents=True, exist_ok=True)
            txt_path = dest / f"{src.stem}.transcript.txt"
            json_path = dest / f"{src.stem}.segments.json"
            txt_path.write_text(text, encoding="utf-8")
            json_path.write_text(
                json.dumps(segments, indent=1, ensure_ascii=False), encoding="utf-8"
            )
            payload["transcript_path"] = str(txt_path)
            payload["segments_path"] = str(json_path)
        except Exception as e:
            payload["write_warning"] = f"{type(e).__name__}: {e}"

    return json.dumps(payload, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    mcp.run()
