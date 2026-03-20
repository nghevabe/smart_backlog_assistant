promt_create_content_subtask_feature = """
Giờ tôi muốn tạo ra ngẫu nhiên từ 12 đến 16 SubTask con của User Story và Estimate thời gian cho chúng. Phải tạo riêng từng task để cho 5 Team như Web, Mobile, Backend, UI/UX, QC. Các Task cho mỗi Team phải có ít nhất các tiêu chí sau:
-	Web:
+ Dựng UI các màn hình (nói cụ thể màn nào)
+ Code Logic và ghép API cho các màn (nói cụ thể màn nào)

-	Mobile:
+ Dựng UI các màn hình (nói cụ thể từng màn)
+ Code Logic và ghép API cho các màn (nói cụ thể từng màn)

-	Backend:
+ Viết đặc tả API (cụ thể api nào)
+ Viết logic và cung cấp api (cụ thể từng api)

-	UI/UX:
+ Thiết kế các màn hình (cụ thể từng màn hình)

-	QC:
+ Viết TestCase cho các màn hình
+ Test các màn hình.

Response trả ra phải có đủ 4 thông tin và format có các ký tự đặc biệt để thuận lợi cho việc parsing như sau:
Title: @title here@ Description: ^description here^ Estimate day: ++estimate day here++ Team(Web or Mobile or Backend or UI/UX or QC): --team here--
"""


def promt_create_content_subtask_project(
    user_story: str,
    language: str = "vi"  # "vi" hoặc "en"
) -> str:
    lang_text = "Tiếng Việt" if language == "vi" else "English"

    return f"""
Bạn là một Technical Project Manager trong dự án phát triển phần mềm Agile.

Nhiệm vụ:
Dựa trên User Story được cung cấp, hãy tạo các SubTask kỹ thuật chi tiết.

--------------------------------
INPUT
--------------------------------

User Story:
{user_story}

--------------------------------
QUY TẮC NGÔN NGỮ (BẮT BUỘC)
--------------------------------

1. Nội dung output là {lang_text}.

2. KHÔNG được trộn lẫn nhiều ngôn ngữ.

3. Nếu vi phạm, phải tự động sửa lại trước khi trả kết quả.

4. Các thuật ngữ kỹ thuật phổ biến như API, UI, UX, Mobile, Web, Endpoint, Backend, QC,... được phép giữ nguyên.
--------------------------------
QUY TẮC CHUNG
--------------------------------

1. Phải tạo từ **15 đến 20 SubTask**.

2. SubTask phải được phân bổ cho đúng 5 team:

Web  
Mobile  
Backend  
UI/UX  
QC  

3. Mỗi team phải có ít nhất **2 SubTask**.

4. Không được bỏ sót bất kỳ team nào.

5. Không được tạo task chung chung, mỗi task phải rõ ràng và cụ thể.

6. Mỗi SubTask phải là một dòng độc lập.

--------------------------------
QUY TẮC TASK CHO TỪNG TEAM
--------------------------------

Web:

- Dựng UI cho màn hình cụ thể trong User Story
- Code logic và tích hợp API cho màn hình

Mobile:

- Dựng UI cho màn hình cụ thể trong User Story
- Code logic và tích hợp API cho màn hình

Backend:

- Viết đặc tả API (ghi rõ API)
- Viết logic xử lý và triển khai API

UI/UX:

- Thiết kế UI cho màn hình cụ thể

QC:

- Viết Test Case
- Thực hiện test chức năng

--------------------------------
QUY TẮC ESTIMATE
--------------------------------

Estimate phải là số hợp lệ trong danh sách:

0.5  
1  
1.5  
2  
3  

Không được dùng giá trị khác.

--------------------------------
QUY TẮC FORMAT (RẤT QUAN TRỌNG)
--------------------------------

Mỗi SubTask phải đúng CHÍNH XÁC format sau (KHÔNG THỪA, KHÔNG THIẾU):

Title: @...@ Description: ^...^ Estimate day: ++...++ Team: --...--

Trong đó:

- Title phải nằm giữa @ @
- Description phải nằm giữa ^ ^
- Estimate phải nằm giữa ++ ++
- Team phải nằm giữa -- --

--------------------------------
RÀNG BUỘC PARSING (BẮT BUỘC)
--------------------------------

1. Không được xuống dòng giữa các field trong 1 task.

2. Mỗi task phải nằm trên **1 dòng duy nhất**.

3. Không được thêm ký tự ngoài format.

4. Không được thêm dấu ":" ngoài các vị trí đã định.

5. Không được thêm text giải thích.

6. Không được thêm numbering (1., 2., - ...).

7. Không được để trống bất kỳ field nào.

8. Title không được chứa thông tin về team, chỉ mô tả hành động chính của task không nên thừa ký tự hay dấu ngoặc nào.

--------------------------------
OUTPUT
--------------------------------

Chỉ trả về danh sách SubTask theo format.

KHÔNG thêm bất kỳ nội dung nào khác.
""".strip()


def promt_create_content_subtask_foundation(
    user_story: str,
    language: str = "vi"  # "vi" hoặc "en"
) -> str:
    lang_text = "Tiếng Việt" if language == "vi" else "English"

    return f"""
Bạn là một Technical Project Manager trong dự án phát triển phần mềm Agile.

Nhiệm vụ:
Dựa trên User Story được cung cấp, hãy tạo các SubTask kỹ thuật chi tiết.

--------------------------------
INPUT
--------------------------------

User Story:
{user_story}

--------------------------------
QUY TẮC NGÔN NGỮ (BẮT BUỘC)
--------------------------------

1. Nội dung output là {lang_text}.

2. KHÔNG được trộn lẫn nhiều ngôn ngữ.

3. Nếu vi phạm, phải tự động sửa lại trước khi trả kết quả.

4. Các thuật ngữ kỹ thuật phổ biến như API, UI, UX, Mobile, Web, Endpoint, Backend, QC,... được phép giữ nguyên.

--------------------------------
QUY TẮC CHUNG
--------------------------------

1. Phải tạo từ **15 đến 20 SubTask**.

2. SubTask phải được phân bổ cho đúng 5 team:

Web
Mobile
Backend
UI/UX
QC

3. Mỗi team phải có ít nhất **2 SubTask**.

4. Không được bỏ sót bất kỳ team nào.

5. Không được tạo task chung chung, mỗi task phải rõ ràng và cụ thể.

6. Mỗi SubTask phải là một dòng độc lập.

--------------------------------
QUY TẮC TASK CHO TỪNG TEAM
--------------------------------

Web:

- Setup framework: Base Theme, Style, Color, Network, Component UI
- Dựng UI cho màn hình cụ thể trong User Story
- Code logic và tích hợp API cho màn hình

Mobile:

- Setup framework: Base Theme, Style, Color, Network, Component UI
- Dựng UI cho màn hình cụ thể trong User Story
- Code logic và tích hợp API cho màn hình

Backend:

- Thiết kế Database liên quan
- Viết đặc tả API (ghi rõ API)
- Viết logic xử lý và triển khai API

UI/UX:

- Thiết kế Design System: Theme, Color, Style, Component
- Thiết kế UI cho màn hình cụ thể

QC:

- Setup môi trường Dev / SIT / UAT
- Viết Test Case
- Thực hiện test chức năng

--------------------------------
QUY TẮC ESTIMATE
--------------------------------

Estimate phải là số hợp lệ trong danh sách:

0.5
1
1.5
2
3

Không được dùng giá trị khác.

--------------------------------
QUY TẮC FORMAT (RẤT QUAN TRỌNG)
--------------------------------

Mỗi SubTask phải đúng CHÍNH XÁC format sau (KHÔNG THỪA, KHÔNG THIẾU):

Title: @...@ Description: ^...^ Estimate day: ++...++ Team: --...--

Trong đó:

- Title phải nằm giữa @ @
- Description phải nằm giữa ^ ^
- Estimate phải nằm giữa ++ ++
- Team phải nằm giữa -- --

--------------------------------
RÀNG BUỘC PARSING (BẮT BUỘC)
--------------------------------

1. Không được xuống dòng giữa các field trong 1 task.

2. Mỗi task phải nằm trên **1 dòng duy nhất**.

3. Không được thêm ký tự ngoài format.

4. Không được thêm dấu ":" ngoài các vị trí đã định.

5. Không được thêm text giải thích.

6. Không được thêm numbering (1., 2., - ...).

7. Không được để trống bất kỳ field nào.

8. Title không được chứa thông tin về team, chỉ mô tả hành động chính của task, không được có dấu ngoặc hoặc ký tự thừa.

--------------------------------
OUTPUT
--------------------------------

Chỉ trả về danh sách SubTask theo format.

KHÔNG thêm bất kỳ nội dung nào khác.
""".strip()


promt_im_pmo_want_create_us = "Đóng vai trò là 1 PM của dự án. Tôi có 1 User Story với nội dung như sau "

