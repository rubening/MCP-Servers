# SuperClaude Quick Reference

This guide distills the Super_Claude_Docs.md resource into actionable notes for the repository version of SuperClaude.

## Personas

| Group | Persona | Primary Focus |
|-------|---------|---------------|
| Development | frontend | UI/UX, accessibility, React/Vue components |
| Development | backend | API design, scalability, reliability |
| Development | architect | System design, long-term decisions |
| Quality | analyzer | Root cause investigation, debugging |
| Quality | security | Threat modeling, compliance |
| Quality | qa | Testing strategy, coverage, edge cases |
| Quality | performance | Profiling, optimization |
| Improvement | refactorer | Technical debt reduction |
| Improvement | mentor | Documentation, onboarding, knowledge transfer |

Use `plan_workflow` to tag each step with an appropriate persona so delegated actions inherit the right expertise.

## MCP Alignment

- **Context7**: official library docs, research-first workflows.
- **Sequential**: multi-step reasoning, architecture, root cause analysis.
- **Magic**: UI component generation, design systems.
- **Puppeteer**: end-to-end and performance testing.

Map these MCP choices to SuperClaude delegation rules to avoid unnecessary token usage and to enforce evidence-based workflows.

## Command Patterns

Typical command structure from the legacy setup:

```
/analyze --seq --persona-analyzer
/build --feature --magic --persona-frontend --tdd
/design --api --seq --persona-architect --ultrathink
/test --coverage --pup --persona-qa
```

In the MCP orchestrator, mirror these combinations when constructing plans:
- Prefer Sequential MCP for complex analysis steps.
- Call filesystem/git before destructive operations to gather evidence.
- Use Magic-equivalent flows (e.g., local UI generators) when personas indicate frontend work.

## Evidence Standards

- Required wording: _may, could, potentially, typically, measured, documented_.
- Avoid absolute claims: _best, optimal, faster, always, never_.
- Validate findings with official documentation (Context7) or reproducible metrics.

## Configuration Hooks

Environment variables exposed via `scripts/generate_config.py`:
- `SUPERCLAUDE_PLAN_DIR`
- `SUPERCLAUDE_LOG_PATH`
- `SUPERCLAUDE_MAX_DELEGATION_DEPTH`
- `SUPERCLAUDE_AUTO_DELEGATE`

Set these in Claude Desktop to customize storage locations and automation behaviour.

## Next Steps

1. Replace `_invoke_tool` stub with real MCP client calls.
2. Expand persona allowlists for additional servers as they are migrated to the shared core.
3. Implement open-task tracking so `summarize_context` can surface outstanding actions.
