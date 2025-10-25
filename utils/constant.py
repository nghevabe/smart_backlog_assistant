import os

model_config = "gpt-4o-mini"
user_config = "user"
# jira_api_token = 'jira_api_token'
# open_api_key = 'open_api_key'

open_api_key = os.environ.get('OPENAI_API_KEY')
jira_api_token = os.environ.get('ATLASSIAN_API_TOKEN')

alllatsian_id_namespace = 'https://bidv-vn.atlassian.net'
confluence_namespace = 'KH0012024'
jira_project_space = 'KH01420231'
alllatsian_username = 'linhth8@bidv.com.vn'


html_source = """
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <title>Kế hoạch & Khái toán - Quản lý lớp học</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }
    h2 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 5px; }
    h3 { color: #34495e; margin-top: 30px; }
    table { border-collapse: collapse; width: 100%; margin-top: 15px; }
    th, td { border: 1px solid #ccc; padding: 10px; text-align: left; }
    th { background-color: #ecf0f1; }
    .acceptance { background: #f9f9f9; padding: 10px; border-left: 4px solid #3498db; }
    .summary { margin-top: 20px; padding: 10px; background: #f4f6f6; border: 1px solid #ccc; }
  </style>
</head>
<body>

  <h1>Kế hoạch & Khái toán - Quản lý lớp học</h1>

  <!-- User Story 1 -->
  <h2>User Story 1: Xem danh sách lớp học</h2>
  <div class="acceptance">
    <strong>Acceptance Criteria:</strong>
    <ul>
      <li>Người dùng có thể thấy danh sách lớp học hiển thị trên màn hình chính.</li>
      <li>Mỗi lớp hiển thị tên lớp, giáo viên phụ trách, và thời gian học.</li>
      <li>Danh sách có thể cuộn và có chức năng tìm kiếm bằng tên lớp.</li>
    </ul>
  </div>

  <table>
    <tr><th>Team</th><th>Title</th><th>Description</th><th>Estimate</th></tr>
    <tr><td>Web</td><td>Hiển thị danh sách lớp học</td><td>Phát triển giao diện web hiển thị danh sách lớp học với đầy đủ thông tin và cuộn.</td><td>3 ngày</td></tr>
    <tr><td>Mobile</td><td>Danh sách lớp học trên mobile</td><td>Thiết kế & phát triển giao diện mobile với chức năng cuộn & tìm kiếm.</td><td>3 ngày</td></tr>
    <tr><td>Backend</td><td>API lấy danh sách lớp học</td><td>Xây dựng API trả về danh sách lớp học từ CSDL.</td><td>2 ngày</td></tr>
    <tr><td>UI/UX</td><td>Thiết kế UI danh sách lớp học</td><td>Thiết kế UI/UX trực quan, dễ sử dụng.</td><td>2 ngày</td></tr>
    <tr><td>QC</td><td>Kiểm thử danh sách lớp học</td><td>Kiểm tra hiển thị, cuộn và tìm kiếm.</td><td>2 ngày</td></tr>
  </table>

  <!-- User Story 2 -->
  <h2>User Story 2: Thêm lớp học mới</h2>
  <div class="acceptance">
    <strong>Acceptance Criteria:</strong>
    <ul>
      <li>Khi nhấn "Thêm lớp học", chuyển đến trang nhập thông tin.</li>
      <li>Người dùng nhập tên lớp, giáo viên, thời gian, mô tả.</li>
      <li>Sau khi lưu, lớp học mới hiển thị trong danh sách.</li>
    </ul>
  </div>

  <table>
    <tr><th>Team</th><th>Title</th><th>Description</th><th>Estimate</th></tr>
    <tr><td>Web</td><td>Thiết kế trang thêm lớp học</td><td>Thiết kế UI nhập thông tin lớp học.</td><td>2 ngày</td></tr>
    <tr><td>Web</td><td>Triển khai thêm lớp học</td><td>Xây dựng chức năng nhập & lưu lớp học trên web.</td><td>3 ngày</td></tr>
    <tr><td>Mobile</td><td>Thiết kế trang thêm lớp học mobile</td><td>Thiết kế UI nhập thông tin trên app mobile.</td><td>2 ngày</td></tr>
    <tr><td>Mobile</td><td>Triển khai thêm lớp học mobile</td><td>Xây dựng chức năng nhập & lưu trên app mobile.</td><td>3 ngày</td></tr>
    <tr><td>Backend</td><td>API thêm lớp học</td><td>Xây dựng API nhận & lưu thông tin lớp học.</td><td>2 ngày</td></tr>
    <tr><td>Backend</td><td>Kết nối CSDL</td><td>Lưu thông tin lớp học mới vào CSDL.</td><td>2 ngày</td></tr>
    <tr><td>UI/UX</td><td>Nghiên cứu UI/UX thêm lớp</td><td>Đề xuất UI/UX tối ưu nhập dữ liệu.</td><td>1 ngày</td></tr>
    <tr><td>QC</td><td>Kiểm thử thêm lớp học web</td><td>Test tính năng thêm lớp trên web.</td><td>2 ngày</td></tr>
    <tr><td>QC</td><td>Kiểm thử thêm lớp học mobile</td><td>Test tính năng thêm lớp trên mobile.</td><td>2 ngày</td></tr>
  </table>

  <!-- User Story 3 -->
  <h2>User Story 3: Chỉnh sửa thông tin lớp học</h2>
  <div class="acceptance">
    <strong>Acceptance Criteria:</strong>
    <ul>
      <li>Người dùng có thể chọn lớp học và nhấn "Chỉnh sửa".</li>
      <li>Trang chỉnh sửa hiển thị thông tin hiện tại.</li>
      <li>Sau khi lưu, danh sách cập nhật thông tin mới.</li>
    </ul>
  </div>

  <table>
    <tr><th>Team</th><th>Title</th><th>Description</th><th>Estimate</th></tr>
    <tr><td>Web</td><td>Nút chỉnh sửa</td><td>Thêm nút "Chỉnh sửa" vào danh sách lớp học.</td><td>2 ngày</td></tr>
    <tr><td>Web</td><td>Trang chỉnh sửa</td><td>Phát triển trang chỉnh sửa thông tin lớp học.</td><td>3 ngày</td></tr>
    <tr><td>Web</td><td>Cập nhật danh sách sau lưu</td><td>Hiển thị thay đổi sau khi lưu.</td><td>2 ngày</td></tr>
    <tr><td>Mobile</td><td>Nút chỉnh sửa mobile</td><td>Phát triển nút chỉnh sửa trên mobile.</td><td>2 ngày</td></tr>
    <tr><td>Mobile</td><td>Trang chỉnh sửa mobile</td><td>Phát triển giao diện chỉnh sửa trên mobile.</td><td>3 ngày</td></tr>
    <tr><td>Mobile</td><td>Cập nhật danh sách mobile</td><td>Hiển thị thay đổi sau khi lưu.</td><td>2 ngày</td></tr>
    <tr><td>Backend</td><td>API lấy thông tin lớp</td><td>API trả về thông tin chi tiết lớp học.</td><td>2 ngày</td></tr>
    <tr><td>Backend</td><td>API cập nhật lớp</td><td>Xử lý yêu cầu chỉnh sửa lớp học.</td><td>2 ngày</td></tr>
    <tr><td>UI/UX</td><td>Thiết kế nút chỉnh sửa</td><td>Thiết kế UI nút chỉnh sửa web & mobile.</td><td>1 ngày</td></tr>
    <tr><td>UI/UX</td><td>Thiết kế trang chỉnh sửa</td><td>Thiết kế UI chỉnh sửa lớp học.</td><td>2 ngày</td></tr>
    <tr><td>QC</td><td>Kiểm thử chọn & chỉnh sửa</td><td>Test chọn lớp & nút chỉnh sửa.</td><td>1 ngày</td></tr>
    <tr><td>QC</td><td>Kiểm thử trang chỉnh sửa</td><td>Test giao diện & chỉnh sửa thông tin.</td><td>2 ngày</td></tr>
    <tr><td>QC</td><td>Kiểm thử cập nhật danh sách</td><td>Đảm bảo danh sách cập nhật chính xác.</td><td>1 ngày</td></tr>
  </table>

  <!-- User Story 4 -->
  <h2>User Story 4: Xóa lớp học</h2>
  <div class="acceptance">
    <strong>Acceptance Criteria:</strong>
    <ul>
      <li>Người dùng có thể chọn lớp học và nhấn "Xóa".</li>
      <li>Hệ thống yêu cầu xác nhận trước khi xóa.</li>
      <li>Sau khi xác nhận, lớp học bị xóa và thông báo thành công hiển thị.</li>
    </ul>
  </div>

  <table>
    <tr><th>Team</th><th>Title</th><th>Description</th><th>Estimate</th></tr>
    <tr><td>Web</td><td>Nút Xóa</td><td>Thêm nút Xóa trên danh sách lớp học web.</td><td>1 ngày</td></tr>
    <tr><td>Web</td><td>Hộp thoại xác nhận</td><td>Hiển thị popup xác nhận xóa.</td><td>1 ngày</td></tr>
    <tr><td>Web</td><td>Cập nhật danh sách</td><td>Xóa lớp và cập nhật giao diện danh sách.</td><td>1 ngày</td></tr>
    <tr><td>Mobile</td><td>Nút Xóa mobile</td><td>Thêm nút Xóa trên app mobile.</td><td>1 ngày</td></tr>
    <tr><td>Mobile</td><td>Xác nhận xóa mobile</td><td>Popup xác nhận xóa trên mobile.</td><td>1 ngày</td></tr>
    <tr><td>Mobile</td><td>Cập nhật danh sách mobile</td><td>Cập nhật danh sách sau khi xóa.</td><td>1 ngày</td></tr>
    <tr><td>Backend</td><td>API xóa lớp học</td><td>Xây dựng API xóa lớp học.</td><td>2 ngày</td></tr>
    <tr><td>Backend</td><td>Xác thực quyền xóa</td><td>Đảm bảo người dùng có quyền xóa lớp học.</td><td>1 ngày</td></tr>
    <tr><td>UI/UX</td><td>Thiết kế nút Xóa</td><td>Thiết kế UI/UX cho nút Xóa.</td><td>1 ngày</td></tr>
    <tr><td>UI/UX</td><td>Thiết kế hộp thoại xác nhận</td><td>Thiết kế UI/UX cho popup xác nhận xóa.</td><td>1 ngày</td></tr>
    <tr><td>QC</td><td>Kiểm thử xóa lớp học</td><td>Test chức năng xóa trên web & mobile.</td><td>1 ngày</td></tr>
    <tr><td>QC</td><td>Kiểm thử xác nhận xóa</td><td>Test các case xác nhận xóa.</td><td>1 ngày</td></tr>
  </table>

  <div class="summary">
    <h3>Tổng hợp khái toán</h3>
    <p><strong>Tổng effort ước tính:</strong> ~ 47 ngày công (cộng tất cả các task).</p>
    <p><strong>Phân bổ effort:</strong> Web (14d), Mobile (13d), Backend (11d), UI/UX (8d), QC (8d).</p>
    <p><strong>Ghi chú:</strong> Các team có thể làm song song, nên tổng thời gian triển khai thực tế dự kiến khoảng 3–4 tuần.</p>
  </div>

</body>
</html>

"""

promt_estimate_html_source = """ 
<h1>Khái toán manday và phân khai kế hoạch chi tiết<h1>

<div class="table-wrap">
    <table>
      <thead>
        <tr>
          <th>Thông tin</th>
          <th>Giá trị</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="label-cell"> <!-- in đậm --> Mã kế hoạch <!-- in đậm --></td>
          <td> mã kế hoạch được cấp</td>
        </tr>
        <tr>
          <td class="label-cell"> <!-- in đậm -->Tên kế hoạch <!-- in đậm --></td>
          <td> tên kế hoạch được cấp</td>
        </tr>
        <tr>
          <td class="label-cell"> <!-- in đậm --> Mã phần mềm <!-- in đậm --> </td>
          <td> mã phần mềm</td>
        </tr>
        <tr>
          <td class="label-cell"> <!-- in đậm --> Tên phần mềm <!-- in đậm --> </td>
          <td> Tên phần mềm</td>
        </tr>
        <tr>
          <td class="label-cell"> <!-- in đậm --> Ngày hoàn thành URD theo kế hoạch <!-- in đậm --> </td>
          <td> Ngày hoàn thành URD theo kế hoạch phần mềm</td>
        </tr>
        <tr>
          <td class="label-cell">Ngày TTPTNHS nhận URD thực tế</td>
          <td> Ngày thực tế PM/BA TTPTNHS nhận URD đã phê duyệt từ ĐVNV và bắt đầu tính timeline 30 ngày khảo sát</td>
        </tr>
      </tbody>
    </table>
  </div>

<h2> 1. Danh sách nhân sự dự án theo chức năng tại thời điểm phân khai kế hoạch <h2>

  <div class="table-wrap">
    <table>
      <thead>
        <tr>
          <th>Role</th>
          <th>Nhân sự</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="role-cell">PM</td>
          <td> PM</td>
        </tr>
        <tr>
          <td class="role-cell">PO</td>
          <td> PO</td>
        </tr>
        <tr>
          <td class="role-cell">BA</td>
          <td> BA, BA Lead</td>
        </tr>
        <tr>
          <td class="role-cell">Dev</td>
          <td> Dev, Dev Lead</td>
        </tr>
        <tr>
          <td class="role-cell">UIUX (nếu có)</td>
          <td> UIUX, UIUX Lead</td>
        </tr>
        <tr>
          <td class="role-cell">QA (nếu có)</td>
          <td>QA</td>
        </tr>
        <tr>
          <td class="role-cell">QCs</td>
          <td> QC, QC Lead</td>
        </tr>
      </tbody>
    </table>
  </div>

<h2> 2. Phạm vi thực hiện và khái toán manday <h2>

<div class="table-wrap">
 <!-- trình bày, phân chia các User Story và Subtask 1 cách dễ nhìn -->
    <table>
      <thead>
        <tr>
          <th style="width:4%;">STT</th>
          <th style="width:20%;">Chức năng / User Story</th>
          <th style="width:20%;">Tên chức năng / Subtask</th>
          <th style="width:28%;">Mô tả sơ bộ nội dung</th>
          <th style="width:14%;">Nhóm thực hiện</th>
          <th style="width:14%;">Khái toán mandays</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td data-label="STT">1</td>
          <td data-label="Chức năng / User Story" class="content-cell"> <!-- in đậm --> Tên User Story <!-- in đậm --> </td>
          <td data-label="Tên chức năng / Subtask"> <!-- in thường --> Tên Subtask tương ứng <!-- in thường --> </td>
          <td data-label="Mô tả sơ bộ nội dung" class="small">Mô tả sơ bộ nội dung khảo sát</td>
          <td data-label="Nhóm thực hiện">Mobile / Web / Backend / QC / UI-UX</td>
          <td data-label="Khái toán mandays">X</td>
        </tr>
        <tr>
          <td data-label="STT">2</td>
          <td data-label="Chức năng / User Story"></td>
          <td data-label="Tên chức năng / Subtask"> <!-- in thường --> Tên Subtask tương ứng <!-- in thường --> </td>
          <td data-label="Mô tả sơ bộ nội dung" class="small">Mô tả sơ bộ nội dung khảo sát</td>
          <td data-label="Nhóm thực hiện">Mobile / Web / Backend / QC / UI-UX</td>
          <td data-label="Khái toán mandays">Y</td>
        </tr>
        <tr>
          <td data-label="STT">3</td>
          <td data-label="Chức năng / User Story"></td>
          <td data-label="Tên chức năng / Subtask"> <!-- in thường --> Tên Subtask tương ứng <!-- in thường --> </td>
          <td data-label="Mô tả sơ bộ nội dung" class="small">Mô tả sơ bộ nội dung khảo sát</td>
          <td data-label="Nhóm thực hiện">Mobile / Web / Backend / QC / UI-UX</td>
          <td data-label="Khái toán mandays">Y</td>
        </tr>
        <tr>
          <td data-label="STT">4</td>
          <td data-label="Chức năng / User Story"></td>
          <td data-label="Tên chức năng / Subtask"> <!-- in thường --> Tên Subtask tương ứng <!-- in thường --> </td>
          <td data-label="Mô tả sơ bộ nội dung" class="small">Mô tả sơ bộ nội dung khảo sát</td>
          <td data-label="Nhóm thực hiện">Mobile / Web / Backend / QC / UI-UX</td>
          <td data-label="Khái toán mandays">Y</td>
        </tr>
        <!-- thêm dòng mới tại đây nếu cần -->
        <tr>
          <td data-label="STT">5</td>
          <td data-label="Chức năng / User Story" class="content-cell"> <!-- in đậm --> Tên User Story <!-- in đậm --> </td>
          <td data-label="Tên chức năng / Subtask"> <!-- in thường --> Tên Subtask tương ứng <!-- in thường --> </td>
          <td data-label="Mô tả sơ bộ nội dung" class="small">Mô tả sơ bộ nội dung khảo sát</td>
          <td data-label="Nhóm thực hiện">Mobile / Web / Backend / QC / UI-UX</td>
          <td data-label="Khái toán mandays">Z</td>
        </tr>
        <tr>
          <td data-label="STT">6</td>
          <td data-label="Chức năng / User Story"></td>
          <td data-label="Tên chức năng / Subtask"> <!-- in thường --> Tên Subtask tương ứng <!-- in thường --> </td>
          <td data-label="Mô tả sơ bộ nội dung" class="small">Mô tả sơ bộ nội dung khảo sát</td>
          <td data-label="Nhóm thực hiện">Mobile / Web / Backend / QC / UI-UX</td>
          <td data-label="Khái toán mandays">W</td>
        </tr>
        <!-- thêm dòng mới tại đây nếu cần -->
      </tbody>
    </table>
  </div>

<h2> 3. Kế hoạch chi tiết" <h2>

<div class="table-wrap">
  <table aria-label="Bảng tiến độ công việc">
    <thead>
      <tr>
        <th style="width:55%;">Nội dung</th>
        <th style="width:22%;">Ngày bắt đầu</th>
        <th style="width:23%;">Ngày hoàn thành</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td data-label="Nội dung" class="content-cell">RSD</td>
        <td data-label="Ngày bắt đầu"></td>
        <td data-label="Ngày hoàn thành"></td>
      </tr>

      <tr>
        <td data-label="Nội dung" class="content-cell">Phân tích thiết kế</td>
        <td data-label="Ngày bắt đầu"> x </td>
        <td data-label="Ngày hoàn thành"> x </td>
      </tr>

      <tr>
        <td data-label="Nội dung" class="content-cell">Lập trình</td>
        <td data-label="Ngày bắt đầu"> x </td>
        <td data-label="Ngày hoàn thành"> x </td>
      </tr>

      <tr>
        <td data-label="Nội dung" class="content-cell">KTNT kỹ thuật</td>
        <td data-label="Ngày bắt đầu"> x </td>
        <td data-label="Ngày hoàn thành"> x </td>
      </tr>

      <tr>
        <td data-label="Nội dung" class="content-cell">KTNT nghiệp vụ</td>
        <td data-label="Ngày bắt đầu"> x </td>
        <td data-label="Ngày hoàn thành"> x </td>
      </tr>

      <tr>
        <td data-label="Nội dung" class="content-cell">KTNT ANBM</td>
        <td data-label="Ngày bắt đầu"> x </td>
        <td data-label="Ngày hoàn thành"> x </td>
      </tr>

      <tr>
        <td data-label="Nội dung" class="content-cell">Triển khai</td>
        <td data-label="Ngày bắt đầu"> x </td>
        <td data-label="Ngày hoàn thành"> x </td>
      </tr>
    </tbody>
  </table>
</div>

<h2> 4. Tổng hợp khái toán" <h2>

<!-- in đậm --> Tổng effort ước tính: <!-- in đậm -->  <!-- in thường --> ~ x ngày công (cộng tất cả các task). <in thường>

<!-- in đậm --> Phân bổ effort: <!-- in đậm --> <!-- in thường --> Web (x ngày công), Mobile (x ngày công), Backend (x ngày công), UI/UX (x ngày công), QC (x ngày công). <!-- in thường -->

 """


