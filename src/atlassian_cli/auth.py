"""Authentication helpers — create SDK clients from config."""

from typing import Any

from atlassian import Confluence, Jira

from atlassian_cli.config import get_validated_config


def _base_kwargs(config: dict[str, Any]) -> dict[str, Any]:
    return {
        "url": config["url"],
        "username": config["email"],
        "password": config["api_token"],
        "cloud": config.get("auth_type", "cloud") == "cloud",
    }


def get_confluence(config: dict[str, Any] | None = None) -> Confluence:
    """Return an authenticated Confluence client."""
    cfg = config or get_validated_config()
    return Confluence(**_base_kwargs(cfg))


def get_jira(config: dict[str, Any] | None = None) -> Jira:
    """Return an authenticated Jira client."""
    cfg = config or get_validated_config()
    return Jira(**_base_kwargs(cfg))
