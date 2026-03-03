# Atlassian CLI Plugin for Claude Code

This plugin provides comprehensive Confluence and Jira operations via the `atlassian-python-api` SDK.

## Setup

1. Install: `cd <this-directory> && pip install -e .` (or `uv pip install -e .`)
2. Configure: `atlassian-cli init` or set env vars `ATLASSIAN_URL`, `ATLASSIAN_EMAIL`, `ATLASSIAN_TOKEN`
3. Verify: `atlassian-cli jira user me`

## Available Skills

| Skill | Trigger | Purpose |
|-------|---------|---------|
| `/atlassian-init` | `atlassian init` | Setup and configure credentials |
| `/confluence` | `confluence`, `컨플루언스` | All Confluence operations |
| `/jira` | `jira`, `지라` | All Jira operations |
| `/atlassian-search-guide` | `atlassian search guide` | AI search scenario guide |

## CLI Usage

```
atlassian-cli <service> <resource> <action> [options]
```

Services: `confluence` (alias: `conf`), `jira`, `cross`, `init`

### Output Formats
- `--format markdown` (default): Human/AI-readable markdown
- `--format json`: Raw JSON for programmatic use

### Exit Codes
- 0: Success
- 1: Error
- 2: Authentication failure

## Constitution (Safety)

**All write operations require user confirmation.** The hooks in `hooks/hooks.json` detect write operations and emit warnings via stderr. Claude Code's built-in permission system then handles the actual user approval before executing the command.

Write operations include:
- **Confluence**: page create/update/delete, attachment upload/delete, label/property changes
- **Jira**: issue create/update/delete/transition, sprint creation, comment CRUD, attachment CRUD

Read operations are always safe and require no confirmation.

## Architecture

```
src/atlassian_cli/
├── cli.py          # argparse entry point
├── config.py       # Credential management
├── auth.py         # SDK client creation
├── formatter.py    # Output formatting
├── confluence/     # Confluence operations (pages, search, spaces, attachments, templates)
├── jira/           # Jira operations (issues, search, projects, agile, comments, attachments, worklogs)
└── cross/          # Cross-service workflows (sprint reports, release notes)
```

## Quick Reference

### Confluence
```bash
atlassian-cli confluence page get <ID>
atlassian-cli confluence search --text "keyword" --space KEY
atlassian-cli confluence space list
```

### Jira
```bash
atlassian-cli jira issue get <KEY>
atlassian-cli jira search --jql "project = PROJ AND status = Open"
atlassian-cli jira user me
```

### Cross-Service
```bash
atlassian-cli cross sprint-report --board <ID> --sprint <ID> --space KEY
atlassian-cli cross release-notes --project PROJ --version "1.0" --space KEY
```
