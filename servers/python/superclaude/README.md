# SuperClaude MCP Server

SuperClaude coordinates other MCP servers with planning, delegation, and context synthesis tools rooted in the SuperClaude personas and workflows.

## Tools

- `plan_workflow`: produce a plan file (JSON) and tag steps with suggested personas.
- `delegate_task`: guard-railed delegation to approved servers/tools.
- `summarize_context`: aggregate changelog and recent plan information.
- `log_decision`: append decisions and next actions to a structured log file.

## Configuration

Environment variables (defaults set by config generator):

- `SUPERCLAUDE_PLAN_DIR`
- `SUPERCLAUDE_LOG_PATH`
- `SUPERCLAUDE_MAX_DELEGATION_DEPTH`
- `SUPERCLAUDE_AUTO_DELEGATE`

See `documentation/SUPERCLAUDE_GUIDE.md` for persona guidance and legacy workflow mapping.
