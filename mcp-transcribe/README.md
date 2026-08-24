# mcp-transcribe

Local MCP server that transcribes **audio files that already exist on disk**.

No microphone. No text-to-speech. No streaming. No voice-activity detection.
That narrowness is the point — see "Why this replaced mcp-voice" below.

## Tools

| Tool | Purpose |
|---|---|
| `transcribe_file(path, initial_prompt, vocabulary_group, language, model, out_dir, write_files)` | Transcribe a recording. Returns text + timed segments; also writes `<name>.transcript.txt` and `<name>.segments.json`. |
| `backend_info()` | Report the active backend and whether ffmpeg is present. Call this first when something is wrong. |

## Backends

Auto-selected at first use:

1. **mlx-whisper** — Apple Silicon, Metal-accelerated. Default model `mlx-community/whisper-large-v3-turbo`. Many times faster than realtime.
2. **faster-whisper** — CPU fallback for Intel Macs, Windows, Linux. Default model `medium.en`.

## Install

```bash
brew install uv ffmpeg          # if you don't have them
python3 install_transcribe_mcp.py
# restart Claude Desktop
```

The installer verifies uv, the server file, ffmpeg, and the Claude Desktop config
directory, installs dependencies, and **smoke-tests the server's imports** before
it writes anything to your config. If any check fails it stops and changes nothing.

## Standalone CLI (no MCP required)

Transcription should never depend on a daemon starting. Same engine, no server:

```bash
uv run cli/transcribe.py ~/path/recording.mp3 --prompt "AcmeCorp, Widgetron, J. Doe"
uv run cli/transcribe.py ~/path/recording.mp3 --vocab-group example-employer
```

## Two settings that matter

**`initial_prompt` is not optional in practice.** Whisper mangles unusual proper
nouns badly — on real recordings it has turned a four-letter vendor name into a
common English word, a surname into a different surname, and a firm name into a
near-homophone. Seeding the prompt with the names you already know will be spoken
fixes most of this for free, and costs nothing.

**VAD is off and stays off.** Voice-activity filtering trims silence, but it
drops speech at silence boundaries. On a 23-minute recruiter screen it silently
removed ~28 seconds — including the interviewer's entire answer about the
interview process, the most actionable content in the call. The time saved is
not worth losing content you will never know was missing.

## Keeping names out of the repository

This repo is public. Employer names, people's names, and project names belong in
**`vocabulary.local.json`**, which is gitignored and never committed. Copy
`vocabulary.example.json` to `vocabulary.local.json` (the installer does this for
you) and fill in your real terms:

```json
{
  "always": ["MyProject", "MyCompany"],
  "groups": {
    "some-employer": ["Their Product", "A. Person", "THEIRACRONYM"]
  }
}
```

`transcribe_file` merges `always` plus any requested `vocabulary_group` into the
Whisper prompt automatically; the CLI takes `--vocab-group`. Neither the tools nor
the logs ever echo the terms back — `backend_info` and the transcription result
report only a **count**, so private names cannot leak into a transcript header,
a tool result, or a commit.

For interview work the richer source is the tracker itself
(`career/CareerNavigator/`), which is already gitignored — the `interview-capture`
skill builds the prompt from the matched application's company, role, and contact
names. Use `vocabulary.local.json` for cross-cutting terms the tracker does not
carry, such as your own project names.

Keep the merged prompt under roughly 200 tokens; Whisper truncates a long one.

## Why this replaced mcp-voice

`mcp-voice` bundles microphone capture, Kokoro TTS, and STT into one stdio
daemon. Several things prevent it from starting:

- `requires-python = ">=3.14"`. Several dependencies have no cp314 wheels yet, so
  dependency resolution fails before the server runs.
- `webrtcvad` is imported at module top level and listed in the inline script
  metadata, but is **missing from `pyproject.toml` dependencies**. It is also
  effectively unmaintained and needs a C build on modern Python.
- `sounddevice` is imported at module top level, which loads PortAudio at import
  time. No PortAudio, no server — and the failure happens before any tool registers.
- Even when it starts, `listen` needs a TCC microphone grant for the process
  Claude Desktop spawned.

The decisive point: **mcp-voice has no file-transcription tool at all.** Its only
tools are `speak` and `listen` (live mic). Even fully working, it could not have
transcribed a recorded interview. The capability that was actually needed never
existed.

Live TTS/STT for `mock-interview` is a separate concern and belongs in a separate
server, so a microphone permission problem can never take transcription down.
