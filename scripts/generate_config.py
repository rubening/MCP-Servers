import argparse
import json
import os
from pathlib import Path
from typing import Dict, Optional


def _env(var: str, default: Optional[str] = None) -> str:
    value = os.environ.get(var)
    if value:
        return value
    if default is not None:
        return default
    return f"<SET {var}>"


def _path_env(var: str, default: Path) -> Path:
    value = os.environ.get(var)
    if value:
        return Path(value).expanduser().resolve()
    return default


def build_config() -> Dict[str, object]:
    repo_root = _path_env("MCP_REPO_ROOT", Path(__file__).resolve().parents[1])
    data_root = _path_env("MCP_DATA_ROOT", repo_root / "data")
    secure_root = _path_env("MCP_SECURE_ROOT", Path.home() / "Claude Tools")
    secure_data_root = _path_env("MCP_SECURE_DATA_ROOT", secure_root / "secure_data")
    secure_config_root = _path_env("MCP_SECURE_CONFIG_ROOT", secure_root / "config")

    servers = repo_root / "servers"
    python_servers = servers / "python"
    node_servers = servers / "node"

    return {
        "mcpServers": {
            "filesystem": {
                "command": "py",
                "args": [str(python_servers / "filesystem" / "filesystem.py")],
            },
            "execute-command": {
                "command": "py",
                "args": [str(python_servers / "execute-command" / "execute_command.py")],
            },
            "git": {
                "command": "py",
                "args": [str(python_servers / "git" / "git.py")],
            },
            "youtube": {
                "command": "py",
                "args": [str(python_servers / "youtube" / "youtube_enhanced.py")],
            },
            "project-instructions-generator": {
                "command": "py",
                "args": [
                    str(
                        python_servers
                        / "project-instructions-generator"
                        / "project_instructions_generator.py"
                    )
                ],
            },
            "personal-knowledge-intelligence": {
                "command": "py",
                "args": [
                    str(
                        python_servers
                        / "personal-knowledge-intelligence"
                        / "personal_knowledge_intelligence_fixed.py"
                    ),
                    "--db-path",
                    str(data_root / "personal_intelligence.db"),
                ],
            },
            "analytics": {
                "command": "py",
                "args": [
                    str(python_servers / "analytics" / "duckdb_analytics_fixed.py"),
                    "--db-path",
                    str(data_root / "business_intelligence.db"),
                ],
            },
            "github": {
                "command": "docker",
                "args": [
                    "run",
                    "--rm",
                    "-i",
                    "-e",
                    f"GITHUB_PERSONAL_ACCESS_TOKEN={_env('GITHUB_PERSONAL_ACCESS_TOKEN')}",
                    "ghcr.io/github/github-mcp-server",
                ],
            },
            "playwright": {
                "command": "docker",
                "args": [
                    "run",
                    "--rm",
                    "-i",
                    "--cap-add=SYS_ADMIN",
                    "mcr.microsoft.com/playwright/mcp",
                ],
            },
            "sequentialthinking": {
                "command": "docker",
                "args": ["run", "--rm", "-i", "mcp/sequentialthinking"],
            },
            "deepseek": {
                "command": "py",
                "args": [str(python_servers / "deepseek" / "deepseek_protocol_fixed.py")],
                "env": {
                    "OPENROUTER_API_KEY": _env("OPENROUTER_API_KEY"),
                    "DEEPSEEK_API_KEY": _env("DEEPSEEK_API_KEY"),
                },
            },
            "clickup": {
                "command": "npx",
                "args": ["-y", "@taazkareem/clickup-mcp-server@latest"],
                "env": {
                    "CLICKUP_API_KEY": _env("CLICKUP_API_KEY"),
                    "CLICKUP_TEAM_ID": _env("CLICKUP_TEAM_ID"),
                    "DOCUMENT_SUPPORT": "true",
                },
            },
            "chroma-secure": {
                "command": "py",
                "args": [
                    str(python_servers / "chroma-secure" / "chroma_secure_fixed.py"),
                    "--data-dir",
                    str(secure_data_root / "chroma_law_firm"),
                ],
            },
            "gdrive": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-gdrive"],
                "env": {
                    "GDRIVE_CREDENTIALS_PATH": str(
                        secure_config_root / "gdrive-credentials.json"
                    )
                },
            },
            "superclaude": {
                "command": "py",
                "args": [str(python_servers / "superclaude" / "superclaude_server.py")],
                "env": {
                    "SUPERCLAUDE_PLAN_DIR": str(_path_env("SUPERCLAUDE_PLAN_DIR", repo_root / "documentation" / "superclaude_plans")),
                    "SUPERCLAUDE_LOG_PATH": str(_path_env("SUPERCLAUDE_LOG_PATH", repo_root / "logs" / "superclaude_decisions.log")),
                    "SUPERCLAUDE_MAX_DELEGATION_DEPTH": _env("SUPERCLAUDE_MAX_DELEGATION_DEPTH", "3"),
                    "SUPERCLAUDE_AUTO_DELEGATE": _env("SUPERCLAUDE_AUTO_DELEGATE", "false"),
                },
            },
            "web-search": {
                "command": "node",
                "args": [str(node_servers / "web-search" / "index.js")],
                "cwd": str(node_servers / "web-search"),
            },
        }
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Claude Desktop MCP config")
    parser.add_argument(
        "--output",
        default=Path(__file__).resolve().parent / "claude_desktop_config.local.json",
        type=Path,
        help="Output file for generated configuration",
    )
    args = parser.parse_args()

    config = build_config()
    output_path = args.output.expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(config, indent=2), encoding="utf-8")

    print("Generated MCP config:", output_path)
    print("Set environment variables to replace <SET VAR> placeholders before use.")


if __name__ == "__main__":
    main()
