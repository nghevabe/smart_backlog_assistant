import re
from alllatsian.jira import jira_task_service_handle
from alllatsian.utils import genarate_plan, parser_content
from data.data_app import lstTaskItem, lstUserStoryItem, lstTaskItemPreview
from utils.config import confluence_config
from datetime import datetime



def agent_gen_estimate_doc(promt):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    status = confluence_config().create_page(
        space="BAAI",
        title=f"[GEN{timestamp}] Effort Estimation Document",
        body=promt
    )

    s = str(status.get('_links'))
    regex = r"'webui': '(.*)', 'edituiv2'"
    match = re.findall(regex, s)
    parser_content.url_est_doc_full = "https://bidv-ba-assistant2026.atlassian.net/wiki" + match[0]
    print(parser_content.url_est_doc_full)

    jira_task_service_handle.attach_link_confluence_to_task()


def create_table_est_for_doc_step():

    total_manday = 0
    web_manday = 0
    mobile_manday = 0
    backend_manday = 0
    uiux_manday = 0
    qc_manday = 0
    print("create_table_est_for_doc_step")

    lst_header = []
    table_body = ""
    for i in range(len(lstTaskItem)):
        item_task = lstTaskItem[i]

        total_manday = total_manday + int(item_task.manday)
        if item_task.team == 'Web':
            web_manday = web_manday + int(item_task.manday)
        if item_task.team == 'Mobile':
            mobile_manday = mobile_manday + int(item_task.manday)
        if item_task.team == 'Backend':
            backend_manday = backend_manday + int(item_task.manday)
        if item_task.team == 'UI/UX':
            uiux_manday = uiux_manday + int(item_task.manday)
        if item_task.team == 'QC':
            qc_manday = qc_manday + int(item_task.manday)

        if item_task.user_story_id not in lst_header:
            lst_header.append(item_task.user_story_id)
            table_body = table_body + genarate_plan.generate_row_header(i, item_task,
                                                                        get_title_by_id(item_task.user_story_id))
        else:
            table_body = table_body + genarate_plan.generate_row_normal(i, item_task)

    agent_gen_estimate_doc(
        genarate_plan.source_html_plan_doc(table_body, total_manday, web_manday, mobile_manday, backend_manday,
                                           uiux_manday, qc_manday))


def get_title_by_id(uid):
    title = ""
    for task in lstUserStoryItem:
        if uid == task.uid:
            title = task.title
            break

    return title


def create_table_est_for_doc_step_demo():
    total_manday = 0
    web_manday = 0
    mobile_manday = 0
    backend_manday = 0
    uiux_manday = 0
    qc_manday = 0

    print("create_table_est_for_doc_step_demo")
    lst_header = []
    table_body = ""
    for i in range(len(lstTaskItemPreview)):
        item_task = lstTaskItemPreview[i]

        total_manday = total_manday + int(item_task.manday)
        if item_task.team == 'Web':
            web_manday = web_manday + int(item_task.manday)
        if item_task.team == 'Mobile':
            mobile_manday = mobile_manday + int(item_task.manday)
        if item_task.team == 'Backend':
            backend_manday = backend_manday + int(item_task.manday)
        if item_task.team == 'UI/UX':
            uiux_manday = uiux_manday + int(item_task.manday)
        if item_task.team == 'QC':
            qc_manday = qc_manday + int(item_task.manday)

        if item_task.user_story_id not in lst_header:
            lst_header.append(item_task.user_story_id)
            table_body = table_body + genarate_plan.generate_row_header(i, item_task,
                                                                        get_title_by_id(item_task.user_story_id))
        else:
            table_body = table_body + genarate_plan.generate_row_normal(i, item_task)

    print("XXX_total_manday: " + str(total_manday))
    agent_gen_estimate_doc(
        genarate_plan.source_html_plan_doc(table_body, total_manday, web_manday, mobile_manday, backend_manday,
                                           uiux_manday, qc_manday))
