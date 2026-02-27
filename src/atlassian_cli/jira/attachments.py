"""Jira attachment handler."""

import sys

from atlassian_cli.auth import get_jira
from atlassian_cli.formatter import format_output, output_error, output_success


def handle_attachment(args) -> None:
    """Route attachment subcommands."""
    try:
        jira = get_jira()
    except Exception as exc:
        output_error(f"Failed to connect to Jira: {exc}")

    cmd = args.attachment_cmd
    fmt = getattr(args, "format", "markdown")

    if cmd == "list":
        try:
            result = jira.get_attachments_ids_from_issue(args.key)
        except Exception as exc:
            output_error(f"Failed to list attachments for {args.key}: {exc}")
        format_output(result, fmt=fmt)

    elif cmd == "upload":
        try:
            result = jira.add_attachment(args.key, args.file)
        except Exception as exc:
            output_error(f"Failed to upload attachment to {args.key}: {exc}")
        output_success(f"Attachment uploaded to {args.key}.")

    elif cmd == "download":
        output_dir = getattr(args, "output_dir", ".") or "."
        try:
            jira.download_attachments_from_issue(args.key, path=output_dir)
        except Exception as exc:
            output_error(f"Failed to download attachments from {args.key}: {exc}")
        output_success(f"Attachments from {args.key} downloaded to '{output_dir}'.")

    elif cmd == "delete":
        try:
            jira.remove_attachment(args.attachment_id)
        except Exception as exc:
            output_error(f"Failed to delete attachment {args.attachment_id}: {exc}")
        output_success(f"Attachment {args.attachment_id} deleted.")

    else:
        print(f"Unknown attachment subcommand: {cmd}", file=sys.stderr)
        sys.exit(1)
