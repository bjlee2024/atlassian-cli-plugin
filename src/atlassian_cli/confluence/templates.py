"""Confluence template handlers."""

import sys

from atlassian_cli.auth import get_confluence
from atlassian_cli.formatter import (
    format_output,
    output_error,
    output_markdown_table,
)


def handle_template(args):
    """Route template subcommands."""
    try:
        conf = get_confluence()
    except Exception as exc:
        output_error(f"Failed to connect to Confluence: {exc}")

    cmd = getattr(args, "template_cmd", None)
    fmt = getattr(args, "format", "markdown")

    try:
        if cmd == "list":
            result = conf.get_content_templates()
            templates = result.get("results", result) if isinstance(result, dict) else result
            if fmt == "json":
                from atlassian_cli.formatter import output_json
                output_json(templates)
                return
            headers = ["ID", "Name", "Description"]
            rows = [
                [
                    t.get("templateId", t.get("id", "")),
                    t.get("name", ""),
                    t.get("description", ""),
                ]
                for t in templates
                if isinstance(t, dict)
            ]
            output_markdown_table(headers, rows)

        elif cmd == "get":
            result = conf.get_content_template(args.template_id)
            format_output(result, fmt=fmt)

        else:
            print(f"Unknown template subcommand: {cmd}. Use --help.", file=sys.stderr)
            sys.exit(1)

    except SystemExit:
        raise
    except Exception as exc:
        output_error(str(exc))
