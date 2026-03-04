# Atlassian Init / Setup

Setup and configure Atlassian CLI credentials for Confluence and Jira operations.

## Triggers
- `atlassian init`
- `atlassian setup`
- `atlassian 설정`
- `configure atlassian`

## Instructions

When the user wants to set up or configure Atlassian CLI:

### 1. Check Prerequisites
```bash
python3 --version
```
Requires Python 3.9+.

### 2. Check if Already Installed
```bash
atlassian-cli --version 2>/dev/null || echo "Not installed"
```

### 3. Install if Needed
```bash
cd <plugin-directory>
pip install -e . || uv pip install -e .
```

### 4. Check Existing Configuration
```bash
cat ~/.atlassian-cli/config.json 2>/dev/null || echo "No config found"
```

### 5. Collect Credentials
Use `AskUserQuestion` to gather:
- **Atlassian URL**: e.g., `https://your-domain.atlassian.net`
- **Email**: Account email address
- **API Token**: From https://id.atlassian.com/manage/api-tokens

### 6. Save Configuration
```bash
mkdir -p ~/.atlassian-cli
cat > ~/.atlassian-cli/config.json << 'EOF'
{
  "url": "<URL>",
  "email": "<EMAIL>",
  "api_token": "<TOKEN>",
  "auth_type": "cloud",
  "default_confluence_space": "",
  "default_jira_project": ""
}
EOF
chmod 600 ~/.atlassian-cli/config.json
```

### 7. Verify Connection
```bash
atlassian-cli jira user me
atlassian-cli confluence space list --format json
```

### 8. Set Defaults (Optional)
Ask the user if they want to set default space/project:
```bash
atlassian-cli confluence space list
atlassian-cli jira project list
```
Then update config with chosen defaults.

### 9. Plugin Priority Setup
Ask the user if they want this plugin as the default Atlassian tool:

Use `AskUserQuestion` with:
- **Question**: "이 플러그인을 Atlassian(Confluence/Jira) 접근의 기본 도구로 설정할까요? 설정하면 Atlassian MCP 도구보다 이 플러그인이 우선 사용됩니다."
- **Options**:
  - "Yes (Recommended)" — 플러그인 우선 사용 활성화
  - "No" — 기존 동작 유지

If the user agrees:
- Inform them that the plugin's CLAUDE.md already contains the priority rule
- The rule is automatically loaded when the plugin is installed
- No additional configuration needed

If the user declines:
- Skip this step; the plugin will still work when explicitly invoked via skills

## Environment Variables (Alternative)
Instead of config file, users can set:
- `ATLASSIAN_URL`
- `ATLASSIAN_EMAIL`
- `ATLASSIAN_TOKEN`

These override config file values.

## Troubleshooting
- **401 Unauthorized**: Verify email and API token pair
- **404 Not Found**: Check the URL (should end with `.atlassian.net`)
- **Connection refused**: Check network/VPN access
- **Module not found**: Run `pip install atlassian-python-api`
