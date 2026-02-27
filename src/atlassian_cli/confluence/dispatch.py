"""Confluence command dispatcher — routes parsed args to handler functions."""

import argparse
import sys


def run(args: argparse.Namespace) -> None:
    """Dispatch confluence subcommands."""
    cmd = args.confluence_cmd

    if cmd == "page":
        from atlassian_cli.confluence.pages import handle_page
        handle_page(args)
    elif cmd == "search":
        from atlassian_cli.confluence.search import handle_search
        handle_search(args)
    elif cmd == "tables":
        from atlassian_cli.confluence.search import handle_tables
        handle_tables(args)
    elif cmd == "space":
        from atlassian_cli.confluence.spaces import handle_space
        handle_space(args)
    elif cmd == "attachment":
        from atlassian_cli.confluence.attachments import handle_attachment
        handle_attachment(args)
    elif cmd == "template":
        from atlassian_cli.confluence.templates import handle_template
        handle_template(args)
    elif cmd == "export":
        from atlassian_cli.confluence.pages import handle_export
        handle_export(args)
    elif cmd == "user":
        from atlassian_cli.confluence.pages import handle_user
        handle_user(args)
    elif cmd == "group":
        from atlassian_cli.confluence.pages import handle_group
        handle_group(args)
    else:
        print("Unknown confluence command. Use --help.", file=sys.stderr)
        sys.exit(1)
