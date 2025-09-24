# SuperClaude Orchestrator - Design Overview

## Purpose
SuperClaude acts as a high-level orchestration MCP server that coordinates other agents and MCP services to deliver multi-step assistance inside Claude Code. It provides planning, delegation, and context synthesis on top of existing tooling.

## Primary Responsibilities
- **Workflow Planning**: Accept user objectives, break them into structured plans, and suggest which MCP tools should be invoked.
- **Tool Delegation**: Dispatch `tools/call` requests to other MCP servers (filesystem, git, analytics, etc.) and track progress.
- **Context Synthesis**: Summarize state across repositories, changelog entries, and active plans for downstream agents or handoffs.
- **Human-in-the-loop Support**: Provide checkpoints, request confirmation before running destructive operations, and produce status digests.

## MVP Capabilities
1. `plan_workflow`
   - Input: goal description, optional constraints.
   - Output: ordered steps referencing relevant MCP tools.
2. `delegate_task`
   - Input: plan step identifier plus target MCP server/tool and arguments.
   - Output: Execution status, raw tool response, and follow-up recommendations.
3. `summarize_context`
   - Input: scope flags (`repo`, `changelog`, `open_tasks`).
   - Output: Consolidated narrative with references to key files and outstanding actions.
4. `log_decision`
   - Input: decision summary, rationale, next actions.
   - Output: Appends to a local log file for traceability.

## Future Enhancements (Post-MVP)
- Automatic rollback suggestions when delegated tasks fail.
- Integration with design docs (e.g., auto-update SuperClaude plan files).
- Cross-session memory using personal knowledge intelligence DB.
- Rate limiting and priority scheduling for long-running tasks.

## Dependencies & Integration Points
- Uses the shared `mcp_core` package (`BaseMCPServer`, `ToolSpec`, `MCPError`).
- Calls other MCP servers via a lightweight JSON-RPC client (`asyncio` + stdio subprocess) – implement in `servers/python/superclaude/client.py`.
- Reads `CHANGELOG.md` and relevant docs to seed context summaries.
- Configured via environment variables for:
  - `SUPERCLAUDE_LOG_PATH`
  - `SUPERCLAUDE_PLAN_DIR`
  - `SUPERCLAUDE_MAX_DELEGATION_DEPTH`

## Security & Safeguards
- All delegated actions require explicit user confirmation unless `allow_auto_delegate` flag is present.
- Maintains allowlist of callable MCP tools; dangerous operations require double confirmation.
- Logs every delegated call with timestamp, tool, arguments, and result snippet.

## Testing Strategy
- Unit tests for planning heuristics and policy validation.
- Mocked integration tests to simulate delegation to filesystem and git servers.
- End-to-end smoke test running a full plan/delegate/summarize loop with fixture responses.

## Rollout Plan
1. Implement server skeleton with `plan_workflow`, `delegate_task`, `summarize_context`, `log_decision`.
2. Add config entry templates (`configs/mcp_template.json`, generator). 
3. Document usage in `documentation/SUPERCLAUDE_GUIDE.md` and link from `README.md`.
4. Integrate with changelog helper to capture orchestration milestones.

## External Reference
- Source: Super_Claude_Docs.md (workspace root) – contains original persona and workflow definitions used to prepare this design.
