import time
from datetime import date, timedelta

from jira import JIRA
from openai import OpenAI

from model.task_item import TaskItem
from utils import constant
from alllatsian.utils import parser_content
from utils.constant import jira_api_token, alllatsian_id_namespace, alllatsian_username, jira_project_space
from data.data_app import lstUserStoryItem, lstUserStoryPreview, lstTaskItem, lstTaskItemPreview
from model.user_story_item import UserStoryItem

# Connect to JIRA
jira = JIRA(server=alllatsian_id_namespace, basic_auth=(alllatsian_username, jira_api_token))
# list UserStoryItem
client = OpenAI(api_key=constant.open_api_key)


def create_list_user_story_jira_step():
    for user_story in lstUserStoryPreview:
        create_user_story_item(user_story)
        time.sleep(0.5)


def create_user_story_item(user_story_item):
    title = user_story_item.title
    content = user_story_item.content
    criteria = user_story_item.criteria

    start_date = date.today().isoformat()
    due_date = (date.today() + timedelta(days=10)).isoformat()

    full_description = content + "\n\n" + "Acceptance Criteria:" + "\n" + criteria
    issue_dict = {
        'project': {'key': jira_project_space},
        'summary': title,
        'description': full_description,
        'issuetype': {'name': 'Story'},
        'customfield_10035': start_date,
        'duedate': due_date,
        'assignee': {'id': None}
    }

    # Create the issue
    new_issue = jira.create_issue(fields=issue_dict)

    user_story_item = UserStoryItem(uid=new_issue.key, title=title, content=content, criteria=criteria)
    lstUserStoryItem.append(user_story_item)

    # Print the new issue key
    print(f'Created new issue: {new_issue.key}')


def create_sub_task(parent_id, title, content, estimate, team):

    start_date = date.today().isoformat()
    due_date = (date.today() + timedelta(days=10)).isoformat()

    subtask = {
        "project":
            {
                "key": jira_project_space
            },
        "parent":
            {
                "key": parent_id
            },
        "summary": "[" + team + "]" + "[" + parent_id + "] " + title,
        "description": content,
        "issuetype":
            {
                "name": "Sub-task"
            },
        "timetracking": {
            "originalEstimate": estimate + "d"
        },
        "customfield_10035": start_date,
        "duedate": due_date,
        "components": [{"id": "11284"}],
        "customfield_10084": {"value": "UI/UX_Thiết kế cho các PM trung bình"},
        'assignee': {'id': None}
    }

    # Create the issue
    new_issue = jira.create_issue(fields=subtask)
    # Print the new issue key
    print(f'Created Sub Task: {new_issue.key}')

    task_item = TaskItem(user_story_id=parent_id, title=title, des=content,
                         team=team,
                         manday=estimate)

    lstTaskItem.append(task_item)


def create_task_jira_step():
    print("lstTaskItemPreview: "+str(len(lstTaskItemPreview)))
    for task in lstTaskItemPreview:
        create_sub_task(task.user_story_id, task.title, task.des, task.manday, task.team)
        time.sleep(0.5)


def attach_link_confluence_to_task():
    for i in range(len(lstUserStoryItem)):
        issue = jira.issue(lstUserStoryItem[i].uid)
        new_content = lstUserStoryItem[
                          i].full_description + "\n\n" + " - Link Kế Hoạch và Khái Toán: " + parser_content.url_est_doc_full
        issue.update(update={"description": [{"set": new_content}]})
