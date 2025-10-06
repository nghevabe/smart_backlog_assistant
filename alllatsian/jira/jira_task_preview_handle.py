from openai import OpenAI
from utils import constant
from alllatsian.utils import parser_content
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