import os
from pathlib import Path
from string import Template


def _json_escape_path(p: str) -> str:
    """Escape backslashes for JSON string contexts."""
    return p.replace("\\", "\\\\")


def generate_mcp_config() -> None:
    """Generate a Claude Desktop TEST config from a template.

    - Reads template from: <OneDrive>\\mcp_servers\\configs\\mcp_template.json
    - Writes output to:    <OneDrive>\\mcp_servers\\configs\\claude_desktop_config_TEST.json
    - Substitutes placeholders: ONEDRIVE_PATH, LOCAL_SECURE_PATH
      Supports both `$ONEDRIVE_PATH` (Template) and `{{ONEDRIVE_PATH}}` styles.
    """

    # Resolve base paths (env override > sensible default)
    onedrive_env = os.environ.get("OneDrive") or os.environ.get("ONEDRIVE")
    onedrive_path = onedrive_env or str(Path.home() / "OneDrive")
    local_secure_path = os.environ.get("LOCAL_SECURE_PATH") or str(Path.home() / "Claude Tools")

    print("Generating MCP config from template…")
    print(f"OneDrive path: {onedrive_path}")
    print(f"Local secure path: {local_secure_path}")

    base_dirname = os.environ.get("MCP_SERVERS_DIRNAME", "mcp_servers")

    template_path = Path(onedrive_path) / base_dirname / "configs" / "mcp_template.json"
    output_path = Path(onedrive_path) / base_dirname / "configs" / "claude_desktop_config_TEST.json"

    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    template_content = template_path.read_text(encoding="utf-8")

    # Prefer JSON-escaped paths since templates usually produce JSON
    od_json = _json_escape_path(onedrive_path)
    ls_json = _json_escape_path(local_secure_path)

    # Support both {{PLACEHOLDER}} and $PLACEHOLDER styles
    if "{{ONEDRIVE_PATH}}" in template_content or "{{LOCAL_SECURE_PATH}}" in template_content:
        config_content = (
            template_content
            .replace("{{ONEDRIVE_PATH}}", od_json)
            .replace("{{LOCAL_SECURE_PATH}}", ls_json)
            .replace("\\\\MCP_Servers\\\\", "\\\\mcp_servers\\\\")
        )
    else:
        # Template placeholders only; still normalize directory casing just in case
        config_content = Template(template_content).substitute(
            ONEDRIVE_PATH=od_json,
            LOCAL_SECURE_PATH=ls_json,
        ).replace("\\\\MCP_Servers\\\\", "\\\\mcp_servers\\\\")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(config_content, encoding="utf-8")

    print(f"Generated TEST config: {output_path}")
    print("This file has real paths (no placeholders).")
    print("When ready, copy to your Claude Desktop config location.")


if __name__ == "__main__":
    generate_mcp_config()
