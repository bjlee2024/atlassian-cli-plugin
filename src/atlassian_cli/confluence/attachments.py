"""Confluence attachment handlers."""

import sys

from atlassian_cli.auth import get_confluence
from atlassian_cli.formatter import (
    format_output,
    output_error,
    output_markdown_table,
    output_success,
)


def handle_attachment(args):
    """Route attachment subcommands."""
    try:
        conf = get_confluence()
    except Exception as exc:
        output_error(f"Failed to connect to Confluence: {exc}")

    cmd = getattr(args, "attachment_cmd", None)
    fmt = getattr(args, "format", "markdown")

    try:
        if cmd == "list":
            result = conf.get_attachments_from_content(args.page_id)
            attachments = result.get("results", result) if isinstance(result, dict) else result
            if fmt == "json":
                from atlassian_cli.formatter import output_json
                output_json(attachments)
                return
            headers = ["ID", "Title", "Media Type", "File Size"]
            rows = [
                [
                    a.get("id", ""),
                    a.get("title", ""),
                    a.get("metadata", {}).get("mediaType", ""),
                    str(a.get("extensions", {}).get("fileSize", "")),
                ]
                for a in attachments
                if isinstance(a, dict)
            ]
            output_markdown_table(headers, rows)

        elif cmd == "upload":
            conf.attach_file(args.file, page_id=args.page_id)
            output_success(f"Uploaded '{args.file}' to page {args.page_id}")

        elif cmd == "download":
            output_dir = getattr(args, "output_dir", ".")
            conf.download_attachments_from_page(args.page_id, path=output_dir)
            output_success(f"Downloaded attachments from page {args.page_id} to '{output_dir}'")

        elif cmd == "delete":
            conf.delete_attachment(args.page_id, args.filename)
            output_success(f"Deleted attachment '{args.filename}' from page {args.page_id}")

        else:
            print(f"Unknown attachment subcommand: {cmd}. Use --help.", file=sys.stderr)
            sys.exit(1)

    except SystemExit:
        raise
    except Exception as exc:
        output_error(str(exc))
