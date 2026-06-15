"""Confluence space handlers."""

import sys

from atlassian_cli.auth import get_confluence
from atlassian_cli.formatter import (
    format_output,
    output_error,
    output_json,
    output_markdown_table,
)


def handle_space(args):
    """Route space subcommands."""
    try:
        conf = get_confluence()
    except Exception as exc:
        output_error(f"Failed to connect to Confluence: {exc}")

    cmd = getattr(args, "space_cmd", None)
    fmt = getattr(args, "format", "markdown")

    try:
        if cmd == "list":
            limit = getattr(args, "limit", 50)
            spaces = conf.get_all_spaces(limit=limit)
            if fmt == "json":
                output_json(spaces)
                return
            results = spaces.get("results", spaces) if isinstance(spaces, dict) else spaces
            headers = ["Key", "Name", "Type"]
            rows = [
                [s.get("key", ""), s.get("name", ""), s.get("type", "")]
                for s in results
                if isinstance(s, dict)
            ]
            output_markdown_table(headers, rows)

        elif cmd == "get":
            result = conf.get_space(args.key)
            format_output(result, fmt=fmt)

        elif cmd == "mine":
            # 현재 인증된 사용자(=요청자)의 본인 개인 스페이스를 결정론적으로 해소.
            # 추측 금지: accountId로 ~키(콜론·하이픈 제거)를 만들어 조회.
            user = conf.get("rest/api/user/current") or {}
            acct = user.get("accountId", "")
            if not acct:
                output_error("could not resolve current user accountId")
                return
            key = "~" + acct.replace(":", "").replace("-", "")
            result = conf.get_space(key)
            format_output(result, fmt=fmt)

        elif cmd == "content":
            result = conf.get_space_content(args.key)
            format_output(result, fmt=fmt)

        elif cmd == "pages":
            limit = getattr(args, "limit", 50)
            result = conf.get_all_pages_from_space(args.key, limit=limit)
            format_output(result, fmt=fmt)

        elif cmd == "permissions":
            result = conf.get_space_permissions(args.key)
            format_output(result, fmt=fmt)

        elif cmd == "trash":
            result = conf.get_trashed_contents_by_space(args.key)
            format_output(result, fmt=fmt)

        else:
            print(f"Unknown space subcommand: {cmd}. Use --help.", file=sys.stderr)
            sys.exit(1)

    except SystemExit:
        raise
    except Exception as exc:
        output_error(str(exc))
