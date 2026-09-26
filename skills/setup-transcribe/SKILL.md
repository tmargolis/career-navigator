---
name: setup-transcribe
description: >
  Installs and registers the local mcp-transcribe MCP server with Claude
  Desktop so /career-navigator:interview-capture can transcribe recorded
  interview audio files. Runs the prerequisite checks and installer commands
  on the user's behalf so they don't need to use a terminal themselves.
  Also invocable via /career-navigator:setup-transcribe.
triggers:
  - "set up interview transcription"
  - "install mcp-transcribe"
  - "enable interview capture"
  - "set up audio transcription"
  - "set up mcp-transcribe"
  - "/career-navigator:setup-transcribe"
  - "/setup-transcribe"
---

Install the local `mcp-transcribe` MCP server so `/career-navigator:interview-capture` can transcribe recorded interview audio files. This walks a non-technical user through the same steps `mcp-transcribe/README.md` documents for the command line — but Claude runs them, with confirmation before anything is installed or changed.

This is optional. Skip it entirely if the user doesn't plan to use `interview-capture`.

---

## 1. Check whether it's already installed

Check whether a tool named `backend_info` (from `mcp-transcribe`) is already available in this session. If it is, call it, report the active backend, and stop — nothing to install.

If not, continue.

---

## 2. Locate the plugin directory

Resolve the absolute path to this plugin's `mcp-transcribe/` directory (the same repo `skills/setup-transcribe/SKILL.md` lives in). If it can't be found (e.g. the plugin was installed as a zip without this optional directory), tell the user:

> Interview transcription setup isn't available from this install — it needs the `mcp-transcribe/` folder from the Career Navigator GitHub repo. Clone or download the repo from https://github.com/tmargolis/career-navigator and re-run this from inside it.

Then stop.

---

## 3. Check prerequisites

Run via Bash (read-only checks, no confirmation needed):

```bash
command -v uv; command -v ffmpeg; command -v brew
```

Report which are present. Two cases:

**Homebrew missing (uv and/or ffmpeg also missing):** This flow only automates the Homebrew path (macOS/Linuxbrew). Tell the user to install `uv` and `ffmpeg` themselves (point to https://docs.astral.sh/uv/getting-started/installation/ and https://ffmpeg.org/download.html), then re-run this skill. Stop.

**Homebrew present, uv and/or ffmpeg missing:** Tell the user exactly what will run and why, then ask for explicit confirmation before running it:

> This needs `uv` and `ffmpeg` installed via Homebrew. I'll run: `brew install uv ffmpeg`. OK to proceed?

Only after a clear yes, run it via Bash. If it fails, show the error and stop — do not retry silently.

---

## 4. Run the installer

Explain what's about to happen before running it:

> This runs the plugin's installer, which checks your setup, installs `mcp-transcribe`'s Python dependencies into its own isolated environment, and registers it in Claude Desktop's config (`~/Library/Application Support/Claude/claude_desktop_config.json`). It backs up that config file first and won't touch it if anything fails a check.

Then run:

```bash
python3 {resolved_path}/mcp-transcribe/install_transcribe_mcp.py
```

Relay its output verbatim — it already prints clear OK/FAIL lines per prerequisite and stops cleanly (without touching the config) if anything is wrong. If it fails, do not attempt to fix the underlying issue yourself (e.g. don't `pip install` things by hand around it) — report exactly what it printed and let the user decide how to proceed, since the script is deliberately conservative about not writing a broken config.

---

## 5. Confirm and hand off

On success:

```
✅ mcp-transcribe installed and registered.

Restart Claude Desktop (or start a new chat) so the tool loads, then run
/career-navigator:interview-capture with the path to a recorded interview
audio file.
```

Do not attempt to call `backend_info` in this same session — the config change only takes effect in a new session.

---

## Guardrails

- Never run `brew install` or the Python installer without first telling the user what it does and getting an explicit yes — this modifies the user's local Homebrew packages and Claude Desktop config.
- Never hand-edit `claude_desktop_config.json` directly — always go through `install_transcribe_mcp.py`, which validates and backs up before writing.
- Never paste, log, or echo the contents of `vocabulary.local.json` — the installer seeds it from `vocabulary.example.json` on first run; its real values are the user's private data.
- This flow is macOS/Homebrew-specific (`install_transcribe_mcp.py` targets Claude Desktop's macOS config path). On Windows/Linux, or if Claude Desktop isn't installed, stop after Step 3 and point the user to `mcp-transcribe/README.md`'s manual install steps instead.
