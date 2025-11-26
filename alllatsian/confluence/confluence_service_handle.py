import re
from alllatsian.jira import jira_task_service_handle
from alllatsian.utils import genarate_plan, parser_content
from data.data_app import lstTaskItem, lstUserStoryItem
from utils.config import confluence_config


def agent_gen_estimate_doc(promt):
    status = confluence_config().create_page(
        space='BAAI',
        title='Page Gen 16',
        body=promt
    )

    s = str(status.get('_links'))
    regex = r"'webui': '(.*)', 'edituiv2'"
    match = re.findall(regex, s)
    parser_content.url_est_doc_full = "https://bidv-ba-assistant317.atlassian.net/wiki" + match[0]
    print(parser_content.url_est_doc_full)

    jira_task_service_handle.attach_link_confluence_to_task()


def create_table_est_for_doc_step():
    print("create_table_est_for_doc_step")
    lst_header = []
    table_body = ""
    for i in range(len(lstTaskItem)):
        item_task = lstTaskItem[i]
        if item_task.user_story_id not in lst_header:
            lst_header.append(item_task.user_story_id)
            table_body = table_body + genarate_plan.generate_row_header(i, item_task,
                                                                        get_title_by_id(item_task.user_story_id))
        else:
            table_body = table_body + genarate_plan.generate_row_normal(i, item_task)

    agent_gen_estimate_doc(genarate_plan.source_html_plan_doc(table_body))


def get_title_by_id(uid):
    title = ""
    for task in lstUserStoryItem:
        if uid == task.uid:
            title = task.title
            break

    return title
