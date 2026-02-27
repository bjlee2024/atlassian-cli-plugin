"""Jira search, filter, and dashboard handlers."""

import sys

from atlassian_cli.auth import get_jira
from atlassian_cli.formatter import format_output, output_error, output_success


def handle_search(args) -> None:
    """Execute a JQL search and format results."""
    try:
        jira = get_jira()
    except Exception as exc:
        output_error(f"Failed to connect to Jira: {exc}")

    fmt = getattr(args, "format", "markdown")
    jql = args.jql
    limit = getattr(args, "limit", 50)
    fields_arg = getattr(args, "fields", None)
    fields = fields_arg if fields_arg else None
    fetch_all = getattr(args, "all", False)

    try:
        if fetch_all:
            raw = jira.get_all_issues_from_jql(jql, fields=fields)
            issues = list(raw) if not isinstance(raw, list) else raw
        else:
            response = jira.jql(jql, limit=limit, fields=fields)
            issues = response.get("issues", response) if isinstance(response, dict) else response
    except Exception as exc:
        output_error(f"Search failed: {exc}")

    if fmt == "json":
        format_output(issues, fmt=fmt)
        return

    rows = []
    for issue in issues:
        key = issue.get("key", "")
        f = issue.get("fields", {})
        summary = f.get("summary", "")
        status = (f.get("status") or {}).get("name", "")
        assignee_obj = f.get("assignee") or {}
        assignee = assignee_obj.get("displayName", "") if assignee_obj else ""
        priority_obj = f.get("priority") or {}
        priority = priority_obj.get("name", "") if priority_obj else ""
        rows.append({"Key": key, "Summary": summary, "Status": status, "Assignee": assignee, "Priority": priority})

    format_output(rows, fmt=fmt)


def handle_filter(args) -> None:
    """Route filter subcommands."""
    try:
        jira = get_jira()
    except Exception as exc:
        output_error(f"Failed to connect to Jira: {exc}")

    cmd = args.filter_cmd
    fmt = getattr(args, "format", "markdown")

    if cmd == "get":
        try:
            result = jira.get_filter(args.filter_id)
        except Exception as exc:
            output_error(f"Failed to get filter {args.filter_id}: {exc}")
        format_output(result, fmt=fmt)

    elif cmd == "create":
        try:
            result = jira.create_filter(args.name, args.jql)
        except Exception as exc:
            output_error(f"Failed to create filter: {exc}")
        output_success(f"Filter created: {result.get('id', result)}")

    elif cmd == "update":
        name = getattr(args, "name", None)
        jql = getattr(args, "jql", None)
        kwargs: dict = {}
        if name:
            kwargs["name"] = name
        if jql:
            kwargs["jql"] = jql
        try:
            result = jira.update_filter(args.filter_id, **kwargs)
        except Exception as exc:
            output_error(f"Failed to update filter {args.filter_id}: {exc}")
        output_success(f"Filter {args.filter_id} updated.")

    elif cmd == "delete":
        try:
            jira.delete_filter(args.filter_id)
        except Exception as exc:
            output_error(f"Failed to delete filter {args.filter_id}: {exc}")
        output_success(f"Filter {args.filter_id} deleted.")

    else:
        print(f"Unknown filter subcommand: {cmd}", file=sys.stderr)
        sys.exit(1)


def handle_dashboard(args) -> None:
    """List dashboards."""
    try:
        jira = get_jira()
    except Exception as exc:
        output_error(f"Failed to connect to Jira: {exc}")

    fmt = getattr(args, "format", "markdown")
    try:
        result = jira.get_dashboards()
    except Exception as exc:
        output_error(f"Failed to get dashboards: {exc}")
    format_output(result, fmt=fmt)
