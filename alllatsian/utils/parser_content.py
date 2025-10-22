import re
import time

from alllatsian.jira import jira_task_service_handle
from data.data_app import lstTaskItem
from model.task_item import TaskItem

regexTitle = r'#tit_start#(.*)#tit_end#'
regexContent = r'#des_start#(.*)#des_end#'
regexEstimate = r'#est_start#(.*)#est_end#'
regexTeam = r'#team_start#(.*)#team_end#'
regexNumber = r'\d+'
regexUrlDocEstimate = r"'webui': '(.*) ',"
url_est_doc_full = ""
# 'webui': '    ',


def parse_subtask(res, story_id, story_content):
    lst_sub_task_title = re.findall(regexTitle, res)
    lst_sub_task_content = re.findall(regexContent, res)
    lst_sub_task_estimate = re.findall(regexEstimate, res)
    lst_sub_task_team = re.findall(regexTeam, res)

    for i in range(len(lst_sub_task_title)):
        day_number = re.findall(regexNumber, lst_sub_task_estimate[i])[0]
        jira_task_service_handle.create_sub_task(story_id,
                                                 lst_sub_task_title[i],
                                                 lst_sub_task_content[i],
                                                 day_number,
                                                 lst_sub_task_team[i])

        task_item = TaskItem(story_content, lst_sub_task_title[i], lst_sub_task_content[i], lst_sub_task_team[i],
                             day_number)
        lstTaskItem.append(task_item)
        time.sleep(0.5)


def get_url_estimate_doc(res):
    lst_url = res.split("'webui': '")
    last_part_string = lst_url[len(lst_url) - 1]
    regex = r"(.*)', 'edituiv2':"
    match = re.findall(regex, last_part_string)
    print(match)
    return match
