"""MCP server bridge for the Atlassian CLI.

Claude Desktop (and other MCP clients) cannot load Claude Code plugins, skills,
or hooks directly. This module exposes the `atlassian-cli` command surface as an
MCP server so the same Confluence/Jira operations are available inside Claude
Desktop.

It is a thin wrapper: every call shells out to `python -m atlassian_cli ...`,
which guarantees full coverage of all 140+ CLI commands with no per-command
maintenance. Credentials are resolved exactly as the CLI does (env vars >
project-local config > ~/.atlassian-cli/config.json).

Write-operation safety: Claude Code enforces confirmation via hooks, which do
not run in Claude Desktop. To preserve the plugin's "Constitution" (all writes
require explicit confirmation), this server detects write commands and refuses
to execute them unless the caller passes `confirm_write=True`, returning a clear
description of the intended change instead. Claude Desktop's own per-tool
approval UI provides a second layer on top of this.

Run with:  python -m atlassian_cli.mcp_server   (or the `atlassian-cli-mcp` script)
"""

from __future__ import annotations

import os
import re
import subprocess
import sys

from mcp.server.fastmcp import FastMCP

# 질의 로그 계측 (사내 온톨로지 시스템 단계 3) — 없으면 no-op (플러그인 독립성 유지)
import os as _os
import time as _time
_sys_path_extra = _os.environ.get(
    "QUERY_INSTRUMENTATION_DIR",
    _os.path.expanduser("~/workspace/hermes/query-instrumentation"))
if _sys_path_extra not in sys.path:
    sys.path.insert(0, _sys_path_extra)
try:
    from instrument import record as _instr  # type: ignore
except Exception:
    def _instr(*a, **k):  # noqa: ANN
        pass

mcp = FastMCP("atlassian-cli")

# ---------------------------------------------------------------------------
# Write-operation detection — mirrors hooks/hooks.json so Desktop behaves like
# the Claude Code plugin's safety Constitution.
# ---------------------------------------------------------------------------

_CONFLUENCE_WRITE = re.compile(
    r"^(confluence|conf)\s+(page\s+(create|update|upsert|append|delete|move)"
    r"|page\s+label-(add|remove)|page\s+property-(set|delete)"
    r"|attachment\s+(upload|delete)|template\s+(create|delete))"
)

_JIRA_WRITE = re.compile(
    r"^jira\s+(issue\s+(create|bulk-create|update|bulk-update|delete|transition|assign|archive)"
    r"|issue\s+label-(add|remove)|issue\s+link|sprint\s+(create|add-issues|rename)"
    r"|comment\s+(add|edit)|attachment\s+(upload|delete)|worklog\s+add"
    r"|filter\s+(create|update|delete)|component\s+create|version\s+create|backlog\s+add)"
)


def _is_write(args: list[str]) -> bool:
    joined = " ".join(args)
    return bool(_CONFLUENCE_WRITE.search(joined) or _JIRA_WRITE.search(joined))


def _has_format_flag(args: list[str]) -> bool:
    return any(a in ("--format", "-f") for a in args)


# Claude Desktop rejects tool results larger than 1 MB. Stay well under that to
# leave headroom for JSON-RPC framing and multi-byte UTF-8 (Korean/CJK) chars.
MAX_RESULT_BYTES = 800_000


def _too_large_message(result: str, args: list[str]) -> str:
    """Replace an over-limit payload with actionable guidance to narrow it."""
    size = len(result.encode("utf-8"))
    cmd = " ".join(args)

    tips: list[str] = []
    joined = " ".join(args)
    if "search" in args:
        tips.append("Lower --limit (e.g. --limit 10) to fetch fewer results.")
        if joined.startswith("jira"):
            tips.append(
                "Add --fields to return only what you need, e.g. "
                "--fields 'key,summary,status,assignee' — issue objects are huge by default."
            )
            tips.append("Tighten the JQL (add status/date/assignee filters) to match fewer issues.")
        else:
            tips.append("Add --space KEY and more specific --text to match fewer pages.")
            tips.append("Confluence search includes page bodies; narrow the query to reduce them.")
        tips.append("Paginate: if the CLI exposes --start/offset, fetch in pages and combine.")
    elif "get" in args:
        tips.append(
            "A single object is over the limit (likely a large page/issue body). "
            "Use --fields (Jira) or --expand to fetch only the parts you need."
        )
    else:
        tips.append("Reduce the result set with a smaller --limit or more specific filters.")

    preview = result[:1500]
    return (
        f"RESULT TOO LARGE — {size:,} bytes exceeds the {MAX_RESULT_BYTES:,}-byte tool limit.\n"
        f"Command: atlassian-cli {cmd}\n"
        "The full result was NOT returned (truncated JSON would be unparseable). "
        "Re-run with a narrower query:\n"
        + "\n".join(f"  • {t}" for t in tips)
        + "\n\nPreview of the start of the result (truncated, not valid JSON):\n"
        + preview
    )


def _run_cli(args: list[str]) -> str:
    """Invoke the CLI via the current interpreter and format the result."""
    cmd = [sys.executable, "-m", "atlassian_cli", *args]
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
        )
    except subprocess.TimeoutExpired:
        return "ERROR: atlassian-cli timed out after 120s."
    except Exception as exc:  # noqa: BLE001 — surface any spawn failure to the client
        return f"ERROR: failed to run atlassian-cli: {exc}"

    out = proc.stdout.strip()
    err = proc.stderr.strip()

    if proc.returncode == 0:
        return out or "(command succeeded with no output)"

    label = {2: "AUTH FAILURE (exit 2)"}.get(proc.returncode, f"ERROR (exit {proc.returncode})")
    parts = [label]
    if err:
        parts.append(err)
    if out:
        parts.append(out)
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------


@mcp.tool()
def atlassian_cli(args: list[str], confirm_write: bool = False) -> str:
    """Run any atlassian-cli command for Confluence & Jira operations.

    Pass the command as a list of arguments, exactly as you would type after
    `atlassian-cli` on the command line. JSON output is requested automatically
    unless you include your own --format flag.

    Examples:
      args=["jira", "issue", "get", "PROJ-123"]
      args=["confluence", "search", "--text", "release notes", "--space", "ENG"]
      args=["jira", "search", "--jql", "project = PROJ AND status = Open"]
      args=["confluence", "page", "create", "--space", "ENG", "--title", "Notes", "--body", "..."]

    Services: confluence (alias conf), jira, cross, init.
    Use the `atlassian_help` tool to discover available subcommands and options.

    WRITE SAFETY: Commands that modify Atlassian data (page/issue create/update/
    delete, transitions, comments, attachments, labels, sprints, etc.) are
    blocked unless you pass confirm_write=True. When blocked, this returns a
    description of the intended change so you can confirm with the user first.

    LARGE RESULTS: tool results over ~800 KB are rejected by the client, so the
    server refuses to return oversized payloads and tells you how to narrow the
    query instead. For searches, prefer a small --limit and (for Jira) --fields,
    e.g. ["jira","search","--jql","...","--limit","10","--fields","key,summary,status"].
    """
    if not args:
        return "ERROR: 'args' is empty. Provide CLI arguments, e.g. ['jira','user','me']."

    if _is_write(args) and not confirm_write:
        _instr("atlassian", "atlassian_cli", 0, False, guard="read-only")
        return (
            "WRITE OPERATION BLOCKED — confirmation required.\n\n"
            f"Command: atlassian-cli {' '.join(args)}\n\n"
            "This command modifies Atlassian data. Confirm with the user what it "
            "does, the target page/space/issue/project, and the risk level. Then "
            "re-call this tool with confirm_write=True to execute."
        )

    call_args = list(args)
    if not _has_format_flag(call_args):
        call_args += ["--format", "json"]

    _t0 = _time.time()
    result = _run_cli(call_args)
    _ok = not result.startswith(("ERROR", "AUTH FAILURE"))
    _instr("atlassian", "atlassian_cli", _time.time() - _t0, _ok)
    if len(result.encode("utf-8")) > MAX_RESULT_BYTES:
        return _too_large_message(result, call_args)
    return result


@mcp.tool()
def atlassian_help(path: list[str] | None = None) -> str:
    """Show atlassian-cli usage to discover commands and options.

    Pass the command path to drill into a subcommand's help.
      path=[]                      -> top-level help (services)
      path=["jira"]                -> jira subcommands
      path=["jira", "issue"]       -> jira issue subcommands
      path=["confluence", "page"]  -> confluence page subcommands
    """
    return _run_cli(list(path or []) + ["--help"])


def _serve(argv=None):
    """전송 선택: 기본 stdio, --http면 streamable-http(host/port 설정)."""
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--http", action="store_true")
    ap.add_argument("--host", default=os.environ.get("MCP_HTTP_HOST", "127.0.0.1"))
    ap.add_argument("--port", type=int, default=None)
    args = ap.parse_args(argv)
    if args.http:
        from auth import serve_http
        serve_http(mcp, args.host, args.port)
    else:
        mcp.run()


def main() -> None:
    _serve()


if __name__ == "__main__":
    main()
