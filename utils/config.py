from atlassian import Confluence
from flask import session
from jira import JIRA


def confluence_config():
    ns = session.get("atlassian_namespace")
    email = session.get("atlassian_user")
    token = session.get("atlassian_api_token")

    if not ns or not email or not token:
        raise Exception("Jira chưa được cấu hình – thiếu namespace/email/token")

    return Confluence(
        url=ns.rstrip("/") + "/wiki",
        username=email,
        password=token,
        cloud=True
    )


def jira_config():
    ns = session.get("atlassian_namespace")
    email = session.get("atlassian_user")
    token = session.get("atlassian_api_token")

    if not ns or not email or not token:
        raise Exception("Jira chưa được cấu hình – thiếu namespace/email/token")

    return JIRA(server=ns, basic_auth=(email, token))