import re
from atlassian import Confluence

from alllatsian.jira import jira_task_service_handle
from utils.constant import jira_api_token
from alllatsian.utils import genarate_plan, parser_content
from data.data_app import lstTaskItem, lstUserStoryItem

confluence = Confluence(
    url='https://bidv-vn.atlassian.net/wiki/',
    username="linhth8@bidv.com.vn",
    password=jira_api_token,
    cloud=True)


def agent_gen_estimate_doc(promt):
    status = confluence.create_page(
        space='KH0012024',
        title='Page Gen Planning',
        body=promt
    )

    s = str(status.get('_links'))
    regex = r"'webui': '(.*)', 'edituiv2'"
    match = re.findall(regex, s)
    parser_content.url_est_doc_full = "https://bidv-vn.atlassian.net/wiki" + match[0]
    print(parser_content.url_est_doc_full)

    jira_task_service_handle.attach_link_confluence_to_task()


def create_table_est_for_doc_step():
    print("create_table_est_for_doc_step")
    lst_header = []
    table_body = ""
    print("len(lstTaskItem): "+str(len(lstTaskItem)))
    for i in range(len(lstTaskItem)):
        item_task = lstTaskItem[i]
        print("item_task.user_story_id: "+item_task.user_story_id)
        if item_task.user_story_id not in lst_header:
            lst_header.append(item_task.user_story_id)
            table_body = table_body + genarate_plan.generate_row_header(i, item_task,
                                                                        get_title_by_id(item_task.user_story_id))
        else:
            table_body = table_body + genarate_plan.generate_row_normal(i, item_task)

    agent_gen_estimate_doc(genarate_plan.source_html_plan_doc(table_body))


def get_title_by_id(uid):
    title = ""
    print("len(lstUserStoryItem): " + str(len(lstUserStoryItem)))
    for task in lstUserStoryItem:
        if uid == task.uid:
            title = task.title
            break

    return title
