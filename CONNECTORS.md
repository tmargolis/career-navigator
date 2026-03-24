# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. For example, `~~project tracker` might mean Asana, Linear, Jira, or any other project tracker with an MCP server.

Plugins are **tool-agnostic** — they describe workflows in terms of categories (chat, project tracker, knowledge base, etc.) rather than specific products.

**`.mcp.json` in this repo** ships with an empty `mcpServers` object. Optional MCP servers (notably **Apify** for `salary-research`) are meant to be added in the **host app**, e.g. Claude Desktop **Customize → Connectors → Desktop → Apify**, so tokens stay in the connector UI instead of in JSON or `.env` (MCP launcher args do not reliably expand environment variables).

## Connectors for this plugin

| Category | Placeholder | Primary in-repo / host path | Other options |
|----------|-------------|----------------------------|---------------|
| Career | `~~career` | Indeed (Claude Cowork) | LinkedIn, Glassdoor, Monster, ZipRecruiter, Dice, Handshake |
| Salary benchmarks | — | **Apify** MCP via Claude Desktop **Desktop** connector; **Enabled tools:** `call-actor,get-actor-run,get-dataset-items,cheapget/best-job-search` | Future MCPs; skills should degrade gracefully if Apify is off |
