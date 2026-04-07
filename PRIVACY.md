# Privacy Policy

Effective date: April 7, 2026

This Privacy Policy describes how Career Navigator ("the plugin") handles data when used in Claude Cowork/Desktop or compatible hosts.

Career Navigator is designed to be local-first. By default, your job-search data stays in your own selected folder (`{user_dir}`) on your machine.

## Scope

This policy applies to data handled by the plugin in this repository, including:

- Job-search documents you provide (resumes, cover letters, notes, interview prep materials)
- Structured plugin artifacts and metadata written under `CareerNavigator/` (for example `profile.md`, `tracker.json`, `ExperienceLibrary.json`, `StoryCorpus.json`, and generated artifacts index files)
- Optional connector-derived context when you explicitly enable and approve those integrations

This policy does not replace the privacy terms of Anthropic, Claude, or third-party connector providers (for example Indeed, Google, Microsoft, Apify, LinkedIn, Notion, Dropbox, OneDrive, Google Drive, Meetup, Eventbrite, Luma). Those services have their own policies and controls.

## Data We Process

Depending on how you use the plugin, processed data may include:

- Profile and preference data (target roles, locations, compensation floor, differentiators)
- Application pipeline data (companies, roles, links, stages, notes, contacts, timestamps)
- Resume and cover letter content (source and generated)
- Networking and content-planning data
- Interview preparation and debrief content
- Optional interview-capture transcripts (see "Interview Capture and Audio")
- Optional connector context from enabled services (see "Connectors and External Services")

## How Data Is Collected

Data is collected through:

- Files you place in your chosen job-search folder
- Commands and conversational inputs you provide in Claude
- Plugin-generated outputs saved back to your folder
- Optional connectors only when you choose to enable them and, where required, explicitly approve lookups

## Storage and Local-First Behavior

- Primary storage is local filesystem storage in your selected `{user_dir}`.
- By default, data does not leave your machine through plugin-managed storage.
- The plugin can work without cloud storage connectors.
- Cloud portability (for example Google Drive, OneDrive, Dropbox) is optional and typically performed through provider sync apps or manual backup/restore workflows.

## Connectors and External Services

Career Navigator supports optional connectors and MCP tools. These are opt-in.

### Connector principles

- Discover first: if tools are already connected in-session, the plugin uses them.
- Configure only if needed: setup prompts occur when tools are missing or disconnected.
- Browser automation only when needed: used for browser-only workflows or when MCP tooling is unavailable.

### Authentication and credentials

- OAuth-based connectors are authenticated through host/provider flows in the browser.
- The plugin does not require you to place service passwords in repository files.
- Long-lived secrets should not be committed to this repository.
- Apify token setup is performed in connector UI, not stored in plugin source files.

### Read-only integration behavior (where implemented)

Current documented behavior includes read-only usage for:

- Gmail / Microsoft 365 email context
- Google Calendar / Microsoft calendar context
- LinkedIn post analytics snapshots (your own posts)
- ATS status connectors such as Greenhouse/Workday/Lever (read-only status sync)

For outreach workflows, email/calendar lookups require explicit user approval before lookup.

## Interview Capture and Audio

Interview capture is optional and opt-in.

Current implemented scope:

- User-audio transcription workflow only (not full two-party recording)
- Structured notes are written to local tracker data
- Employer warning/consent notice behavior is included in the workflow design
- Audio/transcript data is user-deletable

The local `mcp-voice` path (when installed) is designed to run on-device for TTS/STT.

## Why Data Is Used

Data is used to provide job-search assistance, including:

- Resume tailoring and ATS scoring
- Job discovery and ranking
- Application tracking and follow-up timing
- Interview prep, mock interview, and debrief support
- Networking, market, and offer-decision support
- Learning from outcome history to improve future recommendations

## Data Sharing

The plugin itself is designed around local data handling and does not include a built-in remote analytics backend in this repository.

Data may be accessed by external services only when you explicitly enable and use corresponding connectors or host capabilities.

## User Control and Deletion

You control your data via your local files:

- Edit or delete artifacts directly in your `{user_dir}`
- Remove connector access in your host application's connector settings
- Disable optional local extensions (for example voice/event bundles) in the host
- Stop using specific workflows at any time

Because data is file-based and local-first, deleting local files removes plugin-managed copies in this project model.

## Security Notes

- Keep your local machine and account(s) secure.
- Use least-privilege connector access where available.
- Review connector permissions during OAuth.
- Do not commit secrets or private credentials to this repository.

No system can guarantee absolute security; responsible local security practices remain important.

## Children

Career Navigator is intended for professional job-search use and is not designed for children.

## International and Regional Privacy

The project documentation references jurisdiction-aware retention behavior for interview capture workflows (for example policy selection based on user location when applicable). This is implementation guidance, not legal advice.

If you have regulatory obligations (for example GDPR/CCPA or employment-law constraints), evaluate your usage and connector configuration with appropriate legal guidance.

## Changes to This Policy

This policy may be updated as features evolve. The current version is the one in `PRIVACY.md` at the repository root.

## Contact

Project contact is maintained through the repository maintainer and issue tracker:

- GitHub: https://github.com/tmargolis/career-navigator

