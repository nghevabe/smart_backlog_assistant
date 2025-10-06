import time
from jira import JIRA
from openai import OpenAI
from utils import parser_content, constant
from utils.constant import jira_api_token, model_config, user_config
from data.data_app import lstUserStory
from model.user_story_item import UserStoryItem
from utils.promts import promt_im_pmo_want_create_us, promt_create_content_subtask_feature, \
    promt_create_content_subtask_project

# Define your JIRA server and credentials
jira_server = 'https://bidv-ba-assistant317.atlassian.net'
jira_username = 'tranhoanglinh317@gmail.com'
# Connect to JIRA
jira = JIRA(server=jira_server, basic_auth=(jira_username, jira_api_token))
# list UserStoryItem
client = OpenAI(api_key=constant.open_api_key)


def update_task_test():
    issue = jira.issue('SCRUM-2')
    issue.update(update={"description": [{"set": "Test Update"}]})


def update_task():
    issue = jira.issue('SCRUM-17')
    issue.update(update={"timetracking": [{"edit": {"originalEstimate": "3d"}}]})


def agent_gen_sub_task_for_new_feature(story_id, story_content, promt):
    content_head = promt_im_pmo_want_create_us
    content_foot = promt_create_content_subtask_feature
    full_content = content_head + "' " + promt + " '" + content_foot

    completion = client.chat.completions.create(
        model=model_config,
        messages=[
            {"role": user_config, "content": full_content}
        ]
    )

    response_data = completion.choices[0].message.content
    parser_content.parse_subtask(response_data, story_id, story_content)

    return response_data


def agent_gen_sub_task_for_new_project(story_id, story_content, promt):
    content_head = promt_im_pmo_want_create_us
    content_foot = promt_create_content_subtask_project
    full_content = content_head + "' " + promt + " '" + content_foot

    completion = client.chat.completions.create(
        model=model_config,
        messages=[
            {"role": user_config, "content": full_content}
        ]
    )

    response_data = completion.choices[0].message.content
    parser_content.parse_subtask(response_data, story_id, story_content)

    return response_data


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


def agent_gen_user_story(epic_name, business_goal, high_level_desc):
    promt = f"""Tôi là 1 BA, hãy tự sinh ra từ 2 hoặc 3 User Story tuỳ thuộc vào nội dung và phải theo chuẩn Agile.
Đây là các thông tin tôi cũng cấp:
- Epic Name: {epic_name}
- Business Goal: {business_goal}
- High-level Description: {high_level_desc}

Output sẽ theo form như sau:
#begin_response#
Title: #tit_start#title here#tit_end#
Description: #des_start#description here#des_end#
Acceptance Criteria:
#start#
acceptance criteria here
#end#
"""

    completion = client.chat.completions.create(
        model=model_config,
        messages=[
            {"role": user_config,
             "content": promt
             }
        ]
    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content


def create_lst_user_story_step(epic_name, business_goal, high_level_desc):
    res = agent_gen_user_story(epic_name,
                               business_goal,
                               high_level_desc)
    lst_story = res.split("#begin_response#")

    for story in lst_story:
        if "#start#" in story:
            title_str = story.split("#tit_start#")[1]
            title = title_str.split("#tit_end#")[0].strip()

            content_str = story.split("#des_start#")[1]
            content = content_str.split("#des_end#")[0].strip()

            criteria_str = story.split("#start#")[1]
            criteria = criteria_str.split("#end#")[0].strip()

            create_user_story_item(title, content, criteria)
            time.sleep(0.5)


def create_lst_task_step(task_type):
    for i in range(len(lstUserStory)):
        if task_type == "1":
            agent_gen_sub_task_for_new_project(lstUserStory[i].uid,
                                               lstUserStory[i].title,
                                               lstUserStory[i].full_description)
        else:
            agent_gen_sub_task_for_new_feature(lstUserStory[i].uid,
                                               lstUserStory[i].title,
                                               lstUserStory[i].full_description)


def attach_link_confluence_to_task():
    for i in range(len(lstUserStory)):
        issue = jira.issue(lstUserStory[i].uid)
        new_content = lstUserStory[
                          i].full_description + "\n\n" + " - Link Kế Hoạch và Khái Toán: " + parser_content.url_est_doc_full
        issue.update(update={"description": [{"set": new_content}]})

