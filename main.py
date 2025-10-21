from alllatsian.confluence.confluence_service_handle import create_table_est_for_doc_step
from alllatsian.jira.jira_task_controller import create_lst_task_preview_step
from alllatsian.jira.jira_task_preview_handle import create_lst_user_story_preview_step
from alllatsian.jira.jira_task_service_handle import create_list_user_story_jira_step, create_task_jira_step


def main_app(epic_name, business_goal, high_level_desc, task_type):
    # Step 1: Create User Story List Preview (output: lstUserStoryItemPreview)
    create_lst_user_story_preview_step(epic_name, business_goal, high_level_desc)
    # |
    # |
    # Step 2: Create User Story List Jira (output: lstUserStoryItem)
    create_list_user_story_jira_step()
    # |
    # |
    # Step 3: Create Task/SubTask List Preview (output: lstTaskItemPreview)
    create_lst_task_preview_step(task_type)
    # |
    # |
    # Step 4: Create Task/SubTask List Jira (output: lstTaskItem)
    create_task_jira_step()
    # |
    # |
    # Step 5: Create Confluence Estimate Document
    create_table_est_for_doc_step()
