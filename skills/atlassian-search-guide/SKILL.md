# Atlassian Search Guide

AI 에이전트가 Atlassian 콘텐츠를 효율적으로 탐색하기 위한 시나리오별 검색 가이드.
A scenario-based guide for AI agents to efficiently search Atlassian content.

## Triggers
- `atlassian search guide`
- `검색 가이드`
- `how to search confluence`
- `how to search jira`
- `atlassian search`

## Instructions

When the user asks how to find information in Confluence or Jira, or when you need to search Atlassian content, follow this decision tree.

### Search Strategy Decision Tree

```
"What are you looking for?"
├── Known page/issue → Direct lookup by ID/key
├── Keyword-based → CQL/JQL text search
├── Structural → Space/project tree traversal
├── Relationship-based → Labels, links, components
└── Time-based → Date range filtering
```

---

### Confluence Search Scenarios

#### 1. Find documents about a specific topic
```bash
atlassian-cli confluence search --text "keyword" --space SPACE_KEY --limit 25
```
For complex queries:
```bash
atlassian-cli confluence search --cql 'text ~ "keyword1" AND text ~ "keyword2" AND space = "KEY"' --limit 25
```

#### 2. Find recently changed documents
```bash
atlassian-cli confluence search --cql 'lastModified >= "2024-01-01" AND space = KEY ORDER BY lastModified DESC' --limit 20
```

#### 3. Find documents by a specific user
```bash
atlassian-cli confluence search --cql 'contributor = "username" AND space = KEY' --limit 25
```

#### 4. Find documents by label
```bash
atlassian-cli confluence search --label "architecture" --limit 50
```
Multiple labels:
```bash
atlassian-cli confluence search --cql 'label = "architecture" AND label = "backend"'
```

#### 5. Navigate page hierarchy
```bash
# Get children of a page
atlassian-cli confluence page children <PAGE_ID>
# Get parent chain
atlassian-cli confluence page ancestors <PAGE_ID>
```
For deep traversal, start from space root and navigate down:
```bash
atlassian-cli confluence space pages <SPACE_KEY> --limit 100
```

#### 6. Extract data from a page
```bash
# Get tables
atlassian-cli confluence tables <PAGE_ID>
# Get full content
atlassian-cli confluence page get <PAGE_ID> --format json
```

#### 7. Find all pages in a space
```bash
atlassian-cli confluence space pages <SPACE_KEY> --limit 500
```

#### 8. Complex search with multiple conditions
```bash
atlassian-cli confluence search --cql 'space = "KEY" AND type = "page" AND text ~ "API" AND lastModified >= "2024-01-01" ORDER BY lastModified DESC'
```

#### 9. Find attachments
```bash
atlassian-cli confluence search --cql 'type = attachment AND filename ~ "*.pdf" AND space = "KEY"'
# Or list attachments on a specific page
atlassian-cli confluence attachment list <PAGE_ID>
```

#### 10. Track page changes
```bash
atlassian-cli confluence page history <PAGE_ID>
```

---

### Jira Search Scenarios

#### 1. My open issues
```bash
atlassian-cli jira search --jql "assignee = currentUser() AND resolution = Unresolved ORDER BY priority DESC"
```

#### 2. Current sprint issues
```bash
atlassian-cli jira search --jql "sprint in openSprints() AND project = PROJ ORDER BY rank"
```

#### 3. Recently created issues
```bash
atlassian-cli jira search --jql "created >= -7d AND project = PROJ ORDER BY created DESC"
```

#### 4. Issues by status
```bash
atlassian-cli jira search --jql "status = 'In Progress' AND project = PROJ"
```
Multiple statuses:
```bash
atlassian-cli jira search --jql "status in ('To Do', 'In Progress') AND project = PROJ"
```

#### 5. Epic and its issues
```bash
atlassian-cli jira epic issues <EPIC_KEY>
```
Or via JQL:
```bash
atlassian-cli jira search --jql "'Epic Link' = EPIC-123"
```

#### 6. Issues by component
```bash
atlassian-cli jira search --jql "component = 'Backend' AND project = PROJ"
```

#### 7. Issues by fix version
```bash
atlassian-cli jira search --jql "fixVersion = '2.0' AND project = PROJ ORDER BY priority DESC"
```

#### 8. Issues with specific labels
```bash
atlassian-cli jira search --jql "labels in ('bug', 'critical') AND project = PROJ"
```

#### 9. Issue subtree (recursive children)
```bash
atlassian-cli jira issue subtree <ISSUE_KEY>
```

#### 10. Issue change history
```bash
atlassian-cli jira issue changelog <ISSUE_KEY>
```

#### 11. Multiple issues at once
```bash
atlassian-cli jira issue bulk-get KEY-1,KEY-2,KEY-3 --format json
```

---

### Cross-Service Search Patterns

#### 1. Find Confluence docs related to a Jira issue
```bash
atlassian-cli confluence search --cql 'text ~ "PROJ-123"' --limit 10
```

#### 2. Find Jira issues related to a Confluence page
```bash
# Get page title first
atlassian-cli confluence page get <PAGE_ID> --format json
# Then search Jira
atlassian-cli jira search --jql "summary ~ 'page title' OR description ~ 'page title'"
```

#### 3. Full project overview
```bash
# Jira side
atlassian-cli jira project get <PROJECT_KEY>
atlassian-cli jira search --jql "project = PROJ AND resolution = Unresolved" --all

# Confluence side
atlassian-cli confluence space pages <SPACE_KEY> --limit 100
```

#### 4. User activity across services
```bash
# Confluence contributions
atlassian-cli confluence search --cql 'contributor = "user"' --limit 20
# Jira assignments
atlassian-cli jira search --jql "assignee = 'user' AND updated >= -30d"
```

---

### Search Optimization Tips

1. **Pagination**: Use `--limit` parameter (default 25-50, max varies by endpoint)
2. **Field selection**: Use `--fields` in Jira to request only needed fields
3. **Format**: Use `--format json` when you need to extract specific data programmatically
4. **Incremental search**: Start broad, then narrow with additional filters
5. **Use `--all` carefully**: It fetches all pages of results; use only when you need the complete set
6. **CQL vs text search**: CQL is more powerful but requires proper syntax; `--text` is simpler for keyword searches
7. **Date formats**: Use `"YYYY-MM-DD"` in CQL, relative dates like `-7d` in JQL
