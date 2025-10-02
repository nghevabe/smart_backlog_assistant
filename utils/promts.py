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


promt_im_pmo_want_create_us = "Đóng vai trò là 1 PM của dự án. Tôi có 1 User Story với nội dung như sau "

