import time

from alllatsian.jira.jira_task_preview_handle import agent_gen_sub_task_preview
from data.data_app import lstUserStoryItem, lstTaskItemPreview


def create_lst_task_preview_step(task_type):
    lstTaskItemPreview.clear()
    print("create_lst_task_preview_step: "+str(len(lstUserStoryItem)))
    for i in range(len(lstUserStoryItem)):
        print("ZZZ_lstUserStoryItem[i].title: " + str(lstUserStoryItem[i].title))
        if 'FOUNDATION' in lstUserStoryItem[i].title:
            print("ZZZ_lstUserStoryItem[i].FOUNDATIONED")
            agent_gen_sub_task_preview(lstUserStoryItem[i].uid,
                                       lstUserStoryItem[i].full_description, 'FOUNDATION')
        else:
            agent_gen_sub_task_preview(lstUserStoryItem[i].uid,
                                       lstUserStoryItem[i].full_description, 'FEATURE')

        time.sleep(1.0)
