import time

from alllatsian.jira.jira_task_preview_handle import agent_gen_sub_task_preview
from data.data_app import lstUserStoryItem, lstTaskItemPreview


def create_lst_task_preview_step(language):
    lstTaskItemPreview.clear()

    for i in range(len(lstUserStoryItem)):

        if 'FOUNDATION' in lstUserStoryItem[i].title:
            print("ZZZ_lstUserStoryItem[i].FOUNDATIONED")
            agent_gen_sub_task_preview(lstUserStoryItem[i].uid,
                                       lstUserStoryItem[i].full_description, 'FOUNDATION', language)
        else:
            agent_gen_sub_task_preview(lstUserStoryItem[i].uid,
                                       lstUserStoryItem[i].full_description, 'FEATURE', language)

        time.sleep(1.0)
