"""Cross-service command dispatcher."""

import argparse
import sys


def run(args: argparse.Namespace) -> None:
    """Dispatch cross-service subcommands."""
    cmd = args.cross_cmd

    if cmd in ("sprint-report", "issue-to-doc", "link-page-to-issue", "project-status", "release-notes"):
        from atlassian_cli.cross.workflows import handle_cross
        handle_cross(args)
    else:
        print("Unknown cross command. Use --help.", file=sys.stderr)
        sys.exit(1)
