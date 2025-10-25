from utils import constant


def init_config(jira_project_space_selected):
    constant.jira_project_space = jira_project_space_selected
    constant.alllatsian_id_namespace = "https://bidv-vn.atlassian.net"
    constant.confluence_namespace = "KH0012024"
    constant.alllatsian_username = "linhth8@bidv.com.vn"
    print("constant.jira_project_space: "+constant.jira_project_space)
