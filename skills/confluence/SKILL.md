# Confluence Operations

Perform Confluence operations — pages, spaces, search, attachments, templates, and more.

## Triggers
- `confluence`
- `컨플루언스`
- `confluence page`
- `confluence search`
- `confluence space`

## Prerequisites
- Atlassian CLI configured (`atlassian-cli init` or environment variables set)
- Run `atlassian-cli confluence space list` to verify connectivity

## Instructions

### Page Operations

#### Read Operations (Safe — no confirmation needed)

**Get page by ID:**
```bash
atlassian-cli confluence page get <PAGE_ID> --format markdown
```

**Get page by title:**
```bash
atlassian-cli confluence page get-by-title <SPACE_KEY> "<Page Title>" --format markdown
```

**Check page existence:**
```bash
atlassian-cli confluence page exists <SPACE_KEY> "<Page Title>"
```

**Get child pages:**
```bash
atlassian-cli confluence page children <PAGE_ID> --format markdown
```

**Get page ancestors (parent hierarchy):**
```bash
atlassian-cli confluence page ancestors <PAGE_ID> --format markdown
```

**Get page version history:**
```bash
atlassian-cli confluence page history <PAGE_ID> --format markdown
```

**Get page labels:**
```bash
atlassian-cli confluence page labels <PAGE_ID> --format markdown
```

**Get page properties:**
```bash
atlassian-cli confluence page properties <PAGE_ID> --format markdown
```

**Get page restrictions:**
```bash
atlassian-cli confluence page restrictions <PAGE_ID> --format markdown
```

#### Write Operations (⚠️ REQUIRES USER CONFIRMATION)

**Create page:**
```bash
atlassian-cli confluence page create --space <SPACE_KEY> --title "<Title>" --body "<HTML body>" [--parent-id <PARENT_ID>]
```

**Update page:**
```bash
atlassian-cli confluence page update <PAGE_ID> --title "<New Title>" --body "<New HTML body>"
```

**Create or update (upsert):**
```bash
atlassian-cli confluence page upsert --space <SPACE_KEY> --title "<Title>" --body "<body>" [--parent-id <PARENT_ID>]
```

**Append content to page:**
```bash
atlassian-cli confluence page append <PAGE_ID> --body "<HTML to append>"
```

**Delete page:**
```bash
atlassian-cli confluence page delete <PAGE_ID> [--recursive]
```

**Move page:**
```bash
atlassian-cli confluence page move <PAGE_ID> --target-id <TARGET_PAGE_ID>
```

**Add/remove label:**
```bash
atlassian-cli confluence page label-add <PAGE_ID> <LABEL>
atlassian-cli confluence page label-remove <PAGE_ID> <LABEL>
```

**Set/delete property:**
```bash
atlassian-cli confluence page property-set <PAGE_ID> --key <KEY> --value '<JSON>'
atlassian-cli confluence page property-delete <PAGE_ID> --key <KEY>
```

### Search

**CQL search:**
```bash
atlassian-cli confluence search --cql 'text ~ "keyword" AND space = "SPACE"' --limit 25
```

**Text search (simplified):**
```bash
atlassian-cli confluence search --text "keyword" --space SPACE_KEY --limit 25
```

**Search by label:**
```bash
atlassian-cli confluence search --label "architecture" --limit 50
```

**Extract tables from page:**
```bash
atlassian-cli confluence tables <PAGE_ID>
```

### Common CQL Patterns
| Goal | CQL |
|------|-----|
| Recent changes | `lastModified >= "2024-01-01" AND space = KEY ORDER BY lastModified DESC` |
| By contributor | `contributor = "user" AND space = KEY` |
| By type | `type = "page" AND space = KEY` |
| Attachments | `type = attachment AND container.title = "Page"` |
| Blog posts | `type = "blogpost" AND space = KEY` |

### Space Operations

```bash
atlassian-cli confluence space list [--limit 50]
atlassian-cli confluence space get <SPACE_KEY>
atlassian-cli confluence space content <SPACE_KEY>
atlassian-cli confluence space pages <SPACE_KEY> [--limit 50]
atlassian-cli confluence space permissions <SPACE_KEY>
atlassian-cli confluence space trash <SPACE_KEY>
```

### Attachment Operations

```bash
# List attachments on a page
atlassian-cli confluence attachment list <PAGE_ID>

# Upload file (⚠️ REQUIRES CONFIRMATION)
atlassian-cli confluence attachment upload <PAGE_ID> /path/to/file.pdf

# Download all attachments
atlassian-cli confluence attachment download <PAGE_ID> --output-dir ./downloads

# Delete attachment (⚠️ REQUIRES CONFIRMATION)
atlassian-cli confluence attachment delete <PAGE_ID> filename.pdf
```

### Template Operations

```bash
atlassian-cli confluence template list
atlassian-cli confluence template get <TEMPLATE_ID>
```

### Export

```bash
atlassian-cli confluence export <PAGE_ID> --output page.pdf
```

### User & Group

```bash
atlassian-cli confluence user get <USERNAME>
atlassian-cli confluence group list
atlassian-cli confluence group members <GROUP_NAME>
```

## Output Formats
- `--format markdown` (default): Human/AI readable markdown tables and pages
- `--format json`: Raw JSON for programmatic processing

## Best Practices
1. Always check page existence before creating to avoid duplicates
2. Use `--format json` when you need to parse specific fields
3. For large spaces, use `--limit` to control result size
4. Use CQL for complex searches; `--text` for simple keyword searches
5. When updating pages, the CLI handles version numbering automatically
