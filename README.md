# Atlassian CLI Plugin for Claude Code

A comprehensive Atlassian CLI plugin that provides **60+ Confluence** and **80+ Jira** commands via the `atlassian-python-api` SDK. No external CLI binaries required.

## Features

- **Confluence**: Pages CRUD, CQL search, spaces, attachments, templates, export, user/group operations
- **Jira**: Issues CRUD, JQL search, projects, agile (boards/sprints/epics), comments, attachments, worklogs, filters, components, versions
- **Cross-Service**: Sprint reports, issue-to-doc conversion, page-issue linking, project status dashboards, release notes generation
- **AI-Optimized**: Markdown/JSON output formats, search scenario guide, constitution hooks for write safety
- **Zero External Dependencies**: Pure Python SDK — no npm, Go, or external CLI tools

## Quick Start

### 1. Claude Code 플러그인 설치

Claude Code에서 플러그인을 설치합니다:

```bash
# Claude Code 내에서 실행
/install-plugin https://github.com/bjlee2024/atlassian-cli-plugin
```

또는 수동으로 설치:

```bash
# 저장소 클론
git clone https://github.com/bjlee2024/atlassian-cli-plugin.git
cd atlassian-cli-plugin

# install.sh 실행 (Python 패키지 + CLI 도구 설치)
./install.sh
```

> **요구사항**: Python 3.9+ 및 `pip` 또는 `uv` 패키지 매니저가 필요합니다.

### 2. API Token 발급

1. https://id.atlassian.com/manage/api-tokens 에 접속
2. **Create API token** 클릭
3. 토큰 이름 입력 (예: `claude-code`) 후 생성
4. 생성된 토큰을 복사 (이후 다시 볼 수 없음)

### 3. 초기 설정 (Init)

Claude Code 세션에서 `/atlassian-init` 스킬을 사용하거나 CLI로 직접 설정합니다:

**방법 A: Claude Code 스킬 사용 (권장)**

```
/atlassian-init
```

대화형으로 URL, 이메일, API 토큰을 입력받아 자동 설정합니다.

**방법 B: CLI 직접 설정**

```bash
atlassian-cli init
```

**방법 C: 환경변수 설정**

```bash
export ATLASSIAN_URL="https://your-domain.atlassian.net"
export ATLASSIAN_EMAIL="user@example.com"
export ATLASSIAN_TOKEN="your-api-token"
```

**방법 D: 설정 파일 직접 생성**

```bash
mkdir -p ~/.atlassian-cli
cat > ~/.atlassian-cli/config.json << 'EOF'
{
  "url": "https://your-domain.atlassian.net",
  "email": "user@example.com",
  "api_token": "your-api-token",
  "auth_type": "cloud",
  "default_confluence_space": "",
  "default_jira_project": ""
}
EOF
chmod 600 ~/.atlassian-cli/config.json
```

> **참고**: 환경변수가 설정되어 있으면 config 파일보다 우선 적용됩니다.

### 4. 연결 확인

```bash
# Jira 연결 확인
atlassian-cli jira user me

# Confluence 연결 확인
atlassian-cli confluence space list
```

### 5. 기본값 설정 (선택)

자주 사용하는 Confluence Space나 Jira Project를 기본값으로 설정할 수 있습니다:

```bash
# 사용 가능한 Space/Project 확인
atlassian-cli confluence space list
atlassian-cli jira project list

# config.json의 default_confluence_space, default_jira_project 값을 수정
```

### Troubleshooting

| 에러 | 원인 | 해결 |
|------|------|------|
| `401 Unauthorized` | 이메일 또는 API 토큰이 잘못됨 | 토큰 재발급 후 재설정 |
| `404 Not Found` | URL이 잘못됨 | `https://xxx.atlassian.net` 형식 확인 |
| `Connection refused` | 네트워크/VPN 문제 | 네트워크 연결 확인 |
| `Module not found` | 패키지 미설치 | `pip install atlassian-python-api` 실행 |
| `command not found` | PATH 미등록 | `python3 -m atlassian_cli --version`으로 확인 |

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

## Claude Desktop (MCP Server)

Claude Desktop cannot load Claude Code plugins/skills/hooks directly — it talks to external tools via **MCP servers**. This package ships a thin MCP bridge that wraps the full CLI (all 140+ commands) and exposes it to Claude Desktop.

**1. Install with the MCP extra:**

```bash
pip install -e ".[mcp]"   # adds the `mcp` dependency + `atlassian-cli-mcp` script
```

**2. Configure credentials** (the MCP server reuses the CLI's config):

```bash
atlassian-cli init        # writes ~/.atlassian-cli/config.json
```

**3. Register in `claude_desktop_config.json`**
(macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "atlassian-cli": {
      "command": "/absolute/path/to/atlassian-cli-mcp"
    }
  }
}
```

Find the absolute path with `which atlassian-cli-mcp`. Restart Claude Desktop, then ask it to use the **`atlassian_cli`** / **`atlassian_help`** tools.

The bridge mirrors the plugin's safety Constitution: write operations are **blocked** unless the model passes `confirm_write=true`, so Claude must confirm the change with you first.

## Safety

All write operations are protected by constitution hooks (Claude Code) / the `confirm_write` guard (Claude Desktop MCP) that require explicit user confirmation before execution. Read operations are always safe.

## Requirements

- Python 3.9+
- `atlassian-python-api` >= 3.41.0

## Documentation

- [API Coverage Map](docs/api-coverage.md) — Full list of supported SDK methods
- [Search Scenarios](docs/search-scenarios.md) — CQL/JQL query examples
- [Cross-Service Workflows](docs/cross-service-workflows.md) — Integration patterns
