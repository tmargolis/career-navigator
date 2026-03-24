# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. For example, `~~project tracker` might mean Asana, Linear, Jira, or any other project tracker with an MCP server.

Plugins are **tool-agnostic** — they describe workflows in terms of categories (chat, project tracker, knowledge base, etc.) rather than specific products.

**`.mcp.json` in this repo** ships with an empty `mcpServers` object. Host-native connectors (**Indeed** for job search, **Apify** for salary) are added in the **Claude Desktop** **Customize → Connectors** UI. **Indeed** uses **OAuth in the browser** (Indeed on **secure.indeed.com**); **Apify** uses a token + **Enabled tools** in its connector form. This keeps secrets out of repo JSON and avoids unreliable `${VAR}` expansion in MCP `args`.

## Connectors for this plugin

| Category | Placeholder | Primary in-repo / host path | Other options |
|----------|-------------|----------------------------|---------------|
| Career | `~~career` | **Indeed** MCP — Claude Desktop **Connectors** → **Indeed** → **Connect** → browser OAuth (`search_jobs`, `get_job_details`; connector URL `https://mcp.indeed.com/claude/mcp`) | LinkedIn, Glassdoor, Monster, ZipRecruiter, Dice, Handshake |
| Salary benchmarks | — | **Apify** MCP via Claude Desktop **Desktop** connector; **Enabled tools:** `call-actor,get-actor-run,get-dataset-items,cheapget/best-job-search` | Future MCPs; skills should degrade gracefully if Apify is off |
