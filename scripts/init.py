#!/usr/bin/env python3
"""
Career Navigator — One-time initialization script.

Saves the job search directory path to the Career Navigator config so that
session-start and sync hooks can find it at runtime. Does NOT modify
claude_desktop_config.json — file access uses Claude's built-in tools.

Usage:
    python3 scripts/init.py /path/to/your/job-search-folder
    python3 scripts/init.py          # re-uses the previously saved path

Called automatically by /career-navigator:setup. You should not need to
run this directly.
"""

import os
import sys
import json
import platform
from pathlib import Path


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

    path_str = input("Enter the path to your job search folder: ").strip()
    if not path_str:
        print("No path provided.")
        sys.exit(1)
    return Path(path_str).expanduser().resolve()


def save_config():
    career_nav_config = get_career_nav_config_path()

    user_dir = get_user_dir(career_nav_config)
    user_dir.mkdir(parents=True, exist_ok=True)

    career_nav_config.parent.mkdir(parents=True, exist_ok=True)
    existing_config = {}
    if career_nav_config.exists():
        try:
            existing_config = json.loads(career_nav_config.read_text())
        except json.JSONDecodeError:
            pass

    existing_config["user_dir"] = str(user_dir)
    career_nav_config.write_text(json.dumps(existing_config, indent=2))

    print(f"✅ Job search directory saved: {user_dir}")
    print(f"   Config written to: {career_nav_config}")


if __name__ == "__main__":
    save_config()
