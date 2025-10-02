import re
from atlassian import Confluence
from utils.constant import jira_api_token
from alllatsian import jira_service_handle
from utils import parser_content

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


# "https://bidv-ba-assistant317.atlassian.net/wiki/spaces/BAAI/pages/8028200/Page+Gen+12"