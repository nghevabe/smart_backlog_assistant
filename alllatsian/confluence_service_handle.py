import re
from atlassian import Confluence
from utils.constant import jira_api_token
from alllatsian import jira_service_handle, genarate_plan
from utils import parser_content
from data.data_app import lstUserStory, lstTask

confluence = Confluence(
    url='https://bidv-ba-assistant317.atlassian.net/wiki',
    username="tranhoanglinh317@gmail.com",
    password=jira_api_token,
    cloud=True)


def agent_gen_estimate_doc(promt):
    status = confluence.create_page(
        space='BAAI',
        title='Page Gen 15',
        body=promt
    )

    s = str(status.get('_links'))
    regex = r"'webui': '(.*)', 'edituiv2'"
    match = re.findall(regex, s)
    parser_content.url_est_doc_full = "https://bidv-ba-assistant317.atlassian.net/wiki" + match[0]
    print(parser_content.url_est_doc_full)

    jira_service_handle.attach_link_confluence_to_task()


def create_table_est_for_doc_step():
    lst_header = []
    table_body = ""
    for i in range(len(lstTask)):
        item_task = lstTask[i]
        if item_task.user_story not in lst_header:
            table_body = table_body + genarate_plan.generate_row_header(i, item_task)
            lst_header.append(item_task.user_story)
        else:
            table_body = table_body + genarate_plan.generate_row_normal(i, item_task)

    agent_gen_estimate_doc(genarate_plan.source_html_plan_doc(table_body))
