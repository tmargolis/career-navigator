#!/usr/bin/env python3
"""
Register mcp-transcribe with Claude Desktop.

Run once from Terminal:
    python3 <repo>/mcp-transcribe/install_transcribe_mcp.py

Unlike the old setup_career_voice.py, this verifies every prerequisite BEFORE
touching your config, and tells you exactly what is missing if something is.
"""
import json
import platform
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
SERVER = SCRIPT_DIR / "server" / "main.py"
CONFIG = Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"

fail = []

# 1. uv
uv = shutil.which("uv")
if not uv:
    for c in ["/opt/homebrew/bin/uv", "/usr/local/bin/uv", str(Path.home() / ".local/bin/uv")]:
        if Path(c).exists():
            uv = c
            break
print(f"{'OK  ' if uv else 'FAIL'}  uv: {uv or 'not found — brew install uv'}")
if not uv:
    fail.append("uv")

# 2. server file
print(f"{'OK  ' if SERVER.exists() else 'FAIL'}  server: {SERVER}")
if not SERVER.exists():
    fail.append("server/main.py")

# 3. ffmpeg (whisper decodes through it)
ff = shutil.which("ffmpeg")
print(f"{'OK  ' if ff else 'FAIL'}  ffmpeg: {ff or 'not found — brew install ffmpeg'}")
if not ff:
    fail.append("ffmpeg")

# 4. config dir
print(f"{'OK  ' if CONFIG.parent.exists() else 'FAIL'}  Claude Desktop config dir: {CONFIG.parent}")
if not CONFIG.parent.exists():
    fail.append("Claude Desktop config directory (is Claude Desktop installed?)")

if fail:
    print("\nMissing: " + ", ".join(fail))
    print("Fix those, then re-run. Nothing was changed.")
    sys.exit(1)

# 4b. Seed the gitignored local vocabulary file from the committed example.
VOCAB = SCRIPT_DIR / "vocabulary.local.json"
EXAMPLE = SCRIPT_DIR / "vocabulary.example.json"
if not VOCAB.exists() and EXAMPLE.exists():
    shutil.copy(EXAMPLE, VOCAB)
    print(f"OK    Created {VOCAB.name} (gitignored) — add your real proper nouns there")
elif VOCAB.exists():
    print(f"OK    {VOCAB.name} already present")

# 5. Apple Silicon acceleration — optional but a large speedup
if platform.system() == "Darwin" and platform.machine() == "arm64":
    print("\nApple Silicon detected. Installing mlx-whisper for Metal acceleration...")
    r = subprocess.run([uv, "sync", "--extra", "mlx"], cwd=SCRIPT_DIR)
    if r.returncode != 0:
        print("WARN  mlx-whisper install failed. The server will still work on CPU "
              "via faster-whisper, just slower.")
else:
    subprocess.run([uv, "sync"], cwd=SCRIPT_DIR)

# 6. Smoke test — start the server's imports before wiring it into the config,
#    so a broken environment surfaces here rather than as a silent Claude Desktop failure.
print("\nSmoke test: loading server module...")
probe = subprocess.run(
    [uv, "run", "--project", str(SCRIPT_DIR), "python", "-c",
     "import importlib.util,sys;"
     f"spec=importlib.util.spec_from_file_location('m',r'{SERVER}');"
     "m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);"
     "print(m.backend_info())"],
    capture_output=True, text=True, cwd=SCRIPT_DIR)
print(probe.stdout.strip() or probe.stderr.strip()[-1500:])
if probe.returncode != 0:
    print("\nFAIL  Server did not import cleanly. Not modifying your config.")
    sys.exit(1)

# 7. Write config
config = json.loads(CONFIG.read_text()) if CONFIG.exists() else {}
config.setdefault("mcpServers", {})
config["mcpServers"]["mcp-transcribe"] = {
    "type": "stdio",
    "command": uv,
    "args": ["run", "--project", str(SCRIPT_DIR), str(SERVER)],
}

if CONFIG.exists():
    backup = CONFIG.with_suffix(".json.transcribe_backup")
    shutil.copy(CONFIG, backup)
    print(f"\nOK    Backup: {backup}")

CONFIG.write_text(json.dumps(config, indent=2))
print(f"OK    Registered 'mcp-transcribe' in {CONFIG.name}")
print("\nRestart Claude Desktop. Then ask Claude to run backend_info to confirm it loaded.")
