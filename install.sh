#!/usr/bin/env bash
set -euo pipefail

# Atlassian CLI Plugin installer
# Installs the CLI tool and configures it for use with Claude Code.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== Atlassian CLI Plugin Installer ==="
echo ""

# 1. Check Python
if ! command -v python3 &>/dev/null; then
    echo "Error: python3 is required (>= 3.9). Install it first."
    exit 1
fi

PY_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
PY_MAJOR=$(echo "$PY_VERSION" | cut -d. -f1)
PY_MINOR=$(echo "$PY_VERSION" | cut -d. -f2)

if [ "$PY_MAJOR" -lt 3 ] || { [ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 9 ]; }; then
    echo "Error: Python 3.9+ required, found $PY_VERSION"
    exit 1
fi
echo "✓ Python $PY_VERSION detected"

# 2. Install with uv or pip
if command -v uv &>/dev/null; then
    echo "Installing with uv..."
    cd "$SCRIPT_DIR"
    uv pip install -e . 2>/dev/null || uv pip install -e "$SCRIPT_DIR"
    echo "✓ Installed with uv"
elif command -v pip3 &>/dev/null; then
    echo "Installing with pip..."
    pip3 install -e "$SCRIPT_DIR"
    echo "✓ Installed with pip"
else
    echo "Error: neither uv nor pip3 found. Install one of them first."
    exit 1
fi

# 3. Verify installation
if command -v atlassian-cli &>/dev/null; then
    echo "✓ atlassian-cli command available"
else
    echo "⚠ atlassian-cli not on PATH. You may need to add your Python bin directory to PATH."
    echo "  Try: python3 -m atlassian_cli --version"
fi

# 4. Setup hooks (optional)
if [ -f "$SCRIPT_DIR/hooks/hooks.json" ]; then
    echo ""
    echo "Hooks file available at: $SCRIPT_DIR/hooks/hooks.json"
    echo "To enable constitution hooks, add to your Claude Code settings."
fi

echo ""
echo "=== Installation complete ==="
echo ""
echo "Next steps:"
echo "  1. Run 'atlassian-cli init' to configure credentials"
echo "  2. Or set environment variables: ATLASSIAN_URL, ATLASSIAN_EMAIL, ATLASSIAN_TOKEN"
echo "  3. Test with: atlassian-cli jira user me"
