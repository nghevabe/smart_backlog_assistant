from bs4 import BeautifulSoup
import html
import re

from utils import constant
from utils.config import confluence_config


def get_page_id(url):
    id_regex = r'/pages/(.*)/'
    match_id = re.findall(id_regex, url)
    print(match_id)
    return int(match_id[0])


def get_title_cmmi(source):
    return "This is Title"


def get_des_cmmi(source: str) -> str | None:

    return """Cung cấp chức năng tạo và quản lý mã thỏa thuận tỷ giá phục vụ các phân hệ giao dịch có liên quan trên iBank/FX.

FX Hub được tham chiếu để kiểm tra biên độ/tỷ giá niêm yết và các cảnh báo khi đẩy duyệt mã thỏa thuận."""


def get_expect_cmmi(source):
    return "Kết Quả Mong Muốn không được đề cập"


def handle_cmmi(source):
    # 2. Parse bằng BeautifulSoup
    soup = BeautifulSoup(source, "html.parser")

    # 3. Lấy toàn bộ text (tự loại thẻ)
    text_only = soup.get_text(separator="\n", strip=True)

    return get_title_cmmi(text_only), get_des_cmmi(text_only), get_expect_cmmi(text_only), text_only


def content_extraction(id_page):

    contents = confluence_config().get_page_by_id(
        id_page,
        expand="body.storage,version",
        status="current"
    )

    page_content = contents['body']
    html_content = page_content['storage']['value']
    name, des, result, constant.content_document_input = handle_cmmi(html_content)
    return name, result, des


def scan_page_content(url):
    print("url: ")
    print(url)
    return content_extraction(get_page_id(url))
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