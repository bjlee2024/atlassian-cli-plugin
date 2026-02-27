"""Jira comment handler."""

import sys

from atlassian_cli.auth import get_jira
from atlassian_cli.formatter import format_output, output_error, output_success


def handle_comment(args) -> None:
    """Route comment subcommands."""
    try:
        jira = get_jira()
    except Exception as exc:
        output_error(f"Failed to connect to Jira: {exc}")

    cmd = args.comment_cmd
    fmt = getattr(args, "format", "markdown")

    if cmd == "list":
        try:
            result = jira.issue_get_comments(args.key)
        except Exception as exc:
            output_error(f"Failed to list comments for {args.key}: {exc}")
        comments = result.get("comments", result) if isinstance(result, dict) else result
        format_output(comments, fmt=fmt)

    elif cmd == "get":
        try:
            result = jira.issue_get_comment(args.key, args.comment_id)
        except Exception as exc:
            output_error(f"Failed to get comment {args.comment_id} on {args.key}: {exc}")
        format_output(result, fmt=fmt)

    elif cmd == "add":
        try:
            result = jira.issue_add_comment(args.key, args.body)
        except Exception as exc:
            output_error(f"Failed to add comment to {args.key}: {exc}")
        output_success(f"Comment added to {args.key}: id={result.get('id', result)}")

    elif cmd == "edit":
        try:
            result = jira.issue_edit_comment(args.key, args.comment_id, args.body)
        except Exception as exc:
            output_error(f"Failed to edit comment {args.comment_id} on {args.key}: {exc}")
        output_success(f"Comment {args.comment_id} on {args.key} updated.")

    else:
        print(f"Unknown comment subcommand: {cmd}", file=sys.stderr)
        sys.exit(1)
