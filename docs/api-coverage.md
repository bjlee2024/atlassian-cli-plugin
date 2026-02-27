# API Coverage Map

Coverage of `atlassian-python-api` SDK methods in this CLI.

## Confluence (~60 commands)

### Pages (16 commands)
| Method | CLI Command | Type |
|--------|-------------|------|
| `get_page_by_id` | `confluence page get` | Read |
| `get_page_by_title` | `confluence page get-by-title` | Read |
| `page_exists` | `confluence page exists` | Read |
| `get_page_child_by_type` | `confluence page children` | Read |
| `get_page_ancestors` | `confluence page ancestors` | Read |
| `history` | `confluence page history` | Read |
| `get_page_labels` | `confluence page labels` | Read |
| `get_page_properties` | `confluence page properties` | Read |
| `get_all_restrictions_for_content` | `confluence page restrictions` | Read |
| `create_page` | `confluence page create` | Write |
| `update_page` | `confluence page update` | Write |
| `update_or_create` | `confluence page upsert` | Write |
| `append_page` | `confluence page append` | Write |
| `remove_page` | `confluence page delete` | Write |
| `set_page_label` | `confluence page label-add` | Write |
| `remove_page_label` | `confluence page label-remove` | Write |

### Search (5 commands)
| Method | CLI Command | Type |
|--------|-------------|------|
| `cql` | `confluence search --cql` | Read |
| `cql` (text wrapper) | `confluence search --text` | Read |
| `get_all_pages_by_label` | `confluence search --label` | Read |
| `get_tables_from_page` | `confluence tables` | Read |

### Spaces (6 commands)
| Method | CLI Command | Type |
|--------|-------------|------|
| `get_all_spaces` | `confluence space list` | Read |
| `get_space` | `confluence space get` | Read |
| `get_space_content` | `confluence space content` | Read |
| `get_all_pages_from_space` | `confluence space pages` | Read |
| `get_space_permissions` | `confluence space permissions` | Read |
| `get_trashed_contents_by_space` | `confluence space trash` | Read |

### Attachments (4 commands)
| Method | CLI Command | Type |
|--------|-------------|------|
| `get_attachments_from_content` | `confluence attachment list` | Read |
| `attach_file` | `confluence attachment upload` | Write |
| `download_attachments_from_page` | `confluence attachment download` | Read |
| `delete_attachment` | `confluence attachment delete` | Write |

### Templates (2 commands)
| Method | CLI Command | Type |
|--------|-------------|------|
| `get_content_templates` | `confluence template list` | Read |
| `get_content_template` | `confluence template get` | Read |

### Export & Users (4 commands)
| Method | CLI Command | Type |
|--------|-------------|------|
| `export_page` | `confluence export` | Read |
| `get_user_details_by_username` | `confluence user get` | Read |
| `get_all_groups` | `confluence group list` | Read |
| `get_group_members` | `confluence group members` | Read |

---

## Jira (~80 commands)

### Issues (20 commands)
| Method | CLI Command | Type |
|--------|-------------|------|
| `issue` / `get_issue` | `jira issue get` | Read |
| `bulk_issue` | `jira issue bulk-get` | Read |
| `issue_fields` | `jira issue fields` | Read |
| `get_issue_transitions` | `jira issue transitions` | Read |
| `get_issue_changelog` | `jira issue changelog` | Read |
| `get_issue_tree_recursive` | `jira issue subtree` | Read |
| `issue_get_watchers` | `jira issue watchers` | Read |
| (from fields) | `jira issue links` | Read |
| `issue_create` | `jira issue create` | Write |
| `create_issues` | `jira issue bulk-create` | Write |
| `issue_update` | `jira issue update` | Write |
| `bulk_update_issue_field` | `jira issue bulk-update` | Write |
| `delete_issue` | `jira issue delete` | Write |
| `set_issue_status` | `jira issue transition` | Write |
| `assign_issue` | `jira issue assign` | Write |
| `issue_add_label` | `jira issue label-add` | Write |
| `issue_remove_label` | `jira issue label-remove` | Write |
| `create_issue_link` | `jira issue link` | Write |
| `issue_archive` | `jira issue archive` | Write |

### Search (2 commands)
| Method | CLI Command | Type |
|--------|-------------|------|
| `jql` | `jira search --jql` | Read |
| `get_all_issues_from_jql` | `jira search --jql --all` | Read |

### Projects (7 commands)
| Method | CLI Command | Type |
|--------|-------------|------|
| `projects` | `jira project list` | Read |
| `project` | `jira project get` | Read |
| `get_project_components` | `jira project components` | Read |
| `get_project_versions` | `jira project versions` | Read |
| `get_all_project_issues` | `jira project issues` | Read |
| `get_project_issues_count` | `jira project issue-count` | Read |
| `get_all_assignable_users_for_project` | `jira project users` | Read |

### Agile (10 commands)
| Method | CLI Command | Type |
|--------|-------------|------|
| `get_all_agile_boards` | `jira board list` | Read |
| `get_agile_board` | `jira board get` | Read |
| `get_issues_for_board` | `jira board issues` | Read |
| `get_agile_board_configuration` | `jira board config` | Read |
| `get_all_sprints_from_board` | `jira sprint list` | Read |
| `create_sprint` | `jira sprint create` | Write |
| `add_issues_to_sprint` | `jira sprint add-issues` | Write |
| `rename_sprint` | `jira sprint rename` | Write |
| `get_epics` | `jira epic list` | Read |
| `epic_issues` | `jira epic issues` | Read |

### Comments (4 commands)
| Method | CLI Command | Type |
|--------|-------------|------|
| `issue_get_comments` | `jira comment list` | Read |
| `issue_get_comment` | `jira comment get` | Read |
| `issue_add_comment` | `jira comment add` | Write |
| `issue_edit_comment` | `jira comment edit` | Write |

### Attachments (4 commands)
| Method | CLI Command | Type |
|--------|-------------|------|
| `get_attachments_ids_from_issue` | `jira attachment list` | Read |
| `add_attachment` | `jira attachment upload` | Write |
| `download_attachments_from_issue` | `jira attachment download` | Read |
| `remove_attachment` | `jira attachment delete` | Write |

### Worklogs (2 commands)
| Method | CLI Command | Type |
|--------|-------------|------|
| `issue_get_worklog` | `jira worklog list` | Read |
| `issue_worklog` | `jira worklog add` | Write |

### Filters & Dashboards (5 commands)
| Method | CLI Command | Type |
|--------|-------------|------|
| `get_filter` | `jira filter get` | Read |
| `create_filter` | `jira filter create` | Write |
| `update_filter` | `jira filter update` | Write |
| `delete_filter` | `jira filter delete` | Write |
| `get_dashboards` | `jira dashboard list` | Read |

### Components & Versions (4 commands)
| Method | CLI Command | Type |
|--------|-------------|------|
| `component` | `jira component get` | Read |
| `create_component` | `jira component create` | Write |
| `get_project_versions` | `jira version list` | Read |
| `add_version` | `jira version create` | Write |

### Users (3 commands)
| Method | CLI Command | Type |
|--------|-------------|------|
| `myself` | `jira user me` | Read |
| `user` | `jira user get` | Read |
| `user_find_by_user_string` | `jira user search` | Read |

---

## Cross-Service (5 workflows)

| Workflow | Command |
|----------|---------|
| Sprint Report → Confluence | `cross sprint-report` |
| Issues → Confluence Doc | `cross issue-to-doc` |
| Page ↔ Issue Link | `cross link-page-to-issue` |
| Project Status Dashboard | `cross project-status` |
| Release Notes | `cross release-notes` |
