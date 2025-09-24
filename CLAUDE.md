# CLAUDE.md

This file guides Claude Code when working in this repository.

## Architecture Snapshot

The repo organizes MCP servers by runtime:
- `servers/python/<name>/` - Production Python servers (filesystem, execute-command, git, analytics, knowledge, Google integrations, business tooling, YouTube).
- `servers/node/<name>/` - Node-based integrations (currently the web search bridge). Additional services will land here.
- `business-tools/` - Promotion pipeline projects that will graduate into `servers/python/` as the refactor progresses.

Supporting directories:
- `src/mcp_core/` - Shared MCP helpers (logging, JSON-RPC base class, path policy utilities).
- `configs/` - Claude Desktop configuration templates and generated files.
- `scripts/` - Repo automation (config generation, validation utilities).
- `documentation/` - Knowledge base, runbooks, historical reports.
- `data/` - Local database files, schemas, and helper utilities.

## Context Sources
- Read `CHANGELOG.md` first to understand recent shifts before editing code or configs.
- Reference the changelog when summarizing work back to the user or other agents.

## Development Commands

### Python Servers
```powershell
cd servers/python/<name>
py -m pip install -r requirements.txt  # when present
py <entrypoint>.py
```

### Node Servers
```powershell
cd servers/node/<name>
npm install
npm start
```

### Configuration Generation
```powershell
py scripts/generate_config.py
```

(Generator already emits sanitized configs with env-driven paths; SuperClaude defaults will land during orchestration work.)

## SuperClaude Notes
- Orchestrator server: `servers/python/superclaude/superclaude_server.py`.
- Review `documentation/SUPERCLAUDE_GUIDE.md` for personas and MCP combinations before planning workflows.
- Config generator now exports SuperClaude env vars; confirm Claude Desktop loads them.
- `_invoke_tool` is stubbed; replace with real MCP client logic when delegating.

## MCP Protocol Expectations

All servers respond to the JSON-RPC 2.0 trio (`initialize`, `tools/list`, `tools/call`). Shared helpers now live in `src/mcp_core`; prefer importing `BaseMCPServer`, `ToolSpec`, and `MCPError` instead of duplicating protocol scaffolding.

## Promotion Workflow

1. Build or iterate in `business-tools/`.
2. Once stable, migrate into `servers/python/<name>` with docs, tests, and config updates.
3. Update `configs/` and documentation to reflect new paths and required environment variables.
4. Ensure smoke tests cover JSON-RPC basics before promotion.

## Security & Operational Notes

- Secrets belong in environment variables; templates may include `${VAR_NAME}` placeholders but never real tokens.
- File access policies will migrate to shared helpers; avoid adding new hard-coded absolute paths.
- Logging defaults to `~/Claude Tools/logs`; prefer configuration flags over inline path edits.
- When integrating SuperClaude, expose orchestration tools via the shared package and register the server in `configs/` using the templating workflow.

## Current Refactor Focus

- Expand `src/mcp_core` with reusable logging, policy, and runtime helpers.
- Migrate representative servers (`deepseek` done, `filesystem` and `execute-command` next) to the shared base.
- Replace the static config sample with env-aware templates and add tests for generator output.
- Introduce smoke-test suites for every server and wire into CI.

Stay consistent with these conventions to keep Claude Code productive during the transition.




