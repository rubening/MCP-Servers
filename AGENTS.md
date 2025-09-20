# Repository Guidelines

## Project Structure & Module Organization
- Core code lives in `servers/` (Python MCP servers) and `external-services/` (Node-based MCP servers). Examples: `servers/filesystem/`, `servers/deepseek/`, `external-services/web-search-mcp-server/`.
- Shared assets and docs: `configs/` (templates, Claude Desktop configs), `documentation/` (project docs), `data/` (sample datasets), `scripts/` (repo utilities).
- Each server should include a short `README.md` and, if applicable, a `requirements.txt` or `package.json`.

## Build, Test, and Development Commands
- Python server (example DeepSeek):
  - `cd servers/deepseek`
  - `pip install -r requirements.txt`
  - Run locally: `python deepseek.py`
- Node server (web search):
  - `cd external-services/web-search-mcp-server`
  - `npm install`
  - Run locally: `npm start`
- Config generation: `python scripts/generate_config.py` (produces a Claude Desktop test config from templates in `configs/`).

## Coding Style & Naming Conventions
- Python: 4-space indentation, type hints where practical, PEP 8 function/variable names (`snake_case`), classes `PascalCase`, modules `snake_case.py`.
- JavaScript/TypeScript: prefer consistent Prettier/StandardJS style; files `kebab-case.js` within Node servers.
- Keep server directories `kebab-case` (e.g., `google-sheets`, `lead-qualification`). Small, focused modules; avoid monoliths.

## Testing Guidelines
- Python: prefer `pytest` with tests named `test_*.py` near the code or under `servers/<name>/tests/`. Example: `python -m pytest -q`.
- Ad-hoc checks: many servers include simple scripts (e.g., `servers/test_deepseek.py`) to validate JSON-RPC flows.
- Target coverage: >70% for promoted (non-experimental) servers. Include integration tests for external APIs when feasible (guard with env vars and marks).

## Commit & Pull Request Guidelines
- Commits: concise, imperative, and scoped. Prefer Conventional Commits when possible: `feat(servers/deepseek): add chat tool`, `fix(filesystem): guard path traversal)`.
- PRs must include:
  - Clear description, motivation, and scope; link related issues.
  - Usage notes and configuration changes (update server `README.md` and `configs/` if needed).
  - Screenshots or sample requests/responses for user-visible behavior.
  - Evidence of testing (commands run, logs, or CI results).
- Security: never commit secrets. Use environment variables; document required keys in the server `README.md`.

## Security & Configuration Tips
- Store API keys in env vars; keep templates in `configs/` and local overrides out of VCS.
- When adding servers, document required env vars, start command, and `tools/list` output to ease Claude Desktop integration.
