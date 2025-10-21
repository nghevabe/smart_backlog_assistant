import time

from alllatsian.jira.jira_task_preview_handle import agent_gen_sub_task_preview
from data.data_app import lstUserStoryItem


def create_lst_task_preview_step(task_type):
    print("create_lst_task_preview_step: "+str(len(lstUserStoryItem)))
    for i in range(len(lstUserStoryItem)):
        agent_gen_sub_task_preview(lstUserStoryItem[i].uid,
                                   lstUserStoryItem[i].full_description, task_type)
        time.sleep(1.0)
