"""Jira command dispatcher — routes parsed args to handler functions."""

import argparse
import sys


def run(args: argparse.Namespace) -> None:
    """Dispatch jira subcommands."""
    cmd = args.jira_cmd

    if cmd == "issue":
        from atlassian_cli.jira.issues import handle_issue
        handle_issue(args)
    elif cmd == "search":
        from atlassian_cli.jira.search import handle_search
        handle_search(args)
    elif cmd == "project":
        from atlassian_cli.jira.projects import handle_project
        handle_project(args)
    elif cmd == "board":
        from atlassian_cli.jira.agile import handle_board
        handle_board(args)
    elif cmd == "sprint":
        from atlassian_cli.jira.agile import handle_sprint
        handle_sprint(args)
    elif cmd == "epic":
        from atlassian_cli.jira.agile import handle_epic
        handle_epic(args)
    elif cmd == "comment":
        from atlassian_cli.jira.comments import handle_comment
        handle_comment(args)
    elif cmd == "attachment":
        from atlassian_cli.jira.attachments import handle_attachment
        handle_attachment(args)
    elif cmd == "worklog":
        from atlassian_cli.jira.worklogs import handle_worklog
        handle_worklog(args)
    elif cmd == "user":
        from atlassian_cli.jira.issues import handle_user
        handle_user(args)
    elif cmd == "filter":
        from atlassian_cli.jira.search import handle_filter
        handle_filter(args)
    elif cmd == "dashboard":
        from atlassian_cli.jira.search import handle_dashboard
        handle_dashboard(args)
    elif cmd == "component":
        from atlassian_cli.jira.projects import handle_component
        handle_component(args)
    elif cmd == "version":
        from atlassian_cli.jira.projects import handle_version
        handle_version(args)
    else:
        print("Unknown jira command. Use --help.", file=sys.stderr)
        sys.exit(1)
