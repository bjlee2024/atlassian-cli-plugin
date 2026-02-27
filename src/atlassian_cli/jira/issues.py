"""Jira issue and user handlers."""

import json
import sys

from atlassian_cli.auth import get_jira
from atlassian_cli.formatter import format_output, output_error, output_success


def handle_issue(args) -> None:
    """Route issue subcommands."""
    try:
        jira = get_jira()
    except Exception as exc:
        output_error(f"Failed to connect to Jira: {exc}")

    cmd = args.issue_cmd
    fmt = getattr(args, "format", "markdown")

    if cmd == "get":
        _issue_get(jira, args, fmt)
    elif cmd == "bulk-get":
        _issue_bulk_get(jira, args, fmt)
    elif cmd == "fields":
        _issue_fields(jira, args, fmt)
    elif cmd == "transitions":
        _issue_transitions(jira, args, fmt)
    elif cmd == "changelog":
        _issue_changelog(jira, args, fmt)
    elif cmd == "subtree":
        _issue_subtree(jira, args, fmt)
    elif cmd == "watchers":
        _issue_watchers(jira, args, fmt)
    elif cmd == "links":
        _issue_links(jira, args, fmt)
    elif cmd == "create":
        _issue_create(jira, args)
    elif cmd == "bulk-create":
        _issue_bulk_create(jira, args)
    elif cmd == "update":
        _issue_update(jira, args)
    elif cmd == "bulk-update":
        _issue_bulk_update(jira, args)
    elif cmd == "delete":
        _issue_delete(jira, args)
    elif cmd == "transition":
        _issue_transition(jira, args)
    elif cmd == "assign":
        _issue_assign(jira, args)
    elif cmd == "label-add":
        _issue_label_add(jira, args)
    elif cmd == "label-remove":
        _issue_label_remove(jira, args)
    elif cmd == "link":
        _issue_link(jira, args)
    elif cmd == "archive":
        _issue_archive(jira, args)
    else:
        print(f"Unknown issue subcommand: {cmd}", file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# Read operations
# ---------------------------------------------------------------------------

def _issue_get(jira, args, fmt: str) -> None:
    fields_arg = getattr(args, "fields", None)
    fields_param = fields_arg if fields_arg else None
    try:
        result = jira.issue(args.key, fields=fields_param)
    except Exception as exc:
        output_error(f"Failed to get issue {args.key}: {exc}")
    format_output(result, fmt=fmt)


def _issue_bulk_get(jira, args, fmt: str) -> None:
    keys = [k.strip() for k in args.keys.split(",") if k.strip()]
    results = []
    for key in keys:
        try:
            issue = jira.issue(key)
            results.append(issue)
        except Exception as exc:
            print(f"Warning: failed to get {key}: {exc}", file=sys.stderr)
    format_output(results, fmt=fmt)


def _issue_fields(jira, args, fmt: str) -> None:
    try:
        result = jira.issue_fields()
    except Exception as exc:
        output_error(f"Failed to get issue fields: {exc}")
    format_output(result, fmt=fmt)


def _issue_transitions(jira, args, fmt: str) -> None:
    try:
        result = jira.get_issue_transitions(args.key)
    except Exception as exc:
        output_error(f"Failed to get transitions for {args.key}: {exc}")
    format_output(result, fmt=fmt)


def _issue_changelog(jira, args, fmt: str) -> None:
    try:
        result = jira.get_issue_changelog(args.key)
    except Exception as exc:
        output_error(f"Failed to get changelog for {args.key}: {exc}")
    format_output(result, fmt=fmt)


def _issue_subtree(jira, args, fmt: str) -> None:
    try:
        result = jira.get_issue_tree_recursive(args.key)
    except Exception as exc:
        output_error(f"Failed to get subtree for {args.key}: {exc}")
    format_output(result, fmt=fmt)


def _issue_watchers(jira, args, fmt: str) -> None:
    try:
        result = jira.issue_get_watchers(args.key)
    except Exception as exc:
        output_error(f"Failed to get watchers for {args.key}: {exc}")
    format_output(result, fmt=fmt)


def _issue_links(jira, args, fmt: str) -> None:
    try:
        issue = jira.issue(args.key)
        links = issue.get("fields", {}).get("issuelinks", [])
    except Exception as exc:
        output_error(f"Failed to get links for {args.key}: {exc}")
    format_output(links, fmt=fmt)


# ---------------------------------------------------------------------------
# Write operations
# ---------------------------------------------------------------------------

def _issue_create(jira, args) -> None:
    fields: dict = {
        "project": {"key": args.project},
        "issuetype": {"name": args.type},
        "summary": args.summary,
        "description": getattr(args, "description", "") or "",
    }

    assignee = getattr(args, "assignee", None)
    if assignee:
        fields["assignee"] = {"accountId": assignee}

    priority = getattr(args, "priority", None)
    if priority:
        fields["priority"] = {"name": priority}

    labels_arg = getattr(args, "labels", None)
    if labels_arg:
        fields["labels"] = [lbl.strip() for lbl in labels_arg.split(",") if lbl.strip()]

    components_arg = getattr(args, "components", None)
    if components_arg:
        fields["components"] = [{"name": c.strip()} for c in components_arg.split(",") if c.strip()]

    parent = getattr(args, "parent", None)
    if parent:
        fields["parent"] = {"key": parent}

    try:
        result = jira.issue_create(fields=fields)
    except Exception as exc:
        output_error(f"Failed to create issue: {exc}")
    output_success(f"Issue created: {result.get('key', result)}")


def _issue_bulk_create(jira, args) -> None:
    try:
        issues_data = json.loads(args.json)
    except json.JSONDecodeError as exc:
        output_error(f"Invalid JSON: {exc}")

    try:
        result = jira.create_issues(issues_data)
    except Exception as exc:
        output_error(f"Failed to bulk-create issues: {exc}")
    output_success(f"Bulk create completed: {result}")


def _issue_update(jira, args) -> None:
    fields_to_update: dict = {}

    summary = getattr(args, "summary", None)
    if summary:
        fields_to_update["summary"] = summary

    description = getattr(args, "description", None)
    if description is not None:
        fields_to_update["description"] = description

    assignee = getattr(args, "assignee", None)
    if assignee:
        fields_to_update["assignee"] = {"accountId": assignee}

    priority = getattr(args, "priority", None)
    if priority:
        fields_to_update["priority"] = {"name": priority}

    labels_arg = getattr(args, "labels", None)
    if labels_arg is not None:
        fields_to_update["labels"] = [lbl.strip() for lbl in labels_arg.split(",") if lbl.strip()]

    if not fields_to_update:
        output_error("No fields specified to update.")

    try:
        jira.issue_update(args.key, fields=fields_to_update)
    except Exception as exc:
        output_error(f"Failed to update {args.key}: {exc}")
    output_success(f"Issue {args.key} updated.")


def _issue_bulk_update(jira, args) -> None:
    keys = [k.strip() for k in args.keys.split(",") if k.strip()]
    field = args.field
    value = args.value
    errors = []

    for key in keys:
        try:
            jira.issue_update(key, fields={field: value})
        except Exception as exc:
            errors.append(f"{key}: {exc}")

    if errors:
        for err in errors:
            print(f"Warning: {err}", file=sys.stderr)
    output_success(f"Bulk update complete for {len(keys)} issue(s).")


def _issue_delete(jira, args) -> None:
    try:
        jira.delete_issue(args.key)
    except Exception as exc:
        output_error(f"Failed to delete {args.key}: {exc}")
    output_success(f"Issue {args.key} deleted.")


def _issue_transition(jira, args) -> None:
    try:
        jira.set_issue_status(args.key, args.status)
    except Exception as exc:
        output_error(f"Failed to transition {args.key} to '{args.status}': {exc}")
    output_success(f"Issue {args.key} transitioned to '{args.status}'.")


def _issue_assign(jira, args) -> None:
    assignee = None if args.assignee.lower() == "unassigned" else args.assignee
    try:
        jira.assign_issue(args.key, assignee)
    except Exception as exc:
        output_error(f"Failed to assign {args.key}: {exc}")
    label = assignee or "unassigned"
    output_success(f"Issue {args.key} assigned to {label}.")


def _issue_label_add(jira, args) -> None:
    try:
        issue = jira.issue(args.key, fields="labels")
        existing = issue.get("fields", {}).get("labels", [])
        if args.label not in existing:
            updated = existing + [args.label]
            jira.issue_update(args.key, fields={"labels": updated})
    except Exception as exc:
        output_error(f"Failed to add label to {args.key}: {exc}")
    output_success(f"Label '{args.label}' added to {args.key}.")


def _issue_label_remove(jira, args) -> None:
    try:
        issue = jira.issue(args.key, fields="labels")
        existing = issue.get("fields", {}).get("labels", [])
        updated = [lbl for lbl in existing if lbl != args.label]
        jira.issue_update(args.key, fields={"labels": updated})
    except Exception as exc:
        output_error(f"Failed to remove label from {args.key}: {exc}")
    output_success(f"Label '{args.label}' removed from {args.key}.")


def _issue_link(jira, args) -> None:
    link_type = getattr(args, "type", "Relates")
    try:
        jira.create_issue_link(link_type, args.key1, args.key2)
    except Exception as exc:
        output_error(f"Failed to link {args.key1} -> {args.key2}: {exc}")
    output_success(f"Linked {args.key1} -> {args.key2} as '{link_type}'.")


def _issue_archive(jira, args) -> None:
    try:
        jira.issue_archive(args.key)
    except Exception as exc:
        output_error(f"Failed to archive {args.key}: {exc}")
    output_success(f"Issue {args.key} archived.")


# ---------------------------------------------------------------------------
# User handler
# ---------------------------------------------------------------------------

def handle_user(args) -> None:
    """Route user subcommands."""
    try:
        jira = get_jira()
    except Exception as exc:
        output_error(f"Failed to connect to Jira: {exc}")

    cmd = args.user_cmd
    fmt = getattr(args, "format", "markdown")

    if cmd == "me":
        try:
            result = jira.myself()
        except Exception as exc:
            output_error(f"Failed to get current user: {exc}")
        format_output(result, fmt=fmt)

    elif cmd == "get":
        try:
            result = jira.user(args.user_id)
        except Exception as exc:
            output_error(f"Failed to get user {args.user_id}: {exc}")
        format_output(result, fmt=fmt)

    elif cmd == "search":
        try:
            result = jira.user_find_by_user_string(args.query)
        except Exception as exc:
            output_error(f"Failed to search users: {exc}")
        format_output(result, fmt=fmt)

    else:
        print(f"Unknown user subcommand: {cmd}", file=sys.stderr)
        sys.exit(1)
