#!/usr/bin/env python3
"""SuperClaude MCP server scaffold using shared MCP core utilities."""

from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path
from typing import Any, Dict, List

from mcp_core import BaseMCPServer, MCPError, ToolSpec, configure_logger

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_PLAN_DIR = ROOT / "documentation" / "superclaude_plans"
DEFAULT_LOG_PATH = ROOT / "logs" / "superclaude_decisions.log"


class SuperClaudeServer(BaseMCPServer):
    """High-level orchestrator coordinating other MCP tools."""

    def __init__(self) -> None:
        logger = configure_logger("superclaude")
        super().__init__("superclaude", "0.1.0", logger=logger)

        self.plan_dir = Path(os.environ.get("SUPERCLAUDE_PLAN_DIR", DEFAULT_PLAN_DIR)).expanduser()
        self.log_path = Path(os.environ.get("SUPERCLAUDE_LOG_PATH", DEFAULT_LOG_PATH)).expanduser()
        self.max_depth = int(os.environ.get("SUPERCLAUDE_MAX_DELEGATION_DEPTH", "3"))
        self.allow_auto_delegate = os.environ.get("SUPERCLAUDE_AUTO_DELEGATE", "false").lower() == "true"
        self.plan_dir.mkdir(parents=True, exist_ok=True)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

        self.allowed_tools = {
            "filesystem": {"list_directory", "read_file", "write_file"},
            "git": {"status", "diff"},
            "analytics": {"run_query"},
        }

        self.register_tool(
            ToolSpec(
                name="plan_workflow",
                description="Create a structured plan for a high-level objective.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "goal": {"type": "string", "description": "Primary objective"},
                        "constraints": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Optional constraints or notes",
                        },
                        "persona": {
                            "type": "string",
                            "description": "Preferred SuperClaude persona to lead execution",
                        },
                    },
                    "required": ["goal"],
                    "additionalProperties": False,
                },
                handler=self._plan_workflow,
            )
        )

        self.register_tool(
            ToolSpec(
                name="delegate_task",
                description="Delegate a plan step to another MCP server/tool with guardrails.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "step": {"type": "string", "description": "Plan step identifier"},
                        "server": {"type": "string", "description": "Target MCP server name"},
                        "tool": {"type": "string", "description": "Tool name on the target server"},
                        "arguments": {
                            "type": "object",
                            "description": "Arguments to pass to the delegated tool",
                        },
                        "persona": {
                            "type": "string",
                            "description": "Persona responsible for this delegation",
                        },
                        "auto_confirm": {
                            "type": "boolean",
                            "description": "Allow execution without additional confirmation",
                            "default": False,
                        },
                    },
                    "required": ["step", "server", "tool"],
                    "additionalProperties": False,
                },
                handler=self._delegate_task,
            )
        )

        self.register_tool(
            ToolSpec(
                name="summarize_context",
                description="Generate a context summary using changelog and plan artifacts.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "include_changelog": {"type": "boolean", "default": True},
                        "include_plans": {"type": "boolean", "default": True},
                        "include_open_tasks": {"type": "boolean", "default": True},
                        "highlight_personas": {"type": "boolean", "default": False},
                    },
                    "additionalProperties": False,
                },
                handler=self._summarize_context,
            )
        )

        self.register_tool(
            ToolSpec(
                name="log_decision",
                description="Append a decision entry to the SuperClaude log.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "decision": {"type": "string", "description": "Decision summary"},
                        "rationale": {"type": "string", "description": "Why this decision was made"},
                        "next_actions": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Follow-up steps",
                        },
                        "persona": {
                            "type": "string",
                            "description": "Persona accountable for next actions",
                        },
                    },
                    "required": ["decision"],
                    "additionalProperties": False,
                },
                handler=self._log_decision,
            )
        )

    async def _plan_workflow(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        goal = arguments["goal"].strip()
        constraints = arguments.get("constraints") or []
        persona = arguments.get("persona", "architect")

        plan = [
            {
                "id": "step-1",
                "action": "Review repository changelog",
                "server": "filesystem",
                "tool": "read_file",
                "arguments": {"path": str(ROOT / "CHANGELOG.md")},
                "persona": "analyzer",
            },
            {
                "id": "step-2",
                "action": "Draft solution outline",
                "server": "superclaude",
                "tool": "summarize_context",
                "arguments": {"include_plans": True, "highlight_personas": True},
                "persona": persona,
            },
        ]

        plan_path = self.plan_dir / f"plan_{self._sanitize_filename(goal)}.json"
        plan_payload = {
            "goal": goal,
            "constraints": constraints,
            "persona": persona,
            "plan": plan,
        }
        plan_path.write_text(json.dumps(plan_payload, indent=2), encoding="utf-8")

        return {
            "goal": goal,
            "constraints": constraints,
            "persona": persona,
            "plan": plan,
            "plan_path": str(plan_path),
        }

    async def _delegate_task(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        server_name = arguments["server"]
        tool_name = arguments["tool"]
        auto_confirm = bool(arguments.get("auto_confirm"))
        persona = arguments.get("persona", "refactorer")

        if server_name not in self.allowed_tools or tool_name not in self.allowed_tools[server_name]:
            raise MCPError(
                f"Delegation to {server_name}.{tool_name} is not permitted. Update allowlist if this is intentional.",
                code=-32602,
            )

        if not (self.allow_auto_delegate or auto_confirm):
            return {
                "status": "confirmation_required",
                "message": "Auto delegation disabled. Re-run with auto_confirm true or enable SUPERCLAUDE_AUTO_DELEGATE.",
            }

        response = await self._invoke_tool(server_name, tool_name, arguments.get("arguments") or {})

        return {
            "status": "completed",
            "server": server_name,
            "tool": tool_name,
            "persona": persona,
            "result": response,
        }

    async def _summarize_context(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        include_changelog = arguments.get("include_changelog", True)
        include_plans = arguments.get("include_plans", True)
        include_open = arguments.get("include_open_tasks", True)
        highlight_personas = arguments.get("highlight_personas", False)

        summary_parts: List[str] = []

        if include_changelog:
            changelog_path = ROOT / "CHANGELOG.md"
            if changelog_path.exists():
                summary_parts.append("Changelog tail:\n" + self._read_tail(changelog_path))

        if include_plans:
            plans = list(sorted(self.plan_dir.glob("plan_*.json"), reverse=True))[:5]
            if plans:
                plan_lines = []
                for path in plans:
                    data = json.loads(path.read_text(encoding="utf-8"))
                    persona = data.get("persona", "architect")
                    plan_lines.append(f"- {data.get('goal')} ({len(data.get('plan', []))} steps | persona: {persona})")
                summary_parts.append("Recent plans:\n" + "\n".join(plan_lines))

        if include_open:
            summary_parts.append("Open task tracking is not yet implemented. Track next actions via log_decision results.")

        if highlight_personas:
            summary_parts.append("Persona guidance sourced from Super_Claude_Docs.md (development, quality, improvement groups).")

        return {"summary": "\n\n".join(summary_parts).strip()}

    async def _log_decision(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        decision = arguments["decision"].strip()
        rationale = arguments.get("rationale", "").strip()
        next_actions = arguments.get("next_actions") or []
        persona = arguments.get("persona", "mentor")

        entry = {
            "decision": decision,
            "rationale": rationale,
            "next_actions": next_actions,
            "persona": persona,
        }
        self._append_log(entry)
        return {"logged": True, "path": str(self.log_path)}

    async def _invoke_tool(self, server: str, tool: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        await asyncio.sleep(0)
        return {
            "stub": True,
            "server": server,
            "tool": tool,
            "arguments": arguments,
        }

    def _append_log(self, entry: Dict[str, Any]) -> None:
        line = json.dumps(entry)
        with self.log_path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")

    def _read_tail(self, path: Path, max_lines: int = 40) -> str:
        lines = path.read_text(encoding="utf-8").splitlines()
        return "\n".join(lines[-max_lines:])

    def _sanitize_filename(self, text: str) -> str:
        return "_".join(text.lower().split())[:80]


async def main() -> None:
    server = SuperClaudeServer()
    loop = asyncio.get_event_loop()

    while True:
        try:
            line = await loop.run_in_executor(None, input)
        except EOFError:
            break
        if not line:
            break

        try:
            request = json.loads(line)
        except json.JSONDecodeError:
            continue

        response = await server.handle_request(request)
        print(json.dumps(response))


if __name__ == "__main__":
    asyncio.run(main())
