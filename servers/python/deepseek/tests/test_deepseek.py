#!/usr/bin/env python3
"""Ad-hoc test harness for the DeepSeek MCP server."""

import asyncio
import json
import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
SERVER_DIR = CURRENT_DIR.parent

if str(SERVER_DIR) not in sys.path:
    sys.path.insert(0, str(SERVER_DIR))

from deepseek_protocol_fixed import DeepSeekMCPServer  # noqa: E402


async def test_deepseek_server() -> None:
    print("=== DeepSeek MCP Server Debug Test ===\n")

    server = DeepSeekMCPServer()

    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {"protocolVersion": "2024-11-05", "capabilities": {}},
    }

    tools_request = {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}

    tool_request = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "deepseek_chat",
            "arguments": {"prompt": "Hello, this is a test message. Please respond briefly."},
        },
    }

    for label, payload in (
        ("Initialize", init_request),
        ("Tools List", tools_request),
        ("Sample Tool Call", tool_request),
    ):
        response = await server.handle_request(payload)
        print(f"-- {label} --")
        print(json.dumps(payload, indent=2))
        print(json.dumps(response, indent=2))
        print()


if __name__ == "__main__":
    asyncio.run(test_deepseek_server())
