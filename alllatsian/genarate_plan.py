def generate_row_header(stt, task_item):
    return f"""
            <tr>
              <td data-label="STT">{stt}</td>
              <td data-label="Chức năng / User Story" class="content-cell"><strong>{task_item.user_story}</strong></td>
              <td data-label="Tên chức năng / Subtask">{task_item.sub_task}</td>
              <td data-label="Mô tả sơ bộ nội dung" class="small">{task_item.des}</td>
              <td data-label="Nhóm thực hiện">{task_item.team}</td>
              <td data-label="Khái toán mandays">{task_item.manday}</td>
            </tr>
    """


def generate_row_normal(stt, task_item):
    return f"""
            <tr>
              <td data-label="STT">{stt}</td>
              <td data-label="Chức năng / User Story" class="content-cell"></td>
              <td data-label="Tên chức năng / Subtask">{task_item.sub_task}</td>
              <td data-label="Mô tả sơ bộ nội dung" class="small">{task_item.des}</td>
              <td data-label="Nhóm thực hiện">{task_item.team}</td>
              <td data-label="Khái toán mandays">{task_item.manday}</td>
            </tr>
    """


def source_html_plan_doc(body_table_plan):
    promt_estimate_html_source = f""" 
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
            {body_table_plan}
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

    return promt_estimate_html_source