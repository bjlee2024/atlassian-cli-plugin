"""Jira worklog handler."""

import sys

from atlassian_cli.auth import get_jira
from atlassian_cli.formatter import format_output, output_error, output_success


def handle_worklog(args) -> None:
    """Route worklog subcommands."""
    try:
        jira = get_jira()
    except Exception as exc:
        output_error(f"Failed to connect to Jira: {exc}")

    cmd = args.worklog_cmd
    fmt = getattr(args, "format", "markdown")

    if cmd == "list":
        try:
            result = jira.issue_get_worklog(args.key)
        except Exception as exc:
            output_error(f"Failed to list worklogs for {args.key}: {exc}")
        worklogs = result.get("worklogs", result) if isinstance(result, dict) else result
        format_output(worklogs, fmt=fmt)

    elif cmd == "add":
        comment = getattr(args, "comment", None) or ""
        try:
            result = jira.issue_worklog(args.key, comment=comment, timeSpent=args.time)
        except Exception as exc:
            output_error(f"Failed to add worklog to {args.key}: {exc}")
        output_success(f"Worklog added to {args.key}: {args.time}")

    else:
        print(f"Unknown worklog subcommand: {cmd}", file=sys.stderr)
        sys.exit(1)
