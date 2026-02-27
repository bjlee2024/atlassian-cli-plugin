# Atlassian CLI Plugin for Claude Code

A comprehensive Atlassian CLI plugin that provides **60+ Confluence** and **80+ Jira** commands via the `atlassian-python-api` SDK. No external CLI binaries required.

## Features

- **Confluence**: Pages CRUD, CQL search, spaces, attachments, templates, export, user/group operations
- **Jira**: Issues CRUD, JQL search, projects, agile (boards/sprints/epics), comments, attachments, worklogs, filters, components, versions
- **Cross-Service**: Sprint reports, issue-to-doc conversion, page-issue linking, project status dashboards, release notes generation
- **AI-Optimized**: Markdown/JSON output formats, search scenario guide, constitution hooks for write safety
- **Zero External Dependencies**: Pure Python SDK — no npm, Go, or external CLI tools

## Quick Start

### Installation

```bash
# Clone and install
cd atlassian-cli-plugin
./install.sh

# Or manually
pip install -e .
```

### Configuration

```bash
# Interactive setup
atlassian-cli init

# Or set environment variables
export ATLASSIAN_URL="https://your-domain.atlassian.net"
export ATLASSIAN_EMAIL="user@example.com"
export ATLASSIAN_TOKEN="your-api-token"
```

Get an API token at: https://id.atlassian.com/manage/api-tokens

### Verify

```bash
atlassian-cli jira user me
atlassian-cli confluence space list
```

## Usage

```
atlassian-cli <service> <resource> <action> [options]
```

### Confluence Examples

```bash
# Search
atlassian-cli confluence search --text "API documentation" --space DEV
atlassian-cli confluence search --cql 'label = "architecture" AND space = "ENG"'

# Pages
atlassian-cli confluence page get 12345
atlassian-cli confluence page get-by-title SPACE "Page Title"
atlassian-cli confluence page create --space DEV --title "New Page" --body "<p>Content</p>"

# Spaces
atlassian-cli confluence space list
atlassian-cli confluence space pages DEV --limit 100
```

### Jira Examples

```bash
# Search
atlassian-cli jira search --jql "assignee = currentUser() AND resolution = Unresolved"
atlassian-cli jira search --jql "sprint in openSprints() AND project = PROJ" --all

# Issues
atlassian-cli jira issue get PROJ-123
atlassian-cli jira issue create --project PROJ --type Task --summary "New task"
atlassian-cli jira issue transition PROJ-123 "In Progress"

# Agile
atlassian-cli jira board list
atlassian-cli jira sprint list 1
atlassian-cli jira epic issues EPIC-1
```

### Cross-Service Examples

```bash
# Generate sprint report in Confluence
atlassian-cli cross sprint-report --board 1 --sprint 10 --space REPORTS

# Generate release notes
atlassian-cli cross release-notes --project PROJ --version "2.0" --space DOCS

# Link Confluence page to Jira issue
atlassian-cli cross link-page-to-issue --page 12345 --issue PROJ-123
```

## Output Formats

- `--format markdown` (default): AI/human-readable tables and pages
- `--format json`: Raw JSON for programmatic processing

## Claude Code Skills

| Skill | Trigger | Purpose |
|-------|---------|---------|
| `/atlassian-init` | `atlassian init` | Setup credentials |
| `/confluence` | `confluence` | Confluence operations |
| `/jira` | `jira` | Jira operations |
| `/atlassian-search-guide` | `search guide` | AI search scenarios |

## Safety

All write operations are protected by constitution hooks that require explicit user confirmation before execution. Read operations are always safe.

## Requirements

- Python 3.9+
- `atlassian-python-api` >= 3.41.0

## Documentation

- [API Coverage Map](docs/api-coverage.md) — Full list of supported SDK methods
- [Search Scenarios](docs/search-scenarios.md) — CQL/JQL query examples
- [Cross-Service Workflows](docs/cross-service-workflows.md) — Integration patterns
