# Changelog

All notable changes to this repo will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Established repository-wide changelog for cross-agent visibility.
- Introduced `mcp_core` shared package, reorganized servers under `servers/python/` and `servers/node/`.
- Refactored DeepSeek MCP server to use shared utilities and asynchronous API execution.
- Switched config templates and generator to env-driven placeholders with sanitized defaults.
- Scaffolded SuperClaude MCP server with planning, delegation, and context tools.
- Documented SuperClaude design and quick-reference guides derived from Super_Claude_Docs.md.

### Changed
- Updated documentation (`README.md`, `CLAUDE.md`, `AGENTS.md`) to reflect new layout and workflows.
- Moved configuration guidance to emphasize generated configs and environment variable usage.
- Extended config templates/generator and repository docs to register SuperClaude workflows.

### Removed
- Legacy server duplicates and outdated directory structure entries.
