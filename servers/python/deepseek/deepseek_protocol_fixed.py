#!/usr/bin/env python3
"""
DeepSeek MCP Server leveraging shared MCP core utilities.
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict

import requests

# Ensure the shared core package is importable whether executed from repo root or server dir.
def _bootstrap_paths() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "pyproject.toml").exists():
            src_dir = parent / "src"
            if src_dir.exists() and str(src_dir) not in sys.path:
                sys.path.insert(0, str(src_dir))
            return parent
    raise RuntimeError("Unable to locate repository root for DeepSeek server")


REPO_ROOT = _bootstrap_paths()

from mcp_core import BaseMCPServer, MCPError, ToolSpec, configure_logger  # noqa: E402


class DeepSeekMCPServer(BaseMCPServer):
    """DeepSeek integration using the shared MCP server base."""

    OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
    DEEPSEEK_URL = "https://api.deepseek.com/chat/completions"

    def __init__(self) -> None:
        logger = configure_logger("deepseek-mcp")
        super().__init__("deepseek-mcp-server", "1.1.0", logger=logger)

        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        self.deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")

        self.register_tool(
            ToolSpec(
                name="deepseek_reasoning",
                description="Advanced reasoning using DeepSeek R1 for complex analysis and problem-solving",
                input_schema={
                    "type": "object",
                    "properties": {
                        "prompt": {
                            "type": "string",
                            "description": "The complex question or problem requiring deep reasoning",
                        }
                    },
                    "required": ["prompt"],
                    "additionalProperties": False,
                },
                handler=self._handle_reasoning,
            )
        )

        self.register_tool(
            ToolSpec(
                name="deepseek_chat",
                description="General conversation using DeepSeek Chat for questions and discussions",
                input_schema={
                    "type": "object",
                    "properties": {
                        "prompt": {
                            "type": "string",
                            "description": "The question or topic for discussion",
                        }
                    },
                    "required": ["prompt"],
                    "additionalProperties": False,
                },
                handler=self._handle_chat,
            )
        )

    # ------------------------------------------------------------------
    # Tool handlers
    # ------------------------------------------------------------------
    async def _handle_reasoning(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        prompt = self._extract_prompt(arguments)
        result = await asyncio.to_thread(self._call_deepseek_api, prompt, "deepseek-r1")
        return self._format_result(result)

    async def _handle_chat(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        prompt = self._extract_prompt(arguments)
        result = await asyncio.to_thread(self._call_deepseek_api, prompt, "deepseek-chat")
        return self._format_result(result)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _extract_prompt(self, arguments: Dict[str, Any]) -> str:
        prompt = (arguments.get("prompt") or "").strip()
        if not prompt:
            raise MCPError("Missing prompt argument", code=-32602)
        if not (self.openrouter_api_key or self.deepseek_api_key):
            raise MCPError(
                "Set OPENROUTER_API_KEY or DEEPSEEK_API_KEY before calling DeepSeek",
                code=-32000,
            )
        return prompt

    def _call_deepseek_api(self, prompt: str, model: str) -> Dict[str, Any]:
        """Call DeepSeek via OpenRouter (preferred) or direct API."""
        try:
            if self.openrouter_api_key:
                url = self.OPENROUTER_URL
                model_name = f"deepseek/{model}"
                headers = {
                    "Authorization": f"Bearer {self.openrouter_api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://claude-desktop",
                    "X-Title": "Claude Desktop DeepSeek MCP",
                }
            elif self.deepseek_api_key:
                url = self.DEEPSEEK_URL
                model_name = "deepseek-reasoner" if model == "deepseek-r1" else "deepseek-chat"
                headers = {
                    "Authorization": f"Bearer {self.deepseek_api_key}",
                    "Content-Type": "application/json",
                }
            else:
                raise MCPError(
                    "Set OPENROUTER_API_KEY or DEEPSEEK_API_KEY before calling DeepSeek",
                    code=-32000,
                )

            payload = {
                "model": model_name,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2 if model == "deepseek-r1" else 0.7,
                "max_tokens": 4000,
                "stream": False,
            }

            response = requests.post(url, headers=headers, json=payload, timeout=60)
            if response.status_code == 200:
                result = response.json()
                content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                return {
                    "success": True,
                    "content": content,
                    "model": model_name,
                    "usage": result.get("usage", {}),
                }

            return {
                "success": False,
                "error": f"API Error {response.status_code}: {response.text[:200]}",
            }
        except MCPError:
            raise
        except Exception as exc:
            self.logger.exception("DeepSeek request failed")
            return {
                "success": False,
                "error": f"Exception: {exc}",
            }

    def _format_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        if result.get("success"):
            response_text = f"**DeepSeek {result.get('model', 'Response')}**\n\n{result.get('content', 'No content returned')}"
            usage = result.get("usage") or {}
            if usage:
                response_text += f"\n\n*Tokens: {usage.get('total_tokens', 'unknown')}*"
        else:
            response_text = f"**DeepSeek Error:** {result.get('error', 'Unknown error occurred')}"

        return {"content": [{"type": "text", "text": response_text}]}


async def main() -> None:
    server = DeepSeekMCPServer()

    if not (server.openrouter_api_key or server.deepseek_api_key):
        server.logger.error("No API key found. Set OPENROUTER_API_KEY or DEEPSEEK_API_KEY")
        return

    loop = asyncio.get_event_loop()
    while True:
        line = await loop.run_in_executor(None, sys.stdin.readline)
        if not line:
            break

        try:
            request = json.loads(line.strip())
        except (json.JSONDecodeError, Exception):
            # Match legacy tolerance for malformed input
            continue

        try:
            response = await server.handle_request(request)
        except Exception:
            # Preserve legacy silent failure behaviour
            continue

        print(json.dumps(response))
        sys.stdout.flush()


if __name__ == "__main__":
    asyncio.run(main())
