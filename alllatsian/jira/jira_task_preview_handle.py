import re
from openai import OpenAI
from alllatsian.utils.parser_content import regexTitle, regexContent, regexEstimate, regexTeam, regexNumber
from data.data_app import lstUserStoryPreview, lstTaskItemPreview
from model.task_item import TaskItem
from model.user_story_item import UserStoryItem
from utils import constant
from utils.constant import model_config, user_config
from utils.promts import promt_im_pmo_want_create_us, promt_create_content_subtask_feature, \
    promt_create_content_subtask_project

client = OpenAI(api_key=constant.open_api_key)


def agent_gen_user_story(epic_name, business_goal, high_level_desc):
    promt = f"""Tôi là 1 BA, hãy tự sinh ra từ 2 hoặc 3 User Story tuỳ thuộc vào nội dung và phải theo chuẩn Agile.
Đây là các thông tin tôi cũng cấp:
- Epic Name: {epic_name}
- Business Goal: {business_goal}
- High-level Description: {high_level_desc}

Output sẽ theo form như sau:
#begin_response#
Title: #tit_start#title here#tit_end#
Description: #des_start#description here#des_end#
Acceptance Criteria:
#start#
acceptance criteria here
#end#
"""

    completion = client.chat.completions.create(
        model=model_config,
        messages=[
            {"role": user_config,
             "content": promt
             }
        ]
    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content


def create_lst_user_story_preview_step(epic_name, business_goal, high_level_desc):
    res = agent_gen_user_story(epic_name,
                               business_goal,
                               high_level_desc)
    lst_story = res.split("#begin_response#")

    for story in lst_story:
        if "#start#" in story:
            title_str = story.split("#tit_start#")[1]
            title = title_str.split("#tit_end#")[0].strip()

            content_str = story.split("#des_start#")[1]
            content = content_str.split("#des_end#")[0].strip()

            criteria_str = story.split("#start#")[1]
            criteria = criteria_str.split("#end#")[0].strip()

            us_preview = UserStoryItem(title=title, content=content, criteria=criteria, uid='')
            lstUserStoryPreview.append(us_preview)

    return lstUserStoryPreview


def agent_gen_sub_task_preview(story_id, promt, requirement_type):
    content_head = promt_im_pmo_want_create_us

    if requirement_type == "1":
        content_foot = promt_create_content_subtask_project
    else:
        content_foot = promt_create_content_subtask_feature
    full_content = content_head + "' " + promt + " '" + content_foot

    completion = client.chat.completions.create(
        model=model_config,
        messages=[
            {"role": user_config, "content": full_content}
        ]
    )

    print("agent_gen_sub_task_preview_start:")
    response_data = completion.choices[0].message.content

    lst_sub_task_title = re.findall(regexTitle, response_data)
    lst_sub_task_content = re.findall(regexContent, response_data)
    lst_sub_task_estimate = re.findall(regexEstimate, response_data)
    lst_sub_task_team = re.findall(regexTeam, response_data)

    print("lst_sub_task_title: "+str(len(lst_sub_task_title)))
    for i in range(len(lst_sub_task_title)):
        day_number = re.findall(regexNumber, lst_sub_task_estimate[i])[0]

        task_item = TaskItem(user_story_id=story_id, title=lst_sub_task_title[i], des=lst_sub_task_content[i],
                             team=lst_sub_task_team[i],
                             manday=day_number)
        lstTaskItemPreview.append(task_item)
