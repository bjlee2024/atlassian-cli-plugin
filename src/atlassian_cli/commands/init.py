"""Interactive init command — collect credentials and verify connectivity."""

import argparse
import json
import sys

from atlassian_cli.config import save_config, DEFAULT_CONFIG


def _prompt(label: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    val = input(f"{label}{suffix}: ").strip()
    return val or default


def run_init(args: argparse.Namespace) -> None:
    """Run interactive setup wizard."""
    print("=== Atlassian CLI Setup ===\n")
    print("Configure your Atlassian Cloud credentials.")
    print("Get an API token at: https://id.atlassian.com/manage/api-tokens\n")

    config = {**DEFAULT_CONFIG}

    config["url"] = _prompt("Atlassian URL (e.g. https://your-domain.atlassian.net)")
    if not config["url"]:
        print("Error: URL is required.", file=sys.stderr)
        sys.exit(1)

    config["email"] = _prompt("Email address")
    if not config["email"]:
        print("Error: Email is required.", file=sys.stderr)
        sys.exit(1)

    config["api_token"] = _prompt("API token")
    if not config["api_token"]:
        print("Error: API token is required.", file=sys.stderr)
        sys.exit(1)

    config["auth_type"] = _prompt("Auth type", "cloud")

    # Verify connectivity
    print("\nVerifying connection...")
    try:
        from atlassian_cli.auth import get_confluence, get_jira

        # Test Confluence
        confluence = get_confluence(config)
        spaces = confluence.get_all_spaces(limit=1)
        print("  Confluence: OK")

        # Test Jira
        jira = get_jira(config)
        myself = jira.myself()
        display_name = myself.get("displayName", myself.get("name", "unknown"))
        print(f"  Jira: OK (logged in as {display_name})")

    except Exception as exc:
        print(f"\nWarning: Connection test failed: {exc}", file=sys.stderr)
        print("Configuration will be saved anyway. Check your credentials.\n")

    # Optional defaults
    config["default_confluence_space"] = _prompt("Default Confluence space key (optional)")
    config["default_jira_project"] = _prompt("Default Jira project key (optional)")

    # Save
    path = save_config(config)
    print(f"\nConfiguration saved to: {path}")
    print("\nSetup complete! Try:")
    print("  atlassian-cli confluence space list")
    print("  atlassian-cli jira user me")
