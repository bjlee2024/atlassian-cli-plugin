"""Enable `python -m atlassian_cli ...` invocation.

This makes the CLI runnable via the same interpreter that imports the package,
which is more robust than relying on the `atlassian-cli` script being on PATH
(important for environments like Claude Desktop that spawn MCP servers with a
minimal PATH).
"""

from atlassian_cli.cli import main

if __name__ == "__main__":
    main()
