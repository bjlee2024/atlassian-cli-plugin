"""Confluence space handlers."""

import sys

from atlassian_cli.auth import get_confluence
from atlassian_cli.formatter import (
    format_output,
    output_error,
    output_json,
    output_markdown_table,
)


def handle_space(args):
    """Route space subcommands."""
    try:
        conf = get_confluence()
    except Exception as exc:
        output_error(f"Failed to connect to Confluence: {exc}")

    cmd = getattr(args, "space_cmd", None)
    fmt = getattr(args, "format", "markdown")

    try:
        if cmd == "list":
            limit = getattr(args, "limit", 50)
            spaces = conf.get_all_spaces(limit=limit)
            if fmt == "json":
                output_json(spaces)
                return
            results = spaces.get("results", spaces) if isinstance(spaces, dict) else spaces
            headers = ["Key", "Name", "Type"]
            rows = [
                [s.get("key", ""), s.get("name", ""), s.get("type", "")]
                for s in results
                if isinstance(s, dict)
            ]
            output_markdown_table(headers, rows)

        elif cmd == "get":
            result = conf.get_space(args.key)
            format_output(result, fmt=fmt)

        elif cmd == "content":
            result = conf.get_space_content(args.key)
            format_output(result, fmt=fmt)

        elif cmd == "pages":
            limit = getattr(args, "limit", 50)
            result = conf.get_all_pages_from_space(args.key, limit=limit)
            format_output(result, fmt=fmt)

        elif cmd == "permissions":
            result = conf.get_space_permissions(args.key)
            format_output(result, fmt=fmt)

        elif cmd == "trash":
            result = conf.get_trashed_contents_by_space(args.key)
            format_output(result, fmt=fmt)

        else:
            print(f"Unknown space subcommand: {cmd}. Use --help.", file=sys.stderr)
            sys.exit(1)

    except SystemExit:
        raise
    except Exception as exc:
        output_error(str(exc))
