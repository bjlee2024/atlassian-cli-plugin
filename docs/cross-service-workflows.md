# Cross-Service Workflows

Patterns for integrating Confluence and Jira operations.

## Available Workflows

### 1. Sprint Report → Confluence

Generates a sprint report page in Confluence from Jira sprint data.

```bash
atlassian-cli cross sprint-report --board <BOARD_ID> --sprint <SPRINT_ID> --space <SPACE_KEY> [--parent-page <PAGE_ID>]
```

**What it does:**
1. Fetches sprint info and all issues via JQL
2. Groups issues by status
3. Creates a formatted table with Key, Summary, Assignee, Priority
4. Creates or updates a Confluence page titled "Sprint Report - {Sprint Name}"

**Use case:** End-of-sprint review meetings, sprint retrospectives.

### 2. Jira Issues → Confluence Documentation

Converts JQL query results into a Confluence documentation page.

```bash
atlassian-cli cross issue-to-doc --jql "<JQL>" --space <SPACE_KEY> --page-title "<Title>"
```

**What it does:**
1. Executes JQL query to fetch matching issues
2. Creates a table with Key, Type, Summary, Status, Assignee
3. Creates or updates the specified Confluence page

**Use case:** Requirements tracking, feature lists, bug inventories.

### 3. Confluence Page ↔ Jira Issue Link

Creates a bidirectional link between a Confluence page and a Jira issue.

```bash
atlassian-cli cross link-page-to-issue --page <PAGE_ID> --issue <ISSUE_KEY>
```

**What it does:**
1. Fetches Confluence page info (title, URL)
2. Creates a remote link on the Jira issue pointing to the Confluence page

**Use case:** Linking design docs to implementation tickets, connecting specs to stories.

### 4. Project Status Dashboard

Generates a project status overview page in Confluence.

```bash
atlassian-cli cross project-status --project <PROJECT_KEY> --space <SPACE_KEY>
```

**What it does:**
1. Fetches project info and issue counts by status
2. Lists recently updated issues (last 7 days)
3. Creates or updates a "Project Status - {Project Name}" page

**Use case:** Stakeholder updates, weekly status reports.

### 5. Release Notes Generation

Generates release notes from a Jira version.

```bash
atlassian-cli cross release-notes --project <PROJECT_KEY> --version "<VERSION>" --space <SPACE_KEY>
```

**What it does:**
1. Fetches all issues with the specified fixVersion
2. Groups by issue type (Bug Fixes, New Features, Tasks)
3. Creates or updates a "Release Notes - {Project} v{Version}" page

**Use case:** Release communications, changelog generation.

## Custom Workflow Patterns

### Manual Multi-Step Workflow

For workflows not covered by built-in commands, chain CLI calls:

```bash
# 1. Get sprint issues
atlassian-cli jira search --jql "sprint in openSprints() AND project = PROJ" --format json > /tmp/sprint-issues.json

# 2. Process and create doc (using the data)
atlassian-cli confluence page upsert --space TEAM --title "Current Sprint" --body "<content>"
```

### Automated Reporting

Schedule periodic updates using cron or CI/CD:

```bash
# Daily project status update
0 9 * * 1-5 atlassian-cli cross project-status --project PROJ --space STATUS

# Weekly sprint report
0 17 * * 5 atlassian-cli cross sprint-report --board 1 --sprint $(atlassian-cli jira sprint list 1 --format json | jq '.[-1].id') --space REPORTS
```
