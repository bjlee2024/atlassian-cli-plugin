"""Cross-service workflows — Confluence ↔ Jira integration."""

import argparse
import json
from datetime import datetime

from atlassian_cli.auth import get_confluence, get_jira
from atlassian_cli.formatter import format_output, output_error, output_success


def handle_cross(args: argparse.Namespace) -> None:
    cmd = args.cross_cmd

    if cmd == "sprint-report":
        _sprint_report(args)
    elif cmd == "issue-to-doc":
        _issue_to_doc(args)
    elif cmd == "link-page-to-issue":
        _link_page_to_issue(args)
    elif cmd == "project-status":
        _project_status(args)
    elif cmd == "release-notes":
        _release_notes(args)
    else:
        output_error(f"Unknown cross command: {cmd}")


def _sprint_report(args: argparse.Namespace) -> None:
    """Generate sprint report in Confluence from Jira sprint data."""
    try:
        jira = get_jira()
        conf = get_confluence()

        sprint_id = args.sprint
        board_id = args.board
        space = args.space
        parent_id = getattr(args, "parent_page", None)

        # Get sprint info
        sprints = jira.get_all_sprints_from_board(board_id)
        sprint_info = None
        for s in sprints.get("values", sprints if isinstance(sprints, list) else []):
            if s.get("id") == sprint_id:
                sprint_info = s
                break

        sprint_name = sprint_info.get("name", f"Sprint {sprint_id}") if sprint_info else f"Sprint {sprint_id}"

        # Get sprint issues via JQL
        jql = f"sprint = {sprint_id} ORDER BY status ASC, priority DESC"
        issues = jira.jql(jql, limit=200)
        issue_list = issues.get("issues", [])

        # Build report body
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        body = f"<p><em>Generated: {now}</em></p>"
        body += f"<h2>Sprint: {sprint_name}</h2>"
        body += f"<p>Total issues: {len(issue_list)}</p>"

        # Group by status
        by_status: dict[str, list] = {}
        for issue in issue_list:
            fields = issue.get("fields", {})
            status = fields.get("status", {}).get("name", "Unknown")
            by_status.setdefault(status, []).append(issue)

        for status, items in sorted(by_status.items()):
            body += f"<h3>{status} ({len(items)})</h3>"
            body += "<table><tr><th>Key</th><th>Summary</th><th>Assignee</th><th>Priority</th></tr>"
            for issue in items:
                fields = issue.get("fields", {})
                key = issue.get("key", "")
                summary = fields.get("summary", "")
                assignee = fields.get("assignee", {})
                assignee_name = assignee.get("displayName", "Unassigned") if assignee else "Unassigned"
                priority = fields.get("priority", {})
                priority_name = priority.get("name", "") if priority else ""
                body += f"<tr><td>{key}</td><td>{summary}</td><td>{assignee_name}</td><td>{priority_name}</td></tr>"
            body += "</table>"

        # Create or update Confluence page
        title = f"Sprint Report - {sprint_name}"
        result = conf.update_or_create(
            parent_id=parent_id,
            title=title,
            body=body,
            representation="storage",
            space=space,
        )
        page_id = result.get("id", "unknown")
        output_success(f"Sprint report created/updated: {title} (page ID: {page_id})")

    except Exception as exc:
        output_error(f"Sprint report failed: {exc}")


def _issue_to_doc(args: argparse.Namespace) -> None:
    """Convert Jira issues to a Confluence documentation page."""
    try:
        jira = get_jira()
        conf = get_confluence()

        jql = args.jql
        space = args.space
        page_title = args.page_title

        issues = jira.jql(jql, limit=500)
        issue_list = issues.get("issues", [])

        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        body = f"<p><em>Generated from JQL: <code>{jql}</code> on {now}</em></p>"
        body += f"<p>Total: {len(issue_list)} issues</p>"

        body += "<table><tr><th>Key</th><th>Type</th><th>Summary</th><th>Status</th><th>Assignee</th></tr>"
        for issue in issue_list:
            fields = issue.get("fields", {})
            key = issue.get("key", "")
            issue_type = fields.get("issuetype", {}).get("name", "")
            summary = fields.get("summary", "")
            status = fields.get("status", {}).get("name", "")
            assignee = fields.get("assignee", {})
            assignee_name = assignee.get("displayName", "Unassigned") if assignee else "Unassigned"
            body += f"<tr><td>{key}</td><td>{issue_type}</td><td>{summary}</td><td>{status}</td><td>{assignee_name}</td></tr>"
        body += "</table>"

        result = conf.update_or_create(
            parent_id=None,
            title=page_title,
            body=body,
            representation="storage",
            space=space,
        )
        page_id = result.get("id", "unknown")
        output_success(f"Documentation page created/updated: {page_title} (page ID: {page_id})")

    except Exception as exc:
        output_error(f"Issue-to-doc failed: {exc}")


def _link_page_to_issue(args: argparse.Namespace) -> None:
    """Create a remote link between a Confluence page and Jira issue."""
    try:
        jira = get_jira()
        conf = get_confluence()

        page_id = args.page
        issue_key = args.issue

        # Get page info for the link title
        page = conf.get_page_by_id(page_id, expand="version")
        page_title = page.get("title", f"Page {page_id}")
        page_url = page.get("_links", {}).get("base", "") + page.get("_links", {}).get("webui", "")

        # Create remote link on the Jira issue
        link_data = {
            "object": {
                "url": page_url,
                "title": f"Confluence: {page_title}",
            }
        }
        jira.create_or_update_issue_remote_links(issue_key, link_data)
        output_success(f"Linked Confluence page '{page_title}' to Jira issue {issue_key}")

    except Exception as exc:
        output_error(f"Link failed: {exc}")


def _project_status(args: argparse.Namespace) -> None:
    """Generate project status dashboard in Confluence."""
    try:
        jira = get_jira()
        conf = get_confluence()

        project_key = args.project
        space = args.space

        # Get project info
        project = jira.project(project_key)
        project_name = project.get("name", project_key)

        # Get issue counts by status
        jql_base = f"project = {project_key} AND resolution = Unresolved"
        all_issues = jira.jql(jql_base, limit=0)
        total = all_issues.get("total", 0)

        statuses = ["To Do", "In Progress", "In Review", "Done"]
        status_counts = {}
        for status in statuses:
            result = jira.jql(f"project = {project_key} AND status = '{status}'", limit=0)
            count = result.get("total", 0)
            if count > 0:
                status_counts[status] = count

        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        body = f"<p><em>Updated: {now}</em></p>"
        body += f"<h2>Project: {project_name} ({project_key})</h2>"
        body += f"<p>Open issues: {total}</p>"

        body += "<h3>Status Breakdown</h3>"
        body += "<table><tr><th>Status</th><th>Count</th></tr>"
        for status, count in sorted(status_counts.items()):
            body += f"<tr><td>{status}</td><td>{count}</td></tr>"
        body += "</table>"

        # Recent activity
        recent_jql = f"project = {project_key} AND updated >= -7d ORDER BY updated DESC"
        recent = jira.jql(recent_jql, limit=10)
        recent_issues = recent.get("issues", [])

        if recent_issues:
            body += "<h3>Recent Activity (7 days)</h3>"
            body += "<table><tr><th>Key</th><th>Summary</th><th>Status</th><th>Updated</th></tr>"
            for issue in recent_issues:
                fields = issue.get("fields", {})
                key = issue.get("key", "")
                summary = fields.get("summary", "")
                status = fields.get("status", {}).get("name", "")
                updated = fields.get("updated", "")[:10]
                body += f"<tr><td>{key}</td><td>{summary}</td><td>{status}</td><td>{updated}</td></tr>"
            body += "</table>"

        title = f"Project Status - {project_name}"
        result = conf.update_or_create(
            parent_id=None,
            title=title,
            body=body,
            representation="storage",
            space=space,
        )
        page_id = result.get("id", "unknown")
        output_success(f"Project status page created/updated: {title} (page ID: {page_id})")

    except Exception as exc:
        output_error(f"Project status failed: {exc}")


def _release_notes(args: argparse.Namespace) -> None:
    """Generate release notes in Confluence from Jira version."""
    try:
        jira = get_jira()
        conf = get_confluence()

        project_key = args.project
        version_name = args.version
        space = args.space

        # Get issues for this version
        jql = f"project = {project_key} AND fixVersion = '{version_name}' ORDER BY issuetype ASC, priority DESC"
        issues = jira.jql(jql, limit=500)
        issue_list = issues.get("issues", [])

        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        body = f"<p><em>Generated: {now}</em></p>"
        body += f"<h2>Release: {project_key} v{version_name}</h2>"
        body += f"<p>Total issues: {len(issue_list)}</p>"

        # Group by issue type
        by_type: dict[str, list] = {}
        for issue in issue_list:
            fields = issue.get("fields", {})
            issue_type = fields.get("issuetype", {}).get("name", "Other")
            by_type.setdefault(issue_type, []).append(issue)

        type_icons = {"Bug": "Bug Fixes", "Story": "New Features", "Task": "Tasks", "Epic": "Epics"}

        for issue_type, items in sorted(by_type.items()):
            section_title = type_icons.get(issue_type, issue_type)
            body += f"<h3>{section_title} ({len(items)})</h3><ul>"
            for issue in items:
                key = issue.get("key", "")
                summary = issue.get("fields", {}).get("summary", "")
                body += f"<li><strong>{key}</strong>: {summary}</li>"
            body += "</ul>"

        title = f"Release Notes - {project_key} v{version_name}"
        result = conf.update_or_create(
            parent_id=None,
            title=title,
            body=body,
            representation="storage",
            space=space,
        )
        page_id = result.get("id", "unknown")
        output_success(f"Release notes created/updated: {title} (page ID: {page_id})")

    except Exception as exc:
        output_error(f"Release notes failed: {exc}")
