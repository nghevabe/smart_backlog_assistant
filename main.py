from alllatsian.confluence.confluence_service_handle import create_table_est_for_doc_step
from alllatsian.jira.jira_task_controller import create_lst_user_story_step, create_lst_task_step


def main_app(epic_name, business_goal, high_level_desc, task_type):
    # Step 1: Create User Story List (output: lstUserStory)
    create_lst_user_story_step(epic_name, business_goal, high_level_desc)
    # |
    # |
    # Step 2: Create Task List (output: lstTask)
    create_lst_task_step(task_type)
    # |
    # |
    # Step 3: Create Confluence Estimate Document
    create_table_est_for_doc_step()
