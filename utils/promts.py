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


promt_create_content_subtask_project = """
Giờ tôi muốn tạo ra ngẫu nhiên từ 15 đến 20 SubTask con của User Story và Estimate thời gian cho chúng. Phải tạo riêng từng task để cho 5 Team như Web, Mobile, Backend, UI/UX, QC. Các Task cho mỗi Team phải có ít nhất các tiêu chí sau:
-	Web:
+ Dựng Framework cho dự án: bao gồm Base Theme, Style, Color, Network, Component UI
+ Dựng UI các màn hình (nói cụ thể màn nào)
+ Code Logic và ghép API cho các màn (nói cụ thể màn nào)

-	Mobile:
+ Dựng Framework cho dự án: bao gồm Base Theme, Style, Color, Network, Component UI
+ Dựng UI các màn hình (nói cụ thể từng màn)
+ Code Logic và ghép API cho các màn (nói cụ thể từng màn)

-	Backend:
+ Thiết kế Database
+ Viết đặc tả API (cụ thể api nào)
+ Viết logic và cung cấp api (cụ thể từng api)

-	UI/UX:
+ Thiết kế bộ Design System: Theme, Color, Style, Component
+ Thiết kế các màn hình (cụ thể từng màn hình)

-	QC:
+ Dựng môi trường Dev, Sit, UAT,… phục vụ việc phát triển
+ Viết TestCase cho các màn hình
+ Test các màn hình.

Response trả ra phải có đủ 4 thông tin và format có các ký tự đặc biệt để thuận lợi cho việc parsing như sau:
Title: @title here@ Description: ^description here^ Estimate day: ++estimate day here++ Team(Web or Mobile or Backend or UI/UX or QC): --team here--
"""

promt_create_content_subtask_foundation = """
Bạn là một Technical Architect trong dự án phát triển phần mềm Agile.

Nhiệm vụ:
Dựa trên Foundation User Story được cung cấp, hãy tạo các SubTask kỹ thuật để thiết lập nền tảng cho dự án.

--------------------------------
INPUT
--------------------------------

Foundation User Story:
{foundation_story}

Ngôn ngữ:
{language}

--------------------------------
QUY TẮC TẠO TASK
--------------------------------

1. Phải tạo từ **5 đến 10 SubTask**.

2. SubTask phải được phân bổ cho các team sau:

Web  
Mobile  
Backend  
UI/UX  
QC

3. Không bắt buộc mỗi team đều phải có task, nhưng nên phân bổ hợp lý.

4. Các SubTask phải tập trung vào việc **thiết lập nền tảng dự án**, ví dụ:

Web / Mobile
- Setup project structure
- Setup base theme
- Setup design tokens
- Setup network layer
- Setup base UI components

Backend
- Setup project architecture
- Setup database schema
- Setup API structure
- Setup authentication mechanism
- Setup logging / error handling

UI/UX
- Thiết kế Design System
- Thiết kế Component Library
- Thiết lập Color System
- Thiết lập Typography

QC
- Setup test environment
- Chuẩn bị test data
- Thiết lập test strategy

5. Không tạo task liên quan đến màn hình cụ thể.

--------------------------------
QUY TẮC ESTIMATE
--------------------------------

Estimate phải ở đơn vị **day**

Giá trị hợp lệ:

0.5  
1  
1.5  
2  
3  

--------------------------------
QUY TẮC NỘI DUNG
--------------------------------

Title:
Phải ngắn gọn và mô tả rõ công việc.

Description:
Mô tả chi tiết công việc cần thực hiện.

Response trả ra phải có đủ 4 thông tin và format có các ký tự đặc biệt để thuận lợi cho việc parsing như sau:
Title: @title here@ Description: ^description here^ Estimate day: ++estimate day here++ Team(Web or Mobile or Backend or UI/UX or QC): --team here--
"""


promt_im_pmo_want_create_us = "Đóng vai trò là 1 PM của dự án. Tôi có 1 User Story với nội dung như sau "

