from jira import JIRA

from utils import parser_content
from utils.constant import jira_api_token
from data.data_app import lstUserStory
from model.user_story_item import UserStoryItem

# Define your JIRA server and credentials
jira_server = 'https://bidv-ba-assistant317.atlassian.net'
jira_username = 'tranhoanglinh317@gmail.com'
# Connect to JIRA
jira = JIRA(server=jira_server, basic_auth=(jira_username, jira_api_token))
# list UserStoryItem



def update_task_test():
    issue = jira.issue('SCRUM-2')
    issue.update(update={"description": [{"set": "Test Update"}]})


def update_task():
    issue = jira.issue('SCRUM-17')
    issue.update(update={"timetracking": [{"edit": {"originalEstimate": "3d"}}]})


def create_user_story_item(title, content, criteria):
    full_description = content + "\n\n" + "Acceptance Criteria:" + "\n" + criteria
    issue_dict = {
        'project': {'key': 'SCRUM'},  # Replace with your project key
        'summary': title,
        'description': full_description,
        'issuetype': {'name': 'Story'},  # Replace with the desired issue type
    }

    # Create the issue
    new_issue = jira.create_issue(fields=issue_dict)

    user_story_item = UserStoryItem(uid=new_issue.key, title=title, content=content, criteria=criteria)
    lstUserStory.append(user_story_item)

    # Print the new issue key
    print(f'Created new issue: {new_issue.key}')


def create_sub_task(parent_id, title, content, estimate, team):
    subtask = {
        "project":
            {
                "key": "SCRUM"
            },
        "parent":
            {
                "key": parent_id
            },
        "summary": "[" + team + "]" + "[" + parent_id + "] " + title,
        "description": content,
        "issuetype":
            {
                "name": "SubTask"
            },
        "timetracking": {
            "originalEstimate": estimate + "d"
        },
    }

    # Create the issue
    new_issue = jira.create_issue(fields=subtask)

    # Print the new issue key
    print(f'Created Sub Task: {new_issue.key}')


def attach_link_confluence_to_task():
    for i in range(len(lstUserStory)):
        issue = jira.issue(lstUserStory[i].uid)
        new_content = lstUserStory[
                          i].full_description + "\n\n" + " - Link Kế Hoạch và Khái Toán: " + parser_content.url_est_doc_full
        issue.update(update={"description": [{"set": new_content}]})

