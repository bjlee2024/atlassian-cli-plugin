"""Credential and configuration management.

Supports:
- Global config: ~/.atlassian-cli/config.json
- Project-local config: .atlassian-cli/config.json (overrides global)
- Environment variables: ATLASSIAN_URL, ATLASSIAN_EMAIL, ATLASSIAN_TOKEN (highest priority)
"""

import json
import os
import sys
from pathlib import Path
from typing import Any, Optional


CONFIG_DIR_NAME = ".atlassian-cli"
CONFIG_FILE_NAME = "config.json"

REQUIRED_FIELDS = ("url", "email", "api_token")

DEFAULT_CONFIG = {
    "url": "",
    "email": "",
    "api_token": "",
    "auth_type": "cloud",
    "default_confluence_space": "",
    "default_jira_project": "",
}

ENV_MAP = {
    "url": "ATLASSIAN_URL",
    "email": "ATLASSIAN_EMAIL",
    "api_token": "ATLASSIAN_TOKEN",
}


def _global_config_path() -> Path:
    return Path.home() / CONFIG_DIR_NAME / CONFIG_FILE_NAME


def _local_config_path() -> Path:
    return Path.cwd() / CONFIG_DIR_NAME / CONFIG_FILE_NAME


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        print(f"Warning: failed to read {path}: {exc}", file=sys.stderr)
        return {}


def load_config() -> dict[str, Any]:
    """Load config with priority: env vars > local > global > defaults."""
    config = {**DEFAULT_CONFIG}

    global_cfg = _load_json(_global_config_path())
    config.update({k: v for k, v in global_cfg.items() if v})

    local_cfg = _load_json(_local_config_path())
    config.update({k: v for k, v in local_cfg.items() if v})

    for field, env_var in ENV_MAP.items():
        env_val = os.environ.get(env_var)
        if env_val:
            config[field] = env_val

    return config


def save_config(
    config: dict[str, Any],
    *,
    local: bool = False,
) -> Path:
    """Save config to global or local path. Returns the path written."""
    path = _local_config_path() if local else _global_config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    path.chmod(0o600)
    return path


def validate_config(config: dict[str, Any]) -> Optional[str]:
    """Return an error message if config is incomplete, else None."""
    missing = [f for f in REQUIRED_FIELDS if not config.get(f)]
    if missing:
        return f"Missing required config fields: {', '.join(missing)}. Run 'atlassian-cli init' to configure."
    return None


def get_validated_config() -> dict[str, Any]:
    """Load and validate config. Exits with code 2 on auth failure."""
    config = load_config()
    error = validate_config(config)
    if error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(2)
    return config
