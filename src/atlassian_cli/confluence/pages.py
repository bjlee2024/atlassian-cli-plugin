"""Confluence page, export, user, and group handlers."""

import json
import sys

from atlassian_cli.auth import get_confluence
from atlassian_cli.formatter import (
    format_output,
    output_error,
    output_json,
    output_markdown_page,
    output_success,
)


def handle_page(args):
    """Route page subcommands."""
    try:
        conf = get_confluence()
    except Exception as exc:
        output_error(f"Failed to connect to Confluence: {exc}")

    cmd = args.page_cmd
    fmt = getattr(args, "format", "markdown")

    try:
        if cmd == "get":
            result = conf.get_page_by_id(args.page_id, expand=args.expand)
            if fmt == "markdown":
                title = result.get("title", "")
                body_storage = result.get("body", {}).get("storage", {}).get("value", "")
                version = result.get("version", {}).get("number", "")
                space_key = result.get("space", {}).get("key", "")
                metadata = {
                    "ID": result.get("id", ""),
                    "Space": space_key,
                    "Version": str(version),
                }
                output_markdown_page(title, body_storage, metadata)
            else:
                output_json(result)

        elif cmd == "get-by-title":
            result = conf.get_page_by_title(args.space, args.title)
            format_output(result, fmt=fmt)

        elif cmd == "exists":
            exists = conf.page_exists(args.space, args.title)
            print(str(exists))

        elif cmd == "children":
            child_type = getattr(args, "type", "page")
            result = conf.get_page_child_by_type(args.page_id, child_type)
            format_output(result, fmt=fmt)

        elif cmd == "ancestors":
            result = conf.get_page_ancestors(args.page_id)
            format_output(result, fmt=fmt)

        elif cmd == "history":
            result = conf.history(args.page_id)
            format_output(result, fmt=fmt)

        elif cmd == "labels":
            result = conf.get_page_labels(args.page_id)
            format_output(result, fmt=fmt)

        elif cmd == "properties":
            result = conf.get_page_properties(args.page_id)
            format_output(result, fmt=fmt)

        elif cmd == "restrictions":
            result = conf.get_all_restrictions_for_content(args.page_id)
            format_output(result, fmt=fmt)

        elif cmd == "create":
            parent_id = getattr(args, "parent_id", None)
            result = conf.create_page(args.space, args.title, args.body, parent_id=parent_id)
            output_success(f"Created page: {result.get('id')} - {result.get('title')}")

        elif cmd == "update":
            page_id = args.page_id
            current = conf.get_page_by_id(page_id, expand="version,body.storage")
            title = getattr(args, "title", None) or current.get("title", "")
            body = getattr(args, "body", None) or current.get("body", {}).get("storage", {}).get("value", "")
            version = current.get("version", {}).get("number", 1)
            result = conf.update_page(page_id, title, body, version=version)
            output_success(f"Updated page: {result.get('id')} - {result.get('title')}")

        elif cmd == "upsert":
            parent_id = getattr(args, "parent_id", None)
            result = conf.update_or_create(
                parent_id=parent_id,
                title=args.title,
                body=args.body,
                representation="storage",
                space=args.space,
            )
            output_success(f"Upserted page: {result.get('id')} - {result.get('title')}")

        elif cmd == "append":
            result = conf.append_page(args.page_id, args.body)
            output_success(f"Appended to page: {result.get('id')}")

        elif cmd == "delete":
            recursive = getattr(args, "recursive", False)
            conf.remove_page(args.page_id, recursive=recursive)
            output_success(f"Deleted page: {args.page_id}")

        elif cmd == "move":
            target_id = getattr(args, "target_id", None)
            position = getattr(args, "position", "append")
            conf.move_page(args.page_id, target_id, position)
            output_success(f"Moved page {args.page_id} to {target_id} ({position})")

        elif cmd == "label-add":
            conf.set_page_label(args.page_id, args.label)
            output_success(f"Added label '{args.label}' to page {args.page_id}")

        elif cmd == "label-remove":
            conf.remove_page_label(args.page_id, args.label)
            output_success(f"Removed label '{args.label}' from page {args.page_id}")

        elif cmd == "property-set":
            value = json.loads(args.value)
            conf.set_page_property(args.page_id, {"key": args.key, "value": value})
            output_success(f"Set property '{args.key}' on page {args.page_id}")

        elif cmd == "property-delete":
            conf.delete_page_property(args.page_id, args.key)
            output_success(f"Deleted property '{args.key}' from page {args.page_id}")

        else:
            print(f"Unknown page subcommand: {cmd}. Use --help.", file=sys.stderr)
            sys.exit(1)

    except SystemExit:
        raise
    except Exception as exc:
        output_error(str(exc))


def handle_export(args):
    """Export a page (e.g. to PDF)."""
    try:
        conf = get_confluence()
    except Exception as exc:
        output_error(f"Failed to connect to Confluence: {exc}")

    try:
        data = conf.export_page(args.page_id)
        output_path = getattr(args, "output", None) or f"page_{args.page_id}.pdf"
        with open(output_path, "wb") as fh:
            fh.write(data)
        output_success(f"Exported page {args.page_id} to {output_path}")
    except SystemExit:
        raise
    except Exception as exc:
        output_error(str(exc))


def handle_user(args):
    """Handle Confluence user subcommands."""
    try:
        conf = get_confluence()
    except Exception as exc:
        output_error(f"Failed to connect to Confluence: {exc}")

    cmd = getattr(args, "user_cmd", None)
    fmt = getattr(args, "format", "markdown")

    try:
        if cmd == "get":
            result = conf.get_user_details_by_username(args.username)
            format_output(result, fmt=fmt)
        else:
            print(f"Unknown user subcommand: {cmd}. Use --help.", file=sys.stderr)
            sys.exit(1)
    except SystemExit:
        raise
    except Exception as exc:
        output_error(str(exc))


def handle_group(args):
    """Handle Confluence group subcommands."""
    try:
        conf = get_confluence()
    except Exception as exc:
        output_error(f"Failed to connect to Confluence: {exc}")

    cmd = getattr(args, "group_cmd", None)
    fmt = getattr(args, "format", "markdown")

    try:
        if cmd == "list":
            result = conf.get_all_groups()
            format_output(result, fmt=fmt)
        elif cmd == "members":
            result = conf.get_group_members(args.name)
            format_output(result, fmt=fmt)
        else:
            print(f"Unknown group subcommand: {cmd}. Use --help.", file=sys.stderr)
            sys.exit(1)
    except SystemExit:
        raise
    except Exception as exc:
        output_error(str(exc))
