# Search Scenarios — Detailed Documentation

## Confluence Search (CQL)

CQL (Confluence Query Language) is used for structured content searches.

### Basic Syntax
```
field operator "value" [AND|OR] field operator "value" [ORDER BY field ASC|DESC]
```

### Operators
| Operator | Description | Example |
|----------|-------------|---------|
| `=` | Exact match | `space = "DEV"` |
| `!=` | Not equal | `status != "archived"` |
| `~` | Contains (fuzzy) | `text ~ "kubernetes"` |
| `!~` | Does not contain | `text !~ "draft"` |
| `>`, `>=`, `<`, `<=` | Comparison | `lastModified >= "2024-01-01"` |
| `IN` | In set | `space IN ("DEV", "OPS")` |

### Fields
| Field | Description |
|-------|-------------|
| `text` | Full-text content search |
| `title` | Page/blog title |
| `space` | Space key |
| `type` | Content type (page, blogpost, attachment, comment) |
| `label` | Content label |
| `creator` | Original author |
| `contributor` | Any editor |
| `lastModified` | Last modification date |
| `created` | Creation date |
| `ancestor` | Parent page ID |
| `container` | Parent container |

### Scenario Examples

**1. Find architecture decision records:**
```bash
atlassian-cli confluence search --cql 'label = "adr" AND space = "ARCH" ORDER BY created DESC'
```

**2. Find all docs modified this month:**
```bash
atlassian-cli confluence search --cql 'lastModified >= "2024-06-01" AND space = "TEAM"'
```

**3. Find pages under a specific parent:**
```bash
atlassian-cli confluence search --cql 'ancestor = 12345 AND type = "page"'
```

**4. Find blog posts about releases:**
```bash
atlassian-cli confluence search --cql 'type = "blogpost" AND text ~ "release" AND space = "ENG"'
```

**5. Find meeting notes:**
```bash
atlassian-cli confluence search --cql 'title ~ "Meeting Notes" AND space = "TEAM" ORDER BY created DESC' --limit 10
```

---

## Jira Search (JQL)

JQL (Jira Query Language) provides powerful issue searching.

### Basic Syntax
```
field operator value [AND|OR] field operator value [ORDER BY field ASC|DESC]
```

### Key Functions
| Function | Description | Example |
|----------|-------------|---------|
| `currentUser()` | Logged-in user | `assignee = currentUser()` |
| `openSprints()` | Active sprints | `sprint in openSprints()` |
| `closedSprints()` | Closed sprints | `sprint in closedSprints()` |
| `futureSprints()` | Future sprints | `sprint in futureSprints()` |
| `now()` | Current datetime | `due < now()` |
| `startOfDay()` | Start of today | `created >= startOfDay()` |
| `endOfWeek()` | End of this week | `due <= endOfWeek()` |
| `membersOf("group")` | Group members | `assignee in membersOf("dev-team")` |

### Relative Dates
- `-1d` = 1 day ago
- `-7d` = 1 week ago
- `-30d` = 30 days ago
- `-1w` = 1 week ago
- `-4w` = 4 weeks ago

### Scenario Examples

**1. Sprint planning — unestimated stories:**
```bash
atlassian-cli jira search --jql "project = PROJ AND issuetype = Story AND originalEstimate is EMPTY AND sprint in futureSprints()"
```

**2. Bug triage — unassigned high-priority bugs:**
```bash
atlassian-cli jira search --jql "project = PROJ AND issuetype = Bug AND assignee is EMPTY AND priority in (Highest, High) ORDER BY created DESC"
```

**3. Release readiness — open issues for version:**
```bash
atlassian-cli jira search --jql "project = PROJ AND fixVersion = '2.0' AND resolution = Unresolved ORDER BY priority DESC"
```

**4. Team workload — issues per assignee:**
```bash
atlassian-cli jira search --jql "project = PROJ AND sprint in openSprints() AND resolution = Unresolved ORDER BY assignee ASC"
```

**5. Stale issues — not updated in 30 days:**
```bash
atlassian-cli jira search --jql "project = PROJ AND resolution = Unresolved AND updated <= -30d ORDER BY updated ASC"
```

**6. Blocked issues:**
```bash
atlassian-cli jira search --jql "project = PROJ AND status = 'Blocked' OR (status = 'In Progress' AND labels = 'blocked')"
```

**7. Recently resolved:**
```bash
atlassian-cli jira search --jql "project = PROJ AND resolved >= -7d ORDER BY resolved DESC"
```

**8. Subtasks of an epic:**
```bash
atlassian-cli jira search --jql "'Epic Link' = EPIC-123 ORDER BY rank ASC"
```

**9. Cross-project dependencies:**
```bash
atlassian-cli jira search --jql "issueFunction in linkedIssuesOf('project = PROJ AND sprint in openSprints()')"
```

**10. Component health — bugs per component:**
```bash
atlassian-cli jira search --jql "project = PROJ AND issuetype = Bug AND component = 'Backend' AND resolution = Unresolved"
```
