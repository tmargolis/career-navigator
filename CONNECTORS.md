# Storage Connectors

Career Navigator uses a connector-based storage model. All plugin components call a standard interface — they never reference the specific backend directly. This means you can switch storage backends without changing any command or agent logic.

## Active Connector: Local (Phase 1A default)

All artifacts are saved to `data/artifacts/` locally. Application records are stored in `data/applications/tracker.json`. The corpus lives in `data/corpus/index.json`. All user data directories are gitignored.

The `~~storage` placeholder in commands refers to the active connector's `save_artifact()` method. In Phase 1A, this writes to the local `data/` tree.

## Storage Interface

| Method | Description |
|--------|-------------|
| `save_artifact(artifact, metadata)` | Saves a generated document with metadata |
| `list_artifacts(filters)` | Returns filterable list of artifacts |
| `get_artifact(id)` | Retrieves a specific artifact by ID |
| `save_event(event)` | Logs a tracker event to the structured event store |
| `query_events(filters)` | Returns structured events for analytics |

## Available Connectors

| Connector | Status | Description |
|-----------|--------|-------------|
| **local** | Active (Phase 1A) | Saves to `data/` subdirectories. No setup required. |
| **google-drive** | Planned (Phase 1A) | Google Drive via OAuth. See `.mcp.json` setup instructions. |
| **onedrive** | Phase 2C | Microsoft OneDrive via OAuth. |
| **dropbox** | Phase 2C | Dropbox via OAuth. |

## Switching Connectors

To activate Google Drive:
1. Complete the setup steps in `.mcp.json` under `_inactive_services.google-drive`
2. Move the `google-drive` entry from `_inactive_services` to `mcpServers`
3. Restart Claude Cowork (or Claude Code) — the connector activates automatically on next session

Local data in `data/` is not automatically migrated to cloud storage. You can manually upload existing artifacts to your Drive folder after switching.

## Data Locations (Local Connector)

```
data/
├── corpus/
│   └── index.json          — Resume corpus (experience units, skill tags, weights)
├── applications/
│   └── tracker.json        — Application records and stage history
└── artifacts/
    ├── index.json           — Artifact inventory with metadata
    └── [artifact files]    — Generated resumes, cover letters, etc.
```

All files in `data/` are gitignored. They live only on your machine unless you configure a cloud connector.
