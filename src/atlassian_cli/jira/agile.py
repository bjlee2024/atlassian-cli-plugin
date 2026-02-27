"""Jira agile handlers: boards, sprints, epics."""

import sys

from atlassian_cli.auth import get_jira
from atlassian_cli.formatter import format_output, output_error, output_success


def handle_board(args) -> None:
    """Route board subcommands."""
    try:
        jira = get_jira()
    except Exception as exc:
        output_error(f"Failed to connect to Jira: {exc}")

    cmd = args.board_cmd
    fmt = getattr(args, "format", "markdown")

    if cmd == "list":
        try:
            result = jira.get_all_agile_boards()
        except Exception as exc:
            try:
                result = jira.boards()
            except Exception as exc2:
                output_error(f"Failed to list boards: {exc2}")
        boards = result.get("values", result) if isinstance(result, dict) else result
        format_output(boards, fmt=fmt)

    elif cmd == "get":
        try:
            result = jira.get_agile_board(args.board_id)
        except Exception as exc:
            output_error(f"Failed to get board {args.board_id}: {exc}")
        format_output(result, fmt=fmt)

    elif cmd == "issues":
        try:
            result = jira.get_issues_for_board(args.board_id)
        except Exception as exc:
            output_error(f"Failed to get issues for board {args.board_id}: {exc}")
        issues = result.get("issues", result) if isinstance(result, dict) else result
        format_output(issues, fmt=fmt)

    elif cmd == "config":
        try:
            result = jira.get_agile_board_configuration(args.board_id)
        except Exception as exc:
            output_error(f"Failed to get config for board {args.board_id}: {exc}")
        format_output(result, fmt=fmt)

    else:
        print(f"Unknown board subcommand: {cmd}", file=sys.stderr)
        sys.exit(1)


def handle_sprint(args) -> None:
    """Route sprint subcommands."""
    try:
        jira = get_jira()
    except Exception as exc:
        output_error(f"Failed to connect to Jira: {exc}")

    cmd = args.sprint_cmd
    fmt = getattr(args, "format", "markdown")

    if cmd == "list":
        try:
            result = jira.get_all_sprints_from_board(args.board_id)
        except Exception as exc:
            output_error(f"Failed to list sprints for board {args.board_id}: {exc}")
        sprints = result.get("values", result) if isinstance(result, dict) else result
        format_output(sprints, fmt=fmt)

    elif cmd == "create":
        start = getattr(args, "start", None)
        end = getattr(args, "end", None)
        try:
            result = jira.create_sprint(args.name, args.board, start, end)
        except Exception as exc:
            output_error(f"Failed to create sprint: {exc}")
        output_success(f"Sprint created: {result.get('id', result)}")

    elif cmd == "add-issues":
        keys = [k.strip() for k in args.keys.split(",") if k.strip()]
        try:
            jira.add_issues_to_sprint(args.sprint_id, keys)
        except Exception as exc:
            output_error(f"Failed to add issues to sprint {args.sprint_id}: {exc}")
        output_success(f"Added {len(keys)} issue(s) to sprint {args.sprint_id}.")

    elif cmd == "rename":
        try:
            jira.rename_sprint(args.sprint_id, args.name)
        except Exception as exc:
            output_error(f"Failed to rename sprint {args.sprint_id}: {exc}")
        output_success(f"Sprint {args.sprint_id} renamed to '{args.name}'.")

    else:
        print(f"Unknown sprint subcommand: {cmd}", file=sys.stderr)
        sys.exit(1)


def handle_epic(args) -> None:
    """Route epic subcommands."""
    try:
        jira = get_jira()
    except Exception as exc:
        output_error(f"Failed to connect to Jira: {exc}")

    cmd = args.epic_cmd
    fmt = getattr(args, "format", "markdown")

    if cmd == "list":
        try:
            result = jira.get_epics(args.board_id)
        except Exception as exc:
            output_error(f"Failed to list epics for board {args.board_id}: {exc}")
        epics = result.get("values", result) if isinstance(result, dict) else result
        format_output(epics, fmt=fmt)

    elif cmd == "issues":
        try:
            result = jira.epic_issues(args.epic_key)
        except Exception as exc:
            output_error(f"Failed to get issues for epic {args.epic_key}: {exc}")
        issues = result.get("issues", result) if isinstance(result, dict) else result
        format_output(issues, fmt=fmt)

    else:
        print(f"Unknown epic subcommand: {cmd}", file=sys.stderr)
        sys.exit(1)
