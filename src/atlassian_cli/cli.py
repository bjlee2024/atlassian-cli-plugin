"""Main CLI entry point — argparse-based subcommand tree.

Usage:
    atlassian-cli init
    atlassian-cli confluence <subcommand> ...
    atlassian-cli jira <subcommand> ...
    atlassian-cli cross <subcommand> ...
"""

import argparse
import sys

from atlassian_cli import __version__


def _add_format_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--format", "-f",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format (default: markdown)",
    )


# ---------------------------------------------------------------------------
# Init
# ---------------------------------------------------------------------------

def cmd_init(args: argparse.Namespace) -> None:
    from atlassian_cli.commands.init import run_init
    run_init(args)


# ---------------------------------------------------------------------------
# Confluence
# ---------------------------------------------------------------------------

def _build_confluence_parser(subparsers: argparse._SubParsersAction) -> None:
    conf = subparsers.add_parser("confluence", aliases=["conf"], help="Confluence operations")
    conf_sub = conf.add_subparsers(dest="confluence_cmd")

    # -- page --
    page = conf_sub.add_parser("page", help="Page operations")
    page_sub = page.add_subparsers(dest="page_cmd")

    p = page_sub.add_parser("get", help="Get page by ID")
    p.add_argument("page_id", help="Page ID")
    p.add_argument("--expand", default="body.storage,version", help="Fields to expand")
    _add_format_arg(p)

    p = page_sub.add_parser("get-by-title", help="Get page by space and title")
    p.add_argument("space", help="Space key")
    p.add_argument("title", help="Page title")
    _add_format_arg(p)

    p = page_sub.add_parser("exists", help="Check if page exists")
    p.add_argument("space", help="Space key")
    p.add_argument("title", help="Page title")

    p = page_sub.add_parser("children", help="Get child pages")
    p.add_argument("page_id", help="Parent page ID")
    p.add_argument("--type", default="page", choices=["page", "comment", "attachment"])
    _add_format_arg(p)

    p = page_sub.add_parser("ancestors", help="Get page ancestors")
    p.add_argument("page_id", help="Page ID")
    _add_format_arg(p)

    p = page_sub.add_parser("history", help="Get page history")
    p.add_argument("page_id", help="Page ID")
    _add_format_arg(p)

    p = page_sub.add_parser("labels", help="Get page labels")
    p.add_argument("page_id", help="Page ID")
    _add_format_arg(p)

    p = page_sub.add_parser("properties", help="Get page properties")
    p.add_argument("page_id", help="Page ID")
    _add_format_arg(p)

    p = page_sub.add_parser("restrictions", help="Get page restrictions")
    p.add_argument("page_id", help="Page ID")
    _add_format_arg(p)

    # page write commands
    p = page_sub.add_parser("create", help="Create a page")
    p.add_argument("--space", required=True, help="Space key")
    p.add_argument("--title", required=True, help="Page title")
    p.add_argument("--body", default="", help="Page body (storage format)")
    p.add_argument("--parent-id", help="Parent page ID")
    _add_format_arg(p)

    p = page_sub.add_parser("update", help="Update a page")
    p.add_argument("page_id", help="Page ID")
    p.add_argument("--title", help="New title")
    p.add_argument("--body", help="New body (storage format)")
    _add_format_arg(p)

    p = page_sub.add_parser("upsert", help="Create or update page")
    p.add_argument("--space", required=True, help="Space key")
    p.add_argument("--title", required=True, help="Page title")
    p.add_argument("--body", default="", help="Page body")
    p.add_argument("--parent-id", help="Parent page ID")
    _add_format_arg(p)

    p = page_sub.add_parser("append", help="Append to page body")
    p.add_argument("page_id", help="Page ID")
    p.add_argument("--body", required=True, help="Content to append")
    _add_format_arg(p)

    p = page_sub.add_parser("delete", help="Delete a page")
    p.add_argument("page_id", help="Page ID")
    p.add_argument("--recursive", action="store_true", help="Delete children too")

    p = page_sub.add_parser("move", help="Move a page")
    p.add_argument("page_id", help="Page ID")
    p.add_argument("--target-id", required=True, help="Target parent page ID")
    p.add_argument("--position", default="append", help="Position (append/prepend)")

    p = page_sub.add_parser("label-add", help="Add label to page")
    p.add_argument("page_id", help="Page ID")
    p.add_argument("label", help="Label name")

    p = page_sub.add_parser("label-remove", help="Remove label from page")
    p.add_argument("page_id", help="Page ID")
    p.add_argument("label", help="Label name")

    p = page_sub.add_parser("property-set", help="Set page property")
    p.add_argument("page_id", help="Page ID")
    p.add_argument("--key", required=True, help="Property key")
    p.add_argument("--value", required=True, help="Property value (JSON)")

    p = page_sub.add_parser("property-delete", help="Delete page property")
    p.add_argument("page_id", help="Page ID")
    p.add_argument("--key", required=True, help="Property key")

    # -- search --
    search = conf_sub.add_parser("search", help="Search Confluence")
    search.add_argument("--cql", help="CQL query")
    search.add_argument("--text", help="Text search (wraps in CQL)")
    search.add_argument("--label", help="Search by label")
    search.add_argument("--space", help="Limit to space")
    search.add_argument("--limit", type=int, default=25, help="Max results")
    _add_format_arg(search)

    p = conf_sub.add_parser("tables", help="Extract tables from page")
    p.add_argument("page_id", help="Page ID")
    _add_format_arg(p)

    # -- space --
    space = conf_sub.add_parser("space", help="Space operations")
    space_sub = space.add_subparsers(dest="space_cmd")

    p = space_sub.add_parser("list", help="List spaces")
    p.add_argument("--limit", type=int, default=50)
    _add_format_arg(p)

    p = space_sub.add_parser("get", help="Get space details")
    p.add_argument("key", help="Space key")
    _add_format_arg(p)

    p = space_sub.add_parser(
        "mine", help="Get the CURRENT authenticated user's OWN personal space")
    _add_format_arg(p)

    p = space_sub.add_parser("content", help="Get space content")
    p.add_argument("key", help="Space key")
    _add_format_arg(p)

    p = space_sub.add_parser("pages", help="Get all pages in space")
    p.add_argument("key", help="Space key")
    p.add_argument("--limit", type=int, default=50)
    _add_format_arg(p)

    p = space_sub.add_parser("permissions", help="Get space permissions")
    p.add_argument("key", help="Space key")
    _add_format_arg(p)

    p = space_sub.add_parser("trash", help="Get trashed content")
    p.add_argument("key", help="Space key")
    _add_format_arg(p)

    # -- attachment --
    att = conf_sub.add_parser("attachment", help="Attachment operations")
    att_sub = att.add_subparsers(dest="attachment_cmd")

    p = att_sub.add_parser("list", help="List attachments")
    p.add_argument("page_id", help="Page ID")
    _add_format_arg(p)

    p = att_sub.add_parser("upload", help="Upload attachment")
    p.add_argument("page_id", help="Page ID")
    p.add_argument("file", help="File path")

    p = att_sub.add_parser("download", help="Download attachments")
    p.add_argument("page_id", help="Page ID")
    p.add_argument("--output-dir", default=".", help="Output directory")

    p = att_sub.add_parser("delete", help="Delete attachment")
    p.add_argument("page_id", help="Page ID")
    p.add_argument("filename", help="Attachment filename")

    # -- template --
    tmpl = conf_sub.add_parser("template", help="Template operations")
    tmpl_sub = tmpl.add_subparsers(dest="template_cmd")

    p = tmpl_sub.add_parser("list", help="List templates")
    _add_format_arg(p)

    p = tmpl_sub.add_parser("get", help="Get template")
    p.add_argument("template_id", help="Template ID")
    _add_format_arg(p)

    # -- export --
    p = conf_sub.add_parser("export", help="Export page to PDF")
    p.add_argument("page_id", help="Page ID")
    p.add_argument("--output", "-o", help="Output file path")

    # -- user / group --
    user = conf_sub.add_parser("user", help="User operations")
    user_sub = user.add_subparsers(dest="user_cmd")

    p = user_sub.add_parser("get", help="Get user details")
    p.add_argument("username", help="Username")
    _add_format_arg(p)

    group = conf_sub.add_parser("group", help="Group operations")
    group_sub = group.add_subparsers(dest="group_cmd")

    p = group_sub.add_parser("list", help="List groups")
    _add_format_arg(p)

    p = group_sub.add_parser("members", help="Get group members")
    p.add_argument("name", help="Group name")
    _add_format_arg(p)


# ---------------------------------------------------------------------------
# Jira
# ---------------------------------------------------------------------------

def _build_jira_parser(subparsers: argparse._SubParsersAction) -> None:
    jira = subparsers.add_parser("jira", help="Jira operations")
    jira_sub = jira.add_subparsers(dest="jira_cmd")

    # -- issue --
    issue = jira_sub.add_parser("issue", help="Issue operations")
    issue_sub = issue.add_subparsers(dest="issue_cmd")

    p = issue_sub.add_parser("get", help="Get issue")
    p.add_argument("key", help="Issue key (e.g. PROJ-123)")
    p.add_argument("--fields", help="Comma-separated field names")
    _add_format_arg(p)

    p = issue_sub.add_parser("bulk-get", help="Get multiple issues")
    p.add_argument("keys", help="Comma-separated issue keys")
    _add_format_arg(p)

    p = issue_sub.add_parser("fields", help="Get issue field definitions")
    p.add_argument("key", help="Issue key")
    _add_format_arg(p)

    p = issue_sub.add_parser("transitions", help="Get available transitions")
    p.add_argument("key", help="Issue key")
    _add_format_arg(p)

    p = issue_sub.add_parser("changelog", help="Get issue changelog")
    p.add_argument("key", help="Issue key")
    _add_format_arg(p)

    p = issue_sub.add_parser("subtree", help="Get issue subtree recursively")
    p.add_argument("key", help="Issue key")
    _add_format_arg(p)

    p = issue_sub.add_parser("watchers", help="Get issue watchers")
    p.add_argument("key", help="Issue key")
    _add_format_arg(p)

    p = issue_sub.add_parser("links", help="Get issue links")
    p.add_argument("key", help="Issue key")
    _add_format_arg(p)

    # issue write commands
    p = issue_sub.add_parser("create", help="Create issue")
    p.add_argument("--project", required=True, help="Project key")
    p.add_argument("--type", required=True, help="Issue type (Bug, Task, Story, Epic)")
    p.add_argument("--summary", required=True, help="Summary")
    p.add_argument("--description", default="", help="Description")
    p.add_argument("--assignee", help="Assignee account ID or username")
    p.add_argument("--priority", help="Priority name")
    p.add_argument("--labels", help="Comma-separated labels")
    p.add_argument("--components", help="Comma-separated component names")
    p.add_argument("--parent", help="Parent issue key (for subtasks)")
    _add_format_arg(p)

    p = issue_sub.add_parser("bulk-create", help="Create multiple issues from JSON")
    p.add_argument("--json", required=True, help="JSON array of issue dicts")
    _add_format_arg(p)

    p = issue_sub.add_parser("update", help="Update issue")
    p.add_argument("key", help="Issue key")
    p.add_argument("--summary", help="New summary")
    p.add_argument("--description", help="New description")
    p.add_argument("--assignee", help="New assignee")
    p.add_argument("--priority", help="New priority")
    p.add_argument("--labels", help="New labels (comma-separated)")
    _add_format_arg(p)

    p = issue_sub.add_parser("bulk-update", help="Bulk update field")
    p.add_argument("--keys", required=True, help="Comma-separated issue keys")
    p.add_argument("--field", required=True, help="Field name")
    p.add_argument("--value", required=True, help="New value")

    p = issue_sub.add_parser("delete", help="Delete issue")
    p.add_argument("key", help="Issue key")

    p = issue_sub.add_parser("transition", help="Transition issue status")
    p.add_argument("key", help="Issue key")
    p.add_argument("status", help="Target status name")

    p = issue_sub.add_parser("assign", help="Assign issue")
    p.add_argument("key", help="Issue key")
    p.add_argument("assignee", help="Assignee (account ID or 'unassigned')")

    p = issue_sub.add_parser("label-add", help="Add label to issue")
    p.add_argument("key", help="Issue key")
    p.add_argument("label", help="Label name")

    p = issue_sub.add_parser("label-remove", help="Remove label from issue")
    p.add_argument("key", help="Issue key")
    p.add_argument("label", help="Label name")

    p = issue_sub.add_parser("link", help="Link two issues")
    p.add_argument("key1", help="Source issue key")
    p.add_argument("key2", help="Target issue key")
    p.add_argument("--type", default="Relates", help="Link type")

    p = issue_sub.add_parser("archive", help="Archive issue")
    p.add_argument("key", help="Issue key")

    # -- search --
    search = jira_sub.add_parser("search", help="Search Jira with JQL")
    search.add_argument("--jql", required=True, help="JQL query")
    search.add_argument("--fields", help="Comma-separated fields")
    search.add_argument("--all", action="store_true", help="Fetch all results (paginated)")
    search.add_argument("--limit", type=int, default=50, help="Max results per page")
    _add_format_arg(search)

    # -- project --
    proj = jira_sub.add_parser("project", help="Project operations")
    proj_sub = proj.add_subparsers(dest="project_cmd")

    p = proj_sub.add_parser("list", help="List projects")
    _add_format_arg(p)

    p = proj_sub.add_parser("get", help="Get project details")
    p.add_argument("key", help="Project key")
    _add_format_arg(p)

    p = proj_sub.add_parser("components", help="List project components")
    p.add_argument("key", help="Project key")
    _add_format_arg(p)

    p = proj_sub.add_parser("versions", help="List project versions")
    p.add_argument("key", help="Project key")
    _add_format_arg(p)

    p = proj_sub.add_parser("issues", help="Get all project issues")
    p.add_argument("key", help="Project key")
    p.add_argument("--limit", type=int, default=50)
    _add_format_arg(p)

    p = proj_sub.add_parser("issue-count", help="Get issue count")
    p.add_argument("key", help="Project key")

    p = proj_sub.add_parser("users", help="List assignable users")
    p.add_argument("key", help="Project key")
    _add_format_arg(p)

    # -- board --
    board = jira_sub.add_parser("board", help="Board operations")
    board_sub = board.add_subparsers(dest="board_cmd")

    p = board_sub.add_parser("list", help="List boards")
    _add_format_arg(p)

    p = board_sub.add_parser("get", help="Get board details")
    p.add_argument("board_id", type=int, help="Board ID")
    _add_format_arg(p)

    p = board_sub.add_parser("issues", help="Get board issues")
    p.add_argument("board_id", type=int, help="Board ID")
    _add_format_arg(p)

    p = board_sub.add_parser("config", help="Get board configuration")
    p.add_argument("board_id", type=int, help="Board ID")
    _add_format_arg(p)

    # -- sprint --
    sprint = jira_sub.add_parser("sprint", help="Sprint operations")
    sprint_sub = sprint.add_subparsers(dest="sprint_cmd")

    p = sprint_sub.add_parser("list", help="List sprints for board")
    p.add_argument("board_id", type=int, help="Board ID")
    _add_format_arg(p)

    p = sprint_sub.add_parser("create", help="Create sprint")
    p.add_argument("--board", required=True, type=int, help="Board ID")
    p.add_argument("--name", required=True, help="Sprint name")
    p.add_argument("--start", help="Start date (ISO format)")
    p.add_argument("--end", help="End date (ISO format)")

    p = sprint_sub.add_parser("add-issues", help="Add issues to sprint")
    p.add_argument("sprint_id", type=int, help="Sprint ID")
    p.add_argument("--keys", required=True, help="Comma-separated issue keys")

    p = sprint_sub.add_parser("rename", help="Rename sprint")
    p.add_argument("sprint_id", type=int, help="Sprint ID")
    p.add_argument("--name", required=True, help="New name")

    # -- epic --
    epic = jira_sub.add_parser("epic", help="Epic operations")
    epic_sub = epic.add_subparsers(dest="epic_cmd")

    p = epic_sub.add_parser("list", help="List epics for board")
    p.add_argument("board_id", type=int, help="Board ID")
    _add_format_arg(p)

    p = epic_sub.add_parser("issues", help="Get epic issues")
    p.add_argument("epic_key", help="Epic key")
    _add_format_arg(p)

    # -- comment --
    comment = jira_sub.add_parser("comment", help="Comment operations")
    comment_sub = comment.add_subparsers(dest="comment_cmd")

    p = comment_sub.add_parser("list", help="List comments")
    p.add_argument("key", help="Issue key")
    _add_format_arg(p)

    p = comment_sub.add_parser("get", help="Get comment")
    p.add_argument("key", help="Issue key")
    p.add_argument("comment_id", help="Comment ID")
    _add_format_arg(p)

    p = comment_sub.add_parser("add", help="Add comment")
    p.add_argument("key", help="Issue key")
    p.add_argument("--body", required=True, help="Comment body")

    p = comment_sub.add_parser("edit", help="Edit comment")
    p.add_argument("key", help="Issue key")
    p.add_argument("comment_id", help="Comment ID")
    p.add_argument("--body", required=True, help="New body")

    # -- attachment --
    att = jira_sub.add_parser("attachment", help="Attachment operations")
    att_sub = att.add_subparsers(dest="attachment_cmd")

    p = att_sub.add_parser("list", help="List attachments")
    p.add_argument("key", help="Issue key")
    _add_format_arg(p)

    p = att_sub.add_parser("upload", help="Upload attachment")
    p.add_argument("key", help="Issue key")
    p.add_argument("file", help="File path")

    p = att_sub.add_parser("download", help="Download attachments")
    p.add_argument("key", help="Issue key")
    p.add_argument("--output-dir", default=".", help="Output directory")

    p = att_sub.add_parser("delete", help="Delete attachment")
    p.add_argument("attachment_id", help="Attachment ID")

    # -- worklog --
    wl = jira_sub.add_parser("worklog", help="Worklog operations")
    wl_sub = wl.add_subparsers(dest="worklog_cmd")

    p = wl_sub.add_parser("list", help="List worklogs")
    p.add_argument("key", help="Issue key")
    _add_format_arg(p)

    p = wl_sub.add_parser("add", help="Add worklog")
    p.add_argument("key", help="Issue key")
    p.add_argument("--time", required=True, help="Time spent (e.g., 1h 30m)")
    p.add_argument("--comment", help="Worklog comment")

    # -- user --
    user = jira_sub.add_parser("user", help="User operations")
    user_sub = user.add_subparsers(dest="user_cmd")

    p = user_sub.add_parser("me", help="Get current user")
    _add_format_arg(p)

    p = user_sub.add_parser("get", help="Get user by ID")
    p.add_argument("user_id", help="Account ID")
    _add_format_arg(p)

    p = user_sub.add_parser("search", help="Search users")
    p.add_argument("query", help="Search query")
    _add_format_arg(p)

    # -- filter --
    filt = jira_sub.add_parser("filter", help="Filter operations")
    filt_sub = filt.add_subparsers(dest="filter_cmd")

    p = filt_sub.add_parser("get", help="Get filter")
    p.add_argument("filter_id", help="Filter ID")
    _add_format_arg(p)

    p = filt_sub.add_parser("create", help="Create filter")
    p.add_argument("--name", required=True, help="Filter name")
    p.add_argument("--jql", required=True, help="JQL query")

    p = filt_sub.add_parser("update", help="Update filter")
    p.add_argument("filter_id", help="Filter ID")
    p.add_argument("--name", help="New name")
    p.add_argument("--jql", help="New JQL")

    p = filt_sub.add_parser("delete", help="Delete filter")
    p.add_argument("filter_id", help="Filter ID")

    # -- dashboard --
    dash = jira_sub.add_parser("dashboard", help="Dashboard operations")
    dash_sub = dash.add_subparsers(dest="dashboard_cmd")

    p = dash_sub.add_parser("list", help="List dashboards")
    _add_format_arg(p)

    # -- component --
    comp = jira_sub.add_parser("component", help="Component operations")
    comp_sub = comp.add_subparsers(dest="component_cmd")

    p = comp_sub.add_parser("get", help="Get component")
    p.add_argument("component_id", help="Component ID")
    _add_format_arg(p)

    p = comp_sub.add_parser("create", help="Create component")
    p.add_argument("--project", required=True, help="Project key")
    p.add_argument("--name", required=True, help="Component name")
    p.add_argument("--description", help="Description")
    p.add_argument("--lead", help="Lead account ID")

    # -- version --
    ver = jira_sub.add_parser("version", help="Version operations")
    ver_sub = ver.add_subparsers(dest="version_cmd")

    p = ver_sub.add_parser("list", help="List versions")
    p.add_argument("project", help="Project key")
    _add_format_arg(p)

    p = ver_sub.add_parser("create", help="Create version")
    p.add_argument("--project", required=True, help="Project key")
    p.add_argument("--name", required=True, help="Version name")
    p.add_argument("--description", help="Description")
    p.add_argument("--release-date", help="Release date (YYYY-MM-DD)")


# ---------------------------------------------------------------------------
# Cross-service
# ---------------------------------------------------------------------------

def _build_cross_parser(subparsers: argparse._SubParsersAction) -> None:
    cross = subparsers.add_parser("cross", help="Cross-service workflows")
    cross_sub = cross.add_subparsers(dest="cross_cmd")

    p = cross_sub.add_parser("sprint-report", help="Generate sprint report in Confluence")
    p.add_argument("--board", required=True, type=int, help="Board ID")
    p.add_argument("--sprint", required=True, type=int, help="Sprint ID")
    p.add_argument("--space", required=True, help="Confluence space key")
    p.add_argument("--parent-page", help="Parent page ID")

    p = cross_sub.add_parser("issue-to-doc", help="Convert Jira issues to Confluence doc")
    p.add_argument("--jql", required=True, help="JQL query")
    p.add_argument("--space", required=True, help="Confluence space key")
    p.add_argument("--page-title", required=True, help="Target page title")

    p = cross_sub.add_parser("link-page-to-issue", help="Link Confluence page to Jira issue")
    p.add_argument("--page", required=True, help="Confluence page ID")
    p.add_argument("--issue", required=True, help="Jira issue key")

    p = cross_sub.add_parser("project-status", help="Project status dashboard in Confluence")
    p.add_argument("--project", required=True, help="Jira project key")
    p.add_argument("--space", required=True, help="Confluence space key")

    p = cross_sub.add_parser("release-notes", help="Generate release notes in Confluence")
    p.add_argument("--project", required=True, help="Jira project key")
    p.add_argument("--version", required=True, help="Version name")
    p.add_argument("--space", required=True, help="Confluence space key")


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------

def _dispatch(args: argparse.Namespace) -> None:
    """Route parsed args to the appropriate command handler."""
    service = args.service

    if service == "init":
        cmd_init(args)
        return

    if service in ("confluence", "conf"):
        from atlassian_cli.confluence import dispatch as conf_dispatch
        conf_dispatch.run(args)
        return

    if service == "jira":
        from atlassian_cli.jira import dispatch as jira_dispatch
        jira_dispatch.run(args)
        return

    if service == "cross":
        from atlassian_cli.cross import dispatch as cross_dispatch
        cross_dispatch.run(args)
        return

    print("Use --help for usage information.", file=sys.stderr)
    sys.exit(1)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="atlassian-cli",
        description="Atlassian CLI — Confluence & Jira operations via Python SDK",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    subparsers = parser.add_subparsers(dest="service")

    subparsers.add_parser("init", help="Initialize configuration")

    _build_confluence_parser(subparsers)
    _build_jira_parser(subparsers)
    _build_cross_parser(subparsers)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if not args.service:
        parser.print_help()
        sys.exit(1)

    try:
        _dispatch(args)
    except KeyboardInterrupt:
        sys.exit(130)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
