#!/usr/bin/env python3
"""
Career Navigator — One-time initialization script.

Registers the filesystem MCP server in Claude Desktop's configuration,
giving Career Navigator read/write access to its data directory.

Run once after extracting the plugin to a permanent location:

    python3 scripts/init.py

Then restart Claude Desktop, install or reinstall the plugin, and run
/career-navigator:setup to complete configuration.
"""

import os
import json
import platform
from pathlib import Path

MCP_SERVER_KEY = "career-navigator"


def find_claude_config_path():
    """Return the path to Claude Desktop's config file for the current OS."""
    home = Path.home()
    system = platform.system()

    if system == "Darwin":
        return home / "Library/Application Support/Claude/claude_desktop_config.json"
    elif system == "Windows":
        appdata = os.environ.get("APPDATA")
        if not appdata:
            raise EnvironmentError("APPDATA environment variable is not set.")
        return Path(appdata) / "Claude/claude_desktop_config.json"
    elif system == "Linux":
        xdg = os.environ.get("XDG_CONFIG_HOME", str(home / ".config"))
        return Path(xdg) / "Claude/claude_desktop_config.json"
    else:
        raise OSError(f"Unsupported operating system: {system}")


def setup_mcp_config():
    # 1. Resolve data directory: scripts/ lives one level below the plugin root
    plugin_root = Path(__file__).parent.parent.resolve()
    data_folder = plugin_root / "data"
    data_folder.mkdir(parents=True, exist_ok=True)

    print(f"Plugin root : {plugin_root}")
    print(f"Data folder : {data_folder}")
    print()

    # 2. Locate Claude Desktop config
    try:
        config_path = find_claude_config_path()
    except (OSError, EnvironmentError) as e:
        print(f"❌ {e}")
        return

    # 3. Load existing config or start fresh
    config = {"mcpServers": {}}
    if config_path.exists():
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
        except json.JSONDecodeError:
            print("⚠️  Existing config is malformed JSON — will overwrite with a clean config.")
        config.setdefault("mcpServers", {})

    # 4. Check if already configured with the correct path (idempotent)
    existing = config["mcpServers"].get(MCP_SERVER_KEY)
    if existing:
        existing_path = (existing.get("args") or [None])[-1]
        if existing_path == str(data_folder):
            print(f"✅ Already configured. Claude Desktop has access to: {data_folder}")
            print("   No changes made.")
            return
        else:
            print(f"⚠️  Updating data path")
            print(f"   Old path: {existing_path}")
            print(f"   New path: {data_folder}")
            print()

    # 5. Add or update the filesystem MCP server entry
    config["mcpServers"][MCP_SERVER_KEY] = {
        "command": "npx",
        "args": [
            "-y",
            "@modelcontextprotocol/server-filesystem",
            str(data_folder)
        ]
    }

    # 6. Write config back
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    print(f"✅ Success! Claude Desktop can now access: {data_folder}")
    print(f"   Config written to: {config_path}")
    print()
    print("→  Restart Claude Desktop to apply changes.")
    print("→  Then run /career-navigator:setup to finish configuration.")


if __name__ == "__main__":
    setup_mcp_config()
