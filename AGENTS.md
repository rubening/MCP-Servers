# Repository Guidelines

## Project Structure & Module Organization
- Production Python MCP servers live in `servers/python/<name>/` (e.g., `servers/python/filesystem/`).
- Node-based MCP servers live in `servers/node/<name>/` (e.g., `servers/node/web-search/`).
- Promotion candidates and domain experiments stay in `business-tools/` until they satisfy graduation criteria.
- Shared assets and docs remain in `configs/`, `documentation/`, `data/`, and `scripts/`.
- Each server owns a `README.md` (and optional `CLAUDE.md`) describing tools, dependencies, and environment variables.

## Build, Test, and Development Commands
- Python server example (DeepSeek):
  - `cd servers/python/deepseek`
  - `py -m pip install -r requirements.txt`
  - Run locally: `py deepseek_protocol_fixed.py`
- Node server example (web search):
  - `cd servers/node/web-search`
  - `npm install`
  - Run locally: `npm start`
- Config generation: `py scripts/generate_config.py` (writes `scripts/claude_desktop_config.local.json`; configure paths via `MCP_*` env vars and inject secrets through the environment).

## Coding Style & Naming Conventions
- Python: 4-space indentation, type hints where practical, PEP 8 naming (`snake_case` functions/variables, `PascalCase` classes), modules `snake_case.py`.
- JavaScript/TypeScript: follow Prettier/StandardJS conventions; filenames `kebab-case.js` inside Node servers.
- Directory naming stays `kebab-case` (`google-ads`, `lead-qualification`). Favor small, composable modules over monoliths.

## Testing Guidelines
- Python: prefer `pytest` with tests near code or under `servers/python/<name>/tests/`. Example: `py -m pytest -q`.
- Ad-hoc checks: keep simple JSON-RPC validation scripts (e.g., `servers/python/deepseek/tests/test_deepseek.py`) for rapid smoke testing.
- Target coverage: >70% for promoted servers. Include integration tests for external APIs when feasible (guard with env vars and markers).

## Commit & Pull Request Guidelines
- Commits: concise, imperative, scoped. Prefer Conventional Commit prefixes: `feat(servers/python/deepseek): add chat tool`, `fix(filesystem): guard path traversal`.
- PRs must include:
  - Motivation, scope, and related issue/initiative links.
  - Usage/configuration notes (update server `README.md` + `configs/` when paths/env vars change).
  - Evidence of testing (commands run, logs, or CI results).
  - Screenshots/sample payloads for user-visible changes.
- Security: never commit secrets. Use env vars/.env files documented in server READMEs.

## Security & Configuration Tips
- Store API keys in env vars; keep templates in `configs/` and exclude local overrides from VCS.
- When adding servers, document required env vars, start command, and `tools/list` output to simplify Claude Desktop integration.
- Prefer configuration files or env overrides instead of hard-coded paths; the shared core module will centralize policy enforcement as refactor progresses.

