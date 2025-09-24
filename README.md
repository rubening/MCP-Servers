# MCP Server Repository
*Model Context Protocol Server Management Platform*

## Overview

This repository houses the full MCP (Model Context Protocol) server ecosystem that powers Claude Desktop and related automation flows. The repo is optimized for multi-language servers, centralized configuration, and disciplined promotion from experiment to production.

## Repository Layout

- `servers/python/` - Production Python MCP servers (filesystem, execute-command, git, analytics, knowledge, business tooling, Google integrations, YouTube).
- `servers/node/` - Node-based MCP servers (currently the web search bridge).
- `business-tools/` - In-flight and specialized automation projects ready for promotion into `servers/python/`.
- `configs/` - Claude Desktop configuration templates and generated outputs.
- `scripts/` - Tooling for config generation and repo automation.
- `documentation/` - System guides, runbooks, and historical reports.
- `data/` - Local database files, schemas, and helper scripts.
- `CHANGELOG.md` - Running log of repository changes for cross-agent context.
- `documentation/SUPERCLAUDE_GUIDE.md` - Persona and MCP quick reference for SuperClaude.

A per-server `README.md` or `CLAUDE.md` documents usage, dependencies, and integration notes.

## Quick Start

### Prerequisites
- Python 3.11+ with MCP-capable CLI (`py` on Windows recommended)
- Node.js 18+ (for Node-based servers)
- Git for version control
- Claude Desktop or Claude Code CLI configured for MCP servers
- Required API keys stored in environment variables (see individual server docs)

### Running a Python Server
```powershell
cd servers/python/filesystem
py filesystem.py
```

### Running a Node Server
```powershell
cd servers/node/web-search
npm install
npm start
```

### Configuration
Run `py scripts/generate_config.py` to produce `configs/claude_desktop_config.json`-compatible output at `scripts/claude_desktop_config.local.json`. Override paths with environment variables (`MCP_REPO_ROOT`, `MCP_DATA_ROOT`, etc.) and ensure secrets are injected through env vars before copying into Claude Desktop.


## SuperClaude Orchestrator

- Server: `servers/python/superclaude/superclaude_server.py`
- Design: `documentation/SUPERCLAUDE_DESIGN.md`
- Quick reference: `documentation/SUPERCLAUDE_GUIDE.md`
- Config: enable via `py scripts/generate_config.py` (adds env defaults for plan/log storage).

SuperClaude implements planning (`plan_workflow`), delegation with guardrails (`delegate_task`), context synthesis (`summarize_context`), and decision logging (`log_decision`). Personas and MCP choices mirror the legacy SuperClaude system.
## Development Workflow

1. Build or iterate on a server inside `servers/python/<name>` or `servers/node/<name>`.
2. Keep tooling small and composable; business-specific logic lives in business-tool modules until it graduates.
3. Document every server and update `configs/` when paths or environment variables change.
4. Use feature branches for work-in-progress and submit PRs with tests and docs.
5. Promote experimental servers by moving them into `servers/python/` after meeting testing and documentation standards.
6. Update `CHANGELOG.md` (use `py scripts/update_changelog.py --category Added --message "Your summary"`) so downstream agents have the latest context.

Automated linting, protocol smoke tests, and integration orchestration for SuperClaude will be added as part of the ongoing refactor.

## Security & Operations

- Never commit live API keys - use environment variables and `.env` files excluded from version control.
- Databases in `data/` are local-only artifacts; back them up with the documented OneDrive jobs.
- Logging directories default to `~/Claude Tools/logs`. Adjust via configuration rather than code edits where possible.
- Follow the existing backup cadence (nightly, weekly, monthly) and validate restores after major changes.

---

**Repository Status:** Active Development  
**Maintained By:** Ruben Sanchez  
**License:** Private/Proprietary








