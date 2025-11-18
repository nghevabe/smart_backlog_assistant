from atlassian import Confluence
from bs4 import BeautifulSoup
import html
import re
from alllatsian.confluence.confluence_service_handle import confluence
from extracter.handle_toc import extract_confluence_toc_string_from_html
from handle_format import normalize_urd_text
from utils import constant
from urllib.parse import unquote
from pathlib import Path


def get_page_id(url):
    id_regex = r'/pages/(.*)/'
    match_id = re.findall(id_regex, url)
    print(match_id)
    return int(match_id[0])


def get_spaces_id(url):
    id_regex = r'/spaces/(.*)/pages'
    match_id = re.findall(id_regex, url)
    print("ZZZ_spaces_id")
    print(match_id)
    return str(match_id[0])


def get_title_cmmi(source):
    pattern = re.compile(
        r"Chức\s*năng\s*trọng\s*tâm\s*:\s*(.*?)\s*(?=\bPhiên\s*bản\s*:)",
        flags=re.IGNORECASE,
    )

    match = pattern.search(source)
    if match:
        focus_function = match.group(1).strip()
        return focus_function
    else:
        print("⚠️ Không tìm thấy phần 'Chức năng trọng tâm:' trong tài liệu.")


def get_des_cmmi(source: str) -> str | None:

    return """Cung cấp chức năng tạo và quản lý mã thỏa thuận tỷ giá phục vụ các phân hệ giao dịch có liên quan trên iBank/FX.

FX Hub được tham chiếu để kiểm tra biên độ/tỷ giá niêm yết và các cảnh báo khi đẩy duyệt mã thỏa thuận."""


def get_expect_cmmi(source):
    return "Kết Quả Mong Muốn không được đề cập"


def handle_cmmi(source):
    print("ZZZ_cmmi_5")
    # with open("output1.txt", "w", encoding="utf-8") as f:
    #     f.write(source)

    # 2. Parse bằng BeautifulSoup
    soup = BeautifulSoup(source, "html.parser")

    # 3. Lấy toàn bộ text (tự loại thẻ)
    text_only = soup.get_text(separator="\n", strip=True)

    return get_title_cmmi(text_only), get_des_cmmi(text_only), get_expect_cmmi(text_only), text_only

    # # 4. Ghi ra file mới
    # Path("text_only_output_2.txt").write_text(normalize_urd_text(text_only), encoding="utf-8")
    #
    # print("✅ Đã ghi nội dung vào file output.txt")


def content_extraction(url):
    constant.confluence_namespace = get_spaces_id(url)

    conflu = Confluence(
        url=constant.alllatsian_id_namespace + '/wiki/',
        username=constant.alllatsian_username,
        password=constant.jira_api_token,
        cloud=True)

    print("XXX_constant.alllatsian_id_namespace: "+constant.alllatsian_id_namespace)
    print("XXX_constant.alllatsian_username: "+constant.alllatsian_username)

    contents = conflu.get_page_by_id(
        get_page_id(url),
        expand="body.storage,version",
        status="current"
    )

    contents_view = conflu.get_page_by_id(
        get_page_id(url),
        expand="body.export_view,version",
        status="current"
    )

    page_content = contents['body']
    html_content = page_content['storage']['value']
    if 'CMMI-5' in str(html_content):
        name, des, result, constant.content_cmmi_5 = handle_cmmi(html_content)
        return name, result, des

    print("ZZZ_Normal Format")
    html_view = contents_view["body"]["export_view"]["value"]

    toc_value = extract_confluence_toc_string_from_html(
        html_view,
        min_level=1,
        max_level=4,
        include_outline_prefix=True
    )
    print(toc_value)
    constant.appendix_content = toc_value
    decoded_content = html.unescape(html_content)
    table = decoded_content.split("<tbody>")
    for item in table:
        if "Quy tắc nghiệp vụ" in item:
            soup = BeautifulSoup(item, "html.parser")
            # Tìm tất cả tag có tên bắt đầu bằng "ac:"
            for tag in soup.find_all(lambda t: t.name and t.name.startswith("ac:")):
                tag.unwrap()  # Bỏ tag, giữ lại nội dung bên trong

            clean_html = str(soup)
            map_items_in_row = parse_confluence_table(clean_html)

            name = map_items_in_row[0][1]
            des = map_items_in_row[1][1]
            result = map_items_in_row[5][1]
            print("match_name: " + name)
            print("match_des: " + des)
            print("match_result: " + result)
            return name, des, result


def scan_page_content(url):
    print("ZZZ_print(constant.jira_project_space): " + str(constant.jira_project_space))
    print("url: ")
    print(url)
    return content_extraction(url)
    # return content_extraction(get_page_id("https://bidv-ba-assistant317.atlassian.net/wiki/spaces/BAAI/pages/8028225/URD+CNR+VA+5.+BO_B+o+c+o+b+ng+k+kho+n+ph+i+thu"))


def parse_confluence_table(html_str: str):
    soup = BeautifulSoup(html_str, "html.parser")
    rows_data = []

    # Lặp qua từng hàng <tr>
    for tr in soup.find_all("tr"):
        cols = tr.find_all("td")
        if not cols:
            continue  # bỏ qua nếu không có cột
        # Lấy text từng cột, loại bỏ xuống dòng và khoảng trắng thừa
        col_texts = [col.get_text(separator=" ", strip=True) for col in cols]
        rows_data.append(col_texts)

    return rows_data
