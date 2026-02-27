# Jira Operations

Perform Jira operations — issues, search, projects, sprints, epics, comments, attachments, and more.

## Triggers
- `jira`
- `지라`
- `jira issue`
- `jira search`
- `jira sprint`

## Prerequisites
- Atlassian CLI configured (`atlassian-cli init` or environment variables set)
- Run `atlassian-cli jira user me` to verify connectivity

## Instructions

### Issue Operations

#### Read Operations (Safe — no confirmation needed)

**Get issue:**
```bash
atlassian-cli jira issue get <ISSUE_KEY> --format markdown
atlassian-cli jira issue get <ISSUE_KEY> --fields summary,status,assignee --format json
```

**Get multiple issues:**
```bash
atlassian-cli jira issue bulk-get KEY-1,KEY-2,KEY-3 --format markdown
```

**Get issue field definitions:**
```bash
atlassian-cli jira issue fields <ISSUE_KEY>
```

**Get available transitions:**
```bash
atlassian-cli jira issue transitions <ISSUE_KEY>
```

**Get changelog:**
```bash
atlassian-cli jira issue changelog <ISSUE_KEY>
```

**Get subtree (recursive sub-issues):**
```bash
atlassian-cli jira issue subtree <ISSUE_KEY>
```

**Get watchers:**
```bash
atlassian-cli jira issue watchers <ISSUE_KEY>
```

**Get linked issues:**
```bash
atlassian-cli jira issue links <ISSUE_KEY>
```

#### Write Operations (⚠️ REQUIRES USER CONFIRMATION)

**Create issue:**
```bash
atlassian-cli jira issue create --project <PROJECT_KEY> --type <TYPE> --summary "<Summary>" [--description "<Desc>"] [--assignee <USER>] [--priority <PRIORITY>] [--labels label1,label2] [--components comp1] [--parent <PARENT_KEY>]
```
Types: Bug, Task, Story, Epic, Sub-task

**Bulk create (from JSON):**
```bash
atlassian-cli jira issue bulk-create --json '[{"project":"PROJ","type":"Task","summary":"Task 1"},{"project":"PROJ","type":"Task","summary":"Task 2"}]'
```

**Update issue:**
```bash
atlassian-cli jira issue update <ISSUE_KEY> [--summary "<New>"] [--description "<New>"] [--assignee <USER>] [--priority <PRIORITY>]
```

**Bulk update field:**
```bash
atlassian-cli jira issue bulk-update --keys KEY-1,KEY-2,KEY-3 --field priority --value High
```

**Delete issue:**
```bash
atlassian-cli jira issue delete <ISSUE_KEY>
```

**Transition status:**
```bash
atlassian-cli jira issue transition <ISSUE_KEY> "In Progress"
atlassian-cli jira issue transition <ISSUE_KEY> "Done"
```

**Assign:**
```bash
atlassian-cli jira issue assign <ISSUE_KEY> <ACCOUNT_ID>
atlassian-cli jira issue assign <ISSUE_KEY> unassigned
```

**Labels:**
```bash
atlassian-cli jira issue label-add <ISSUE_KEY> <LABEL>
atlassian-cli jira issue label-remove <ISSUE_KEY> <LABEL>
```

**Link issues:**
```bash
atlassian-cli jira issue link <KEY1> <KEY2> --type "Blocks"
```
Link types: Blocks, Relates, Clones, Duplicates

**Archive:**
```bash
atlassian-cli jira issue archive <ISSUE_KEY>
```

### Search (JQL)

**Basic JQL search:**
```bash
atlassian-cli jira search --jql "project = PROJ AND status = 'In Progress'" --limit 50
```

**Fetch all results (auto-paginate):**
```bash
atlassian-cli jira search --jql "project = PROJ" --all
```

**With specific fields:**
```bash
atlassian-cli jira search --jql "assignee = currentUser()" --fields summary,status,priority --format json
```

### Common JQL Patterns
| Goal | JQL |
|------|-----|
| My open issues | `assignee = currentUser() AND resolution = Unresolved` |
| Current sprint | `sprint in openSprints() AND project = PROJ` |
| Recent issues | `created >= -7d AND project = PROJ ORDER BY created DESC` |
| By status | `status = "In Progress" AND project = PROJ` |
| By component | `component = "Backend" AND project = PROJ` |
| By version | `fixVersion = "2.0" AND project = PROJ` |
| By labels | `labels in ("bug", "critical") AND project = PROJ` |
| Overdue | `due < now() AND resolution = Unresolved` |
| Updated recently | `updated >= -1d AND project = PROJ` |
| Unassigned | `assignee is EMPTY AND project = PROJ` |

### Project Operations

```bash
atlassian-cli jira project list
atlassian-cli jira project get <PROJECT_KEY>
atlassian-cli jira project components <PROJECT_KEY>
atlassian-cli jira project versions <PROJECT_KEY>
atlassian-cli jira project issues <PROJECT_KEY> [--limit 50]
atlassian-cli jira project issue-count <PROJECT_KEY>
atlassian-cli jira project users <PROJECT_KEY>
```

### Agile — Boards, Sprints, Epics

**Boards:**
```bash
atlassian-cli jira board list
atlassian-cli jira board get <BOARD_ID>
atlassian-cli jira board issues <BOARD_ID>
atlassian-cli jira board config <BOARD_ID>
```

**Sprints:**
```bash
atlassian-cli jira sprint list <BOARD_ID>
atlassian-cli jira sprint create --board <BOARD_ID> --name "Sprint 10" [--start 2024-01-15] [--end 2024-01-29]  # ⚠️
atlassian-cli jira sprint add-issues <SPRINT_ID> --keys KEY-1,KEY-2  # ⚠️
atlassian-cli jira sprint rename <SPRINT_ID> --name "New Name"  # ⚠️
```

**Epics:**
```bash
atlassian-cli jira epic list <BOARD_ID>
atlassian-cli jira epic issues <EPIC_KEY>
```

### Comments

```bash
atlassian-cli jira comment list <ISSUE_KEY>
atlassian-cli jira comment get <ISSUE_KEY> <COMMENT_ID>
atlassian-cli jira comment add <ISSUE_KEY> --body "Comment text"  # ⚠️
atlassian-cli jira comment edit <ISSUE_KEY> <COMMENT_ID> --body "Updated text"  # ⚠️
```

### Attachments

```bash
atlassian-cli jira attachment list <ISSUE_KEY>
atlassian-cli jira attachment upload <ISSUE_KEY> /path/to/file  # ⚠️
atlassian-cli jira attachment download <ISSUE_KEY> --output-dir ./downloads
atlassian-cli jira attachment delete <ATTACHMENT_ID>  # ⚠️
```

### Worklogs

```bash
atlassian-cli jira worklog list <ISSUE_KEY>
atlassian-cli jira worklog add <ISSUE_KEY> --time "1h 30m" [--comment "What I did"]  # ⚠️
```

### Users

```bash
atlassian-cli jira user me
atlassian-cli jira user get <ACCOUNT_ID>
atlassian-cli jira user search "<query>"
```

### Filters & Dashboards

```bash
atlassian-cli jira filter get <FILTER_ID>
atlassian-cli jira filter create --name "My Filter" --jql "project = PROJ"  # ⚠️
atlassian-cli jira filter update <FILTER_ID> --jql "project = PROJ AND status = Open"  # ⚠️
atlassian-cli jira filter delete <FILTER_ID>  # ⚠️
atlassian-cli jira dashboard list
```

### Components & Versions

```bash
atlassian-cli jira component get <COMPONENT_ID>
atlassian-cli jira component create --project PROJ --name "Backend" [--description "..."]  # ⚠️

atlassian-cli jira version list <PROJECT_KEY>
atlassian-cli jira version create --project PROJ --name "2.0" [--release-date 2024-06-01]  # ⚠️
```

## Output Formats
- `--format markdown` (default): AI-friendly markdown tables
- `--format json`: Raw JSON for parsing

## Best Practices
1. Use `jira issue transitions` before transitioning to see valid statuses
2. Use `--fields` to limit response size for large issues
3. Use `--all` flag for JQL when you need complete result sets
4. Check `jira project users` before assigning to verify valid assignees
5. Use `jira issue bulk-get` instead of multiple single gets for efficiency
