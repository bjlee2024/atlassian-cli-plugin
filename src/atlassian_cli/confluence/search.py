"""Confluence search and table extraction handlers."""

import sys

from atlassian_cli.auth import get_confluence
from atlassian_cli.formatter import (
    format_output,
    output_error,
    output_markdown_table,
)


def handle_search(args):
    """Handle Confluence search subcommand."""
    try:
        conf = get_confluence()
    except Exception as exc:
        output_error(f"Failed to connect to Confluence: {exc}")

    fmt = getattr(args, "format", "markdown")
    limit = getattr(args, "limit", 25)
    cql = getattr(args, "cql", None)
    text = getattr(args, "text", None)
    label = getattr(args, "label", None)
    space = getattr(args, "space", None)

    try:
        if cql:
            result = conf.cql(cql, limit=limit)
            results = result.get("results", result) if isinstance(result, dict) else result
        elif text:
            query = f'text ~ "{text}"'
            if space:
                query += f' AND space = "{space}"'
            result = conf.cql(query, limit=limit)
            results = result.get("results", result) if isinstance(result, dict) else result
        elif label:
            results = conf.get_all_pages_by_label(label)
        else:
            print("Provide --cql, --text, or --label for search.", file=sys.stderr)
            sys.exit(1)

        if fmt == "json":
            from atlassian_cli.formatter import output_json
            output_json(results)
            return

        if not results:
            print("*No results*")
            return

        headers = ["ID", "Title", "Space", "Last Modified"]
        rows = []
        for item in results:
            if isinstance(item, dict):
                content = item.get("content", item)
                page_id = content.get("id", item.get("id", ""))
                title = content.get("title", item.get("title", ""))
                space_key = (
                    content.get("space", {}).get("key", "")
                    or item.get("resultGlobalContainer", {}).get("title", "")
                )
                last_modified = (
                    content.get("history", {}).get("lastUpdated", {}).get("when", "")
                    or item.get("lastModified", "")
                    or item.get("friendlyLastModified", "")
                )
                rows.append([page_id, title, space_key, last_modified])
        output_markdown_table(headers, rows)

    except SystemExit:
        raise
    except Exception as exc:
        output_error(str(exc))


def handle_tables(args):
    """Extract tables from a Confluence page."""
    try:
        conf = get_confluence()
    except Exception as exc:
        output_error(f"Failed to connect to Confluence: {exc}")

    fmt = getattr(args, "format", "markdown")

    try:
        tables = conf.get_tables_from_page(args.page_id)
        format_output(tables, fmt=fmt)
    except SystemExit:
        raise
    except Exception as exc:
        output_error(str(exc))
