#!/usr/bin/env python3
"""
Career Navigator — One-time initialization script.

Registers the filesystem MCP server in Claude Desktop's configuration,
giving Career Navigator read/write access to your job search directory.
Also saves the directory path to ~/Library/Application Support/Claude/cowork_plugins/career-navigator/config.json for use by hooks.

Usage:
    python3 scripts/init.py /path/to/your/job-search-folder
    python3 scripts/init.py          # re-registers the previously saved path

Run once after providing your job search directory. Then restart Claude Desktop
and run /career-navigator:setup to finish configuration.
"""

import os
import sys
import json
import platform
from pathlib import Path

MCP_SERVER_KEY = "career-navigator"


def get_career_nav_config_path():
    """Return the platform-specific path to Career Navigator's config.json."""
    home = Path.home()
    system = platform.system()
    if system == "Darwin":
        return home / "Library/Application Support/Claude/cowork_plugins/career-navigator/config.json"
    elif system == "Windows":
        appdata = os.environ.get("APPDATA", str(home / "AppData/Roaming"))
        return Path(appdata) / "Claude/cowork_plugins/career-navigator/config.json"
    else:  # Linux
        xdg = os.environ.get("XDG_CONFIG_HOME", str(home / ".config"))
        return Path(xdg) / "Claude/cowork_plugins/career-navigator/config.json"


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


def get_user_dir(career_nav_config):
    """Resolve the job search directory from args, saved config, or prompt."""
    if len(sys.argv) > 1:
        return Path(sys.argv[1]).expanduser().resolve()

    if career_nav_config.exists():
        try:
            saved = json.loads(career_nav_config.read_text())
            stored = saved.get("user_dir", "").strip()
            if stored:
                print(f"Using previously configured directory: {stored}")
                return Path(stored)
        except (json.JSONDecodeError, KeyError):
            pass

    # Interactive fallback
    path_str = input("Enter the path to your job search folder: ").strip()
    if not path_str:
        print("❌ No path provided.")
        sys.exit(1)
    return Path(path_str).expanduser().resolve()


def setup_mcp_config():
    career_nav_config = get_career_nav_config_path()

    # 1. Resolve and create the user's job search directory
    user_dir = get_user_dir(career_nav_config)
    user_dir.mkdir(parents=True, exist_ok=True)

    print(f"Job search directory: {user_dir}")
    print()

    # 2. Save to Career Navigator config dir (accessible to hooks without MCP)
    career_nav_config.parent.mkdir(parents=True, exist_ok=True)
    existing_config = {}
    if career_nav_config.exists():
        try:
            existing_config = json.loads(career_nav_config.read_text())
        except json.JSONDecodeError:
            pass
    existing_config["user_dir"] = str(user_dir)
    career_nav_config.write_text(json.dumps(existing_config, indent=2))

    # 3. Locate Claude Desktop config
    try:
        config_path = find_claude_config_path()
    except (OSError, EnvironmentError) as e:
        print(f"❌ {e}")
        return

    # 4. Load existing config or start fresh
    config = {"mcpServers": {}}
    if config_path.exists():
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
        except json.JSONDecodeError:
            print("⚠️  Existing config is malformed JSON — will overwrite.")
        config.setdefault("mcpServers", {})

    # 5. Check if already configured with the correct path (idempotent)
    existing = config["mcpServers"].get(MCP_SERVER_KEY)
    if existing:
        existing_path = (existing.get("args") or [None])[-1]
        if existing_path == str(user_dir):
            print(f"✅ Already configured. Claude has access to: {user_dir}")
            print("   No changes made.")
            return
        else:
            print(f"⚠️  Updating path")
            print(f"   Old: {existing_path}")
            print(f"   New: {user_dir}")
            print()

    # 6. Register the filesystem MCP server pointing to the user's directory
    config["mcpServers"][MCP_SERVER_KEY] = {
        "command": "npx",
        "args": [
            "-y",
            "@modelcontextprotocol/server-filesystem",
            str(user_dir)
        ]
    }

    # 7. Write config back
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    print(f"✅ Success! Claude Desktop can now access: {user_dir}")
    print(f"   Config written to: {config_path}")
    print()
    print("→  Restart Claude Desktop to apply changes.")
    print("→  Then run /career-navigator:setup to finish configuration.")


if __name__ == "__main__":
    setup_mcp_config()
