from atlassian import Confluence
from flask import session


def get_confluence():
    ns = session.get("jira_namespace")
    email = session.get("jira_email")
    token = session.get("jira_api_token")

    if not ns or not email or not token:
        raise Exception("Jira chưa được cấu hình – thiếu namespace/email/token")

    return Confluence(
        url=ns.rstrip("/") + "/wiki",
        username=email,
        password=token,
        cloud=True
    )