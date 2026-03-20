import re
from openai import OpenAI
from alllatsian.utils.parser_content import regexTitle, regexContent, regexEstimate, regexTeam, regexNumber
from data.data_app import lstUserStoryPreview, lstTaskItemPreview
from model.task_item import TaskItem
from model.user_story_item import UserStoryItem
from utils import constant
from utils.constant import model_config, user_config
from utils.promts import promt_im_pmo_want_create_us, promt_create_content_subtask_feature, \
    promt_create_content_subtask_project, promt_create_content_subtask_foundation

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
    return completion.choices[0].message.content


def agent_gen_user_story_foundation(document_content_input, language):
    promt = f"""
Bạn là một Business Analyst chuyên nghiệp trong dự án phát triển phần mềm Agile.

Nhiệm vụ của bạn:
Phân tích tài liệu URD và tạo ra các User Story theo chuẩn Agile.

--------------------------------
INPUT DATA
--------------------------------

Nội dung tài liệu URD:
{document_content_input}

Ngôn ngữ đầu ra:
{language}

--------------------------------
QUY TẮC PHÂN TÍCH URD
--------------------------------

1. Phải đọc kỹ nội dung URD để xác định các màn hình (screens) được mô tả.

2. Một màn hình chỉ được tạo ra đúng 1 User Story.

3. Không được tạo thêm màn hình hoặc chức năng không tồn tại trong tài liệu.

4. Không được suy diễn hoặc tưởng tượng thêm chức năng.

5. Không được tách nhỏ User Story quá chi tiết.

6. Mỗi User Story phải đại diện cho chức năng chính của một màn hình.

--------------------------------
FOUNDATION USER STORY RULE
--------------------------------

Phải tạo thêm đúng 1 Foundation User Story.

Foundation User Story có mục đích:
Thiết lập nền tảng kỹ thuật cho dự án trước khi phát triển các chức năng.

Foundation User Story có thể bao gồm các hoạt động như:

- Setup project structure
- Base theme / design system
- Network configuration
- Shared UI components
- Base architecture

Foundation User Story:

- Không gắn với màn hình cụ thể
- Chỉ được xuất hiện đúng 1 lần
- Phải nằm ở vị trí đầu tiên trong danh sách User Story
- Title phải bắt đầu bằng tiền tố [FOUNDATION]

--------------------------------
QUY TẮC SỐ LƯỢNG USER STORY
--------------------------------

Tổng số User Story phải bằng:

TOTAL_USER_STORY =
SỐ_MÀN_HÌNH_TRONG_URD + 1

User Story đầu tiên phải là Foundation User Story.

Các User Story còn lại phải tương ứng với từng màn hình trong URD.

Không được tạo nhiều hơn hoặc ít hơn số lượng này.

--------------------------------
TITLE PREFIX RULE
--------------------------------

Để phân biệt loại User Story, Title phải có tiền tố như sau:

Foundation User Story:

Title phải bắt đầu bằng

[FOUNDATION]

Ví dụ:

[FOUNDATION] Thiết lập nền tảng dự án

Feature User Story:

Title phải bắt đầu bằng

[FEATURE]

Ví dụ:

[FEATURE] Màn hình tìm kiếm báo cáo

Không được bỏ tiền tố này.

--------------------------------
YÊU CẦU NGÔN NGỮ
--------------------------------

Nếu {language} = "vi":

Toàn bộ output phải viết bằng tiếng Việt.

User Story format:

Là một <vai trò người dùng>  
Tôi muốn <chức năng>  
Để <giá trị mang lại>

Nếu {language} = "en":

Toàn bộ output phải viết bằng English.

User Story format:

As a <user role>  
I want <function>  
So that <business value>

--------------------------------
ACCEPTANCE CRITERIA RULE
--------------------------------

Acceptance Criteria phải:

- Rõ ràng
- Có thể kiểm thử được
- Mỗi dòng một điều kiện

Không viết quá dài.

--------------------------------
FORMAT OUTPUT BẮT BUỘC
--------------------------------

Mỗi User Story phải bắt đầu bằng:

#begin_response#

Không được viết bất kỳ giải thích nào ngoài format.

--------------------------------
FORMAT OUTPUT
--------------------------------

#begin_response#
Title: #tit_start#[FEATURE] title here#tit_end#

Description:
#des_start#
user story description
#des_end#

Acceptance Criteria:
#start#
criteria 1
criteria 2
criteria 3
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
    # print(completion.choices[0].message.content)
    return completion.choices[0].message.content


def create_lst_user_story_preview_step(document_content_input, include_foundation, language):
    lstUserStoryPreview.clear()
    if str(include_foundation).lower() == 'true':
        print("XXX_include_foundation_value OK ")
        res = agent_gen_user_story_foundation(document_content_input, language)
    else:
        print("XXX_include_foundation_value NOT ")
        res = agent_gen_user_story_feature(document_content_input, language)
    print("XXX_res_us: "+str(res))
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


def agent_gen_sub_task_preview(story_id, promt, requirement_type, language):

    if requirement_type == "FOUNDATION":
        full_content = promt_create_content_subtask_foundation(promt, language=language)
    else:
        full_content = promt_create_content_subtask_project(promt, language=language)

    print("ZZZ_full_content: "+str(full_content))

    completion = client.chat.completions.create(
        model=model_config,
        messages=[
            {"role": user_config, "content": full_content}
        ]
    )

    response_data = completion.choices[0].message.content

    print("XXX_res_sub_task: "+str(response_data))

    print("response_data: "+response_data)

    lst_sub_task_title = re.findall(regexTitle, response_data)
    lst_sub_task_content = re.findall(regexContent, response_data)
    lst_sub_task_estimate = re.findall(regexEstimate, response_data)
    lst_sub_task_team = re.findall(regexTeam, response_data)

    for i in range(len(lst_sub_task_title)):
        day_number = re.findall(regexNumber, lst_sub_task_estimate[i])[0]

        task_item = TaskItem(user_story_id=story_id, title=lst_sub_task_title[i], des=lst_sub_task_content[i],
                             team=lst_sub_task_team[i],
                             manday=day_number)
        lstTaskItemPreview.append(task_item)


def agent_gen_user_story_feature(document_content_input, language):
    promt = f"""
Bạn là một Business Analyst chuyên nghiệp trong dự án phát triển phần mềm Agile.

Nhiệm vụ của bạn:
Phân tích tài liệu URD và tạo ra các User Story theo chuẩn Agile.

--------------------------------
INPUT DATA
--------------------------------

Nội dung tài liệu URD:
{document_content_input}

Ngôn ngữ đầu ra:
{language}

--------------------------------
QUY TẮC PHÂN TÍCH URD
--------------------------------

1. Phải đọc kỹ nội dung URD để xác định các màn hình (screens) được mô tả.

2. Một màn hình chỉ được tạo ra đúng 1 User Story.

3. Không được tạo thêm màn hình hoặc chức năng không tồn tại trong tài liệu.

4. Không được suy diễn hoặc tưởng tượng thêm chức năng.

5. Không được tách nhỏ User Story quá chi tiết.

6. Mỗi User Story phải đại diện cho chức năng chính của một màn hình.

--------------------------------
QUY TẮC SỐ LƯỢNG USER STORY
--------------------------------

Tổng số User Story phải bằng:

TOTAL_USER_STORY =
SỐ_MÀN_HÌNH_TRONG_URD

Không được tạo nhiều hơn hoặc ít hơn số lượng này.

--------------------------------
TITLE PREFIX RULE
--------------------------------

Tất cả User Story phải có tiền tố:

[FEATURE]

Ví dụ:

[FEATURE] Màn hình tìm kiếm báo cáo

Không được bỏ tiền tố này.

--------------------------------
YÊU CẦU NGÔN NGỮ
--------------------------------

Nếu {language} = "vi":

Toàn bộ output phải viết bằng tiếng Việt.

User Story format:

Là một <vai trò người dùng>  
Tôi muốn <chức năng>  
Để <giá trị mang lại>

Nếu {language} = "en":

Toàn bộ output phải viết bằng English.

User Story format:

As a <user role>  
I want <function>  
So that <business value>

--------------------------------
ACCEPTANCE CRITERIA RULE
--------------------------------

Acceptance Criteria phải:

- Rõ ràng
- Có thể kiểm thử được
- Mỗi dòng một điều kiện

Không viết quá dài.

--------------------------------
FORMAT OUTPUT BẮT BUỘC
--------------------------------

Mỗi User Story phải bắt đầu bằng:

#begin_response#

Không được viết bất kỳ giải thích nào ngoài format.

--------------------------------
FORMAT OUTPUT
--------------------------------

#begin_response#
Title: #tit_start#[FEATURE] title here#tit_end#

Description:
#des_start#
user story description
#des_end#

Acceptance Criteria:
#start#
criteria 1
criteria 2
criteria 3
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
    # print(completion.choices[0].message.content)
    return completion.choices[0].message.content