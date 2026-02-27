"""Jira project, component, and version handlers."""

import sys

from atlassian_cli.auth import get_jira
from atlassian_cli.formatter import format_output, output_error, output_success


def handle_project(args) -> None:
    """Route project subcommands."""
    try:
        jira = get_jira()
    except Exception as exc:
        output_error(f"Failed to connect to Jira: {exc}")

    cmd = args.project_cmd
    fmt = getattr(args, "format", "markdown")

    if cmd == "list":
        try:
            result = jira.projects()
        except Exception as exc:
            output_error(f"Failed to list projects: {exc}")
        if fmt == "json":
            format_output(result, fmt=fmt)
            return
        rows = [{"Key": p.get("key", ""), "Name": p.get("name", ""), "Lead": (p.get("lead") or {}).get("displayName", "")} for p in (result or [])]
        format_output(rows, fmt=fmt)

    elif cmd == "get":
        try:
            result = jira.project(args.key)
        except Exception as exc:
            output_error(f"Failed to get project {args.key}: {exc}")
        format_output(result, fmt=fmt)

    elif cmd == "components":
        try:
            result = jira.get_project_components(args.key)
        except Exception as exc:
            output_error(f"Failed to get components for {args.key}: {exc}")
        format_output(result, fmt=fmt)

    elif cmd == "versions":
        try:
            result = jira.get_project_versions(args.key)
        except Exception as exc:
            output_error(f"Failed to get versions for {args.key}: {exc}")
        format_output(result, fmt=fmt)

    elif cmd == "issues":
        limit = getattr(args, "limit", 50)
        try:
            response = jira.jql(f"project = {args.key}", limit=limit)
            issues = response.get("issues", response) if isinstance(response, dict) else response
        except Exception as exc:
            output_error(f"Failed to get issues for {args.key}: {exc}")
        format_output(issues, fmt=fmt)

    elif cmd == "issue-count":
        try:
            count = jira.get_project_issues_count(args.key)
        except Exception as exc:
            output_error(f"Failed to get issue count for {args.key}: {exc}")
        print(f"Issue count for {args.key}: {count}")

    elif cmd == "users":
        try:
            result = jira.get_all_assignable_users_for_project(args.key)
        except Exception as exc:
            output_error(f"Failed to get users for {args.key}: {exc}")
        format_output(result, fmt=fmt)

    else:
        print(f"Unknown project subcommand: {cmd}", file=sys.stderr)
        sys.exit(1)


def handle_component(args) -> None:
    """Route component subcommands."""
    try:
        jira = get_jira()
    except Exception as exc:
        output_error(f"Failed to connect to Jira: {exc}")

    cmd = args.component_cmd
    fmt = getattr(args, "format", "markdown")

    if cmd == "get":
        try:
            result = jira.component(args.component_id)
        except Exception as exc:
            output_error(f"Failed to get component {args.component_id}: {exc}")
        format_output(result, fmt=fmt)

    elif cmd == "create":
        component_data: dict = {
            "name": args.name,
            "project": args.project,
        }
        description = getattr(args, "description", None)
        if description:
            component_data["description"] = description
        lead = getattr(args, "lead", None)
        if lead:
            component_data["leadAccountId"] = lead
        try:
            result = jira.create_component(component_data)
        except Exception as exc:
            output_error(f"Failed to create component: {exc}")
        output_success(f"Component created: {result.get('id', result)}")

    else:
        print(f"Unknown component subcommand: {cmd}", file=sys.stderr)
        sys.exit(1)


def handle_version(args) -> None:
    """Route version subcommands."""
    try:
        jira = get_jira()
    except Exception as exc:
        output_error(f"Failed to connect to Jira: {exc}")

    cmd = args.version_cmd
    fmt = getattr(args, "format", "markdown")

    if cmd == "list":
        try:
            result = jira.get_project_versions(args.project)
        except Exception as exc:
            output_error(f"Failed to list versions for {args.project}: {exc}")
        format_output(result, fmt=fmt)

    elif cmd == "create":
        description = getattr(args, "description", None) or ""
        release_date = getattr(args, "release_date", None) or ""
        try:
            result = jira.add_version(
                args.name,
                args.project,
                description,
                release_date,
            )
        except Exception as exc:
            output_error(f"Failed to create version: {exc}")
        output_success(f"Version created: {result.get('id', result)}")

    else:
        print(f"Unknown version subcommand: {cmd}", file=sys.stderr)
        sys.exit(1)
