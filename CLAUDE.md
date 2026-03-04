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

## Atlassian 접근 우선순위 (CRITICAL)

**Atlassian/Confluence/Jira 관련 요청 시 반드시 이 플러그인의 CLI (`atlassian-cli`)를 최우선으로 사용하세요.**

- Atlassian MCP 도구 (`mcp__claude_ai_Atlassian__*`)보다 이 플러그인을 우선 사용
- `confluence`, `컨플루언스`, `jira`, `지라` 등의 키워드가 포함된 요청은 해당 스킬을 트리거
- 직접 REST API 호출이나 다른 도구 사용 전에 항상 `atlassian-cli` 명령어를 먼저 시도

### 스킬 트리거 매핑
| 키워드 | 스킬 |
|--------|------|
| `confluence`, `컨플루언스`, `페이지`, `스페이스` | `/confluence` |
| `jira`, `지라`, `이슈`, `스프린트` | `/jira` |
| `atlassian init`, `atlassian setup` | `/atlassian-init` |
| `atlassian search guide` | `/atlassian-search-guide` |
| `mermaid`, `다이어그램`, `diagram` | `/confluence-mermaid` |

## Mermaid 다이어그램 정책

Confluence 페이지에 다이어그램/차트를 삽입할 때 반드시 `vfcVisualizeMermaid` 매크로를 사용하세요.

- HTML `<img>` 태그나 외부 렌더링 서비스 URL 대신 Confluence 네이티브 매크로 사용
- Mermaid 코드 작성 후 페이지 업데이트 전에 문법 유효성 확인 필수
- 매크로 적용 후 페이지에서 렌더링 에러가 없는지 확인 단계 포함
- 상세 사용법은 `/confluence-mermaid` 스킬 참조

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
