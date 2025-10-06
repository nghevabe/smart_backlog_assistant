import time

from alllatsian.jira.jira_task_service_handle import create_user_story_item
from alllatsian.jira.jira_task_preview_handle import agent_gen_user_story, agent_gen_sub_task_for_new_project, \
    agent_gen_sub_task_for_new_feature
from data.data_app import lstUserStory


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