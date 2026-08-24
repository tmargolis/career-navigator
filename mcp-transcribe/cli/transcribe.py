#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = ["mlx-whisper; sys_platform == 'darwin' and platform_machine == 'arm64'", "faster-whisper"]
# ///
"""
transcribe.py — standalone CLI. Same engine as the MCP server, no daemon.

This exists so transcription never depends on an MCP server starting. If the
server is broken, misconfigured, or Claude Desktop is closed, this still works.

Usage:
    uv run cli/transcribe.py /path/to/recording.mp3
    uv run cli/transcribe.py rec.mp3 --prompt "AcmeCorp, Widgetron, J. Doe"
    uv run cli/transcribe.py rec.mp3 --vocab-group example-employer
    uv run cli/transcribe.py rec.mp3 --model medium.en --out ~/Desktop

Writes <name>.transcript.txt and <name>.segments.json next to the audio.

Proper nouns can also live in vocabulary.local.json (gitignored) instead of
being typed on the command line — see vocabulary.example.json.
"""
import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path

MLX_DEFAULT_MODEL = "mlx-community/whisper-large-v3-turbo"
FW_DEFAULT_MODEL = "medium.en"
VOCAB_PATH = Path(__file__).resolve().parent.parent / "vocabulary.local.json"


def load_vocabulary(group=""):
    """Proper nouns from the gitignored vocabulary.local.json. Never raises."""
    if not VOCAB_PATH.exists():
        return []
    try:
        data = json.loads(VOCAB_PATH.read_text(encoding="utf-8"))
    except Exception:
        return []
    terms = [t for t in data.get("always", []) if isinstance(t, str)]
    if group:
        terms += [t for t in data.get("groups", {}).get(group, []) if isinstance(t, str)]
    seen, out = set(), []
    for t in terms:
        k = t.strip()
        if k and k.lower() not in seen:
            seen.add(k.lower()); out.append(k)
    return out


def duration_of(path: Path):
    if not shutil.which("ffprobe"):
        return None
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
            capture_output=True, text=True, timeout=30)
        return round(float(out.stdout.strip()), 2)
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser(description="Transcribe an audio file with Whisper.")
    ap.add_argument("audio", help="Path to the audio file")
    ap.add_argument("--prompt", default="",
                    help="Proper nouns likely to appear (names, companies, products). "
                         "Strongly recommended — Whisper mangles unusual names without it.")
    ap.add_argument("--vocab-group", default="",
                    help="Key into the 'groups' map of vocabulary.local.json (gitignored)")
    ap.add_argument("--language", default="en")
    ap.add_argument("--model", default="", help="Override the backend default model")
    ap.add_argument("--out", default="", help="Output directory (default: alongside the audio)")
    args = ap.parse_args()

    src = Path(args.audio).expanduser().resolve()
    if not src.is_file():
        sys.exit(f"error: not a file: {src}")
    if not shutil.which("ffmpeg"):
        sys.exit("error: ffmpeg not found. Install with: brew install ffmpeg")

    use_mlx = platform.system() == "Darwin" and platform.machine() == "arm64"
    try:
        if use_mlx:
            import mlx_whisper  # noqa
    except Exception:
        use_mlx = False

    vocab = load_vocabulary(args.vocab_group)
    prompt = ". ".join(x for x in (args.prompt.strip(), ", ".join(vocab)) if x)

    dur = duration_of(src)
    backend = "mlx-whisper" if use_mlx else "faster-whisper"
    model = args.model or (MLX_DEFAULT_MODEL if use_mlx else FW_DEFAULT_MODEL)
    print(f"backend : {backend}")
    print(f"model   : {model}")
    print(f"vocab   : {len(vocab)} local term(s)")  # count only — terms stay private
    print(f"audio   : {src.name}" + (f"  ({dur/60:.1f} min)" if dur else ""))
    print("transcribing...", flush=True)

    t0 = time.time()
    segments = []
    if use_mlx:
        import mlx_whisper
        r = mlx_whisper.transcribe(
            str(src), path_or_hf_repo=model,
            language=args.language or None,
            initial_prompt=prompt or None,
            condition_on_previous_text=True, verbose=None)
        text = (r.get("text") or "").strip()
        segments = [{"start": round(float(s["start"]), 2),
                     "end": round(float(s["end"]), 2),
                     "text": (s.get("text") or "").strip()}
                    for s in r.get("segments", [])]
    else:
        from faster_whisper import WhisperModel
        m = WhisperModel(model, device="cpu", compute_type="int8",
                         cpu_threads=max(1, os.cpu_count() or 2))
        seg_iter, _ = m.transcribe(
            str(src), beam_size=5,
            language=args.language or None,
            initial_prompt=prompt or None,
            condition_on_previous_text=True,
            vad_filter=False)   # deliberate: VAD drops speech at silence edges
        for s in seg_iter:
            segments.append({"start": round(s.start, 2), "end": round(s.end, 2),
                             "text": s.text.strip()})
            print(f"  {s.end:6.0f}s", end="\r", flush=True)
        text = " ".join(s["text"] for s in segments).strip()

    elapsed = time.time() - t0
    dest = Path(args.out).expanduser() if args.out else src.parent
    dest.mkdir(parents=True, exist_ok=True)
    txt = dest / f"{src.stem}.transcript.txt"
    js = dest / f"{src.stem}.segments.json"
    txt.write_text(text, encoding="utf-8")
    js.write_text(json.dumps(segments, indent=1, ensure_ascii=False), encoding="utf-8")

    speed = f"{dur/elapsed:.1f}x realtime" if dur else "n/a"
    print(f"\ndone    : {len(segments)} segments in {elapsed:.0f}s ({speed})")
    print(f"text    : {txt}")
    print(f"segments: {js}")


if __name__ == "__main__":
    main()
