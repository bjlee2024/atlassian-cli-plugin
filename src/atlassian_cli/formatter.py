"""Output formatting for AI-optimized consumption.

Supports markdown (default) and json output modes.
All output goes to stdout; errors to stderr.
"""

import json
import sys
from typing import Any


def output_json(data: Any) -> None:
    """Print data as formatted JSON to stdout."""
    print(json.dumps(data, indent=2, ensure_ascii=False, default=str))


def output_markdown_table(headers: list[str], rows: list[list[str]]) -> None:
    """Print a markdown table."""
    if not rows:
        print("*No results*")
        return
    print("| " + " | ".join(headers) + " |")
    print("| " + " | ".join("---" for _ in headers) + " |")
    for row in rows:
        escaped = [str(c).replace("|", "\\|").replace("\n", " ") for c in row]
        print("| " + " | ".join(escaped) + " |")


def output_markdown_page(title: str, body: str, metadata: dict[str, str] | None = None) -> None:
    """Print page-like content in markdown."""
    print(f"# {title}\n")
    if metadata:
        for key, val in metadata.items():
            print(f"- **{key}**: {val}")
        print()
    print(body)


def output_markdown_list(items: list[dict[str, Any]], key_field: str, value_field: str) -> None:
    """Print a list of items as markdown bullet points."""
    if not items:
        print("*No results*")
        return
    for item in items:
        key = item.get(key_field, "unknown")
        val = item.get(value_field, "")
        print(f"- **{key}**: {val}")


def output_error(message: str, exit_code: int = 1) -> None:
    """Print error to stderr and exit."""
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(exit_code)


def output_success(message: str) -> None:
    """Print a success message."""
    print(f"OK: {message}")


def truncate(text: str, max_length: int = 200) -> str:
    """Truncate text with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def format_output(data: Any, *, fmt: str = "markdown") -> None:
    """Route output to the appropriate formatter.

    For structured data (list of dicts), auto-formats as markdown table.
    For other types, falls back to json.
    """
    if fmt == "json":
        output_json(data)
        return

    if isinstance(data, list) and data and isinstance(data[0], dict):
        headers = list(data[0].keys())
        rows = [[str(item.get(h, "")) for h in headers] for item in data]
        output_markdown_table(headers, rows)
    elif isinstance(data, dict):
        output_json(data)
    elif isinstance(data, str):
        print(data)
    else:
        output_json(data)
