from bs4 import BeautifulSoup
import html
import re
from alllatsian.confluence.confluence_service_handle import confluence


def get_page_id(url):
    id_regex = r'/pages/(.*)/'
    match_id = re.findall(id_regex, url)
    print(match_id)
    return int(match_id[0])


def content_extraction(id_page):
    contents = confluence.get_page_by_id(
        id_page,
        expand="body.storage,version",
        status="current"
    )

    page_content = contents['body']
    html_content = page_content['storage']['value']

    decoded_content = html.unescape(html_content)
    table = decoded_content.split("<tbody>")
    for item in table:
        if "Quy tắc nghiệp vụ (nếu có)" in item:
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
