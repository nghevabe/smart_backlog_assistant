from openai import OpenAI

import time
from utils.constant import model_config, user_config
from alllatsian import genarate_plan
from utils import parser_content
from alllatsian.confluence_service_handle import agent_gen_estimate_doc
from data.data_app import lstUserStory, lstTask
from alllatsian.jira_service_handle import create_user_story_item
from utils.promts import promt_create_content_subtask_feature, promt_create_content_subtask_project, \
    promt_im_pmo_want_create_us

client = OpenAI(
    api_key="api_key")


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


def agent_gen_estimate_doc_source_html(promt):
    completion = client.chat.completions.create(
        model=model_config,
        messages=[
            {"role": user_config,
             "content": promt}
        ]
    )
    return completion.choices[0].message.content


def agent_gen_sub_task_for_new_feature(story_id, story_content, promt):
    content_head = promt_im_pmo_want_create_us
    content_foot = promt_create_content_subtask_feature
    full_content = content_head + "' " + promt + " '" + content_foot
    completion = client.chat.completions.create(
        model=model_config,
        messages=[
            {"role": user_config, "content": full_content}
        ]
    )

    response_data = completion.choices[0].message.content
    parser_content.parse_subtask(response_data, story_id, story_content)

    return response_data


def agent_gen_sub_task_for_new_project(story_id, story_content, promt):
    content_head = promt_im_pmo_want_create_us
    content_foot = promt_create_content_subtask_project
    full_content = content_head + "' " + promt + " '" + content_foot
    completion = client.chat.completions.create(
        model=model_config,
        messages=[
            {"role": user_config, "content": full_content}
        ]
    )

    response_data = completion.choices[0].message.content
    parser_content.parse_subtask(response_data, story_id, story_content)

    return response_data


def main_app(epic_name, business_goal, high_level_desc, task_type):
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

            create_user_story_item(title, content, criteria)
            time.sleep(0.5)

    for i in range(len(lstUserStory)):
        if task_type == "1":
            agent_gen_sub_task_for_new_project(lstUserStory[i].uid,
                                               lstUserStory[i].title,
                                               lstUserStory[i].full_description)
        else:
            agent_gen_sub_task_for_new_feature(lstUserStory[i].uid,
                                               lstUserStory[i].title,
                                               lstUserStory[i].full_description)

    lst_header = []
    table_body = ""
    for i in range(len(lstTask)):
        item_task = lstTask[i]
        if item_task.user_story not in lst_header:
            table_body = table_body + genarate_plan.generate_row_header(i, item_task)
            lst_header.append(item_task.user_story)
        else:
            table_body = table_body + genarate_plan.generate_row_normal(i, item_task)

    print("Start table_body")
    print(table_body)
    print("table_body End")

    agent_gen_estimate_doc(genarate_plan.source_html_plan_doc(table_body))

# main_app("tính năng quản lý ATM",
#                            "cho phép các cán bộ ngân hàng có thể quản lý trạng thái, vị trí và lượng tiền mặt trong mỗi cây atm",
#                            "Bao gồm các tính năng như xem danh sách các cây ATM, kiểm tra trạng thái, kiểm tra lượng tiền mặt trong cây ATM 1 cách nhanh chóng và tiện lợi qua Web và ứng dụng Mobile")
