# CLAUDE.md

Guidance for Claude Code when editing individual Python MCP servers in `servers/python/`.

## Directory Layout

Each server lives in `servers/python/<name>/` with optional `tests/`, `requirements.txt`, and runtime assets. Shared utilities now live in `src/mcp_core`; import helpers from there instead of duplicating JSON-RPC or logging boilerplate.

## Standard Server Shape

- Async loop handling JSON-RPC 2.0 via stdin/stdout
- `initialize`, `tools/list`, and `tools/call` handlers
- Consistent error responses:
  ```python
  return {
      "jsonrpc": "2.0",
      "id": request_id,
      "error": {"code": -32000, "message": str(exc)}
  }
  ```
- Logging configured for Windows-friendly UTF-8 output

## Local Development

```powershell
cd servers/python/<name>
py -m pip install -r requirements.txt  # when present
py <entrypoint>.py
```

Tests (when available):
```powershell
cd servers/python/<name>
py -m pytest -q
```

## Coding Standards

- Python 3.11+ syntax, type hints preferred.
- 4-space indentation, `snake_case` functions/variables, `PascalCase` classes.
- Keep modules single-purpose; factor reusable items into `mcp_core` rather than duplicating.

## Security & Configuration

- Respect existing path-allow lists, rate limiting, and credential loading.
- Replace magic strings/paths with configuration parameters or environment variables; leverage `PathPolicy` and config helpers from `mcp_core` when possible.
- Document new env vars in the server `README.md` and update `configs/` once generator changes land.

## Ongoing Refactor

- Adopt `BaseMCPServer` and `ToolSpec` from `mcp_core` when touching existing servers.
- Centralize configuration and policy via shared helpers before adding bespoke logic.
- SuperClaude orchestration depends on accurate tool metadata; keep schemas descriptive and up to date.

Follow these practices to keep the server layer consistent while the refactor proceeds.



