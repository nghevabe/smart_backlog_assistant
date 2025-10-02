from bs4 import BeautifulSoup
import html
import re
from alllatsian.confluence_service_handle import confluence


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
            print(item)
            name_regex = r'<strong>Tên</strong></p></td><td data-highlight-colour="#ffffff"><p>(.*)</p></td></tr><tr><td data-highlight-colour="#f4f5f7"><p><strong>Mô tả</strong>'
            des_regex = r'<p><strong>Mô tả</strong></p></td><td data-highlight-colour="#ffffff"><p>(.*)</p></td></tr><tr><td data-highlight-colour="#f4f5f7"><p><strong>Tác nhân</strong>'
            result_regex = r'<strong>Kết quả mong muốn</strong></p>(.*)<p><strong>Quy tắc nghiệp vụ'
            match_name = re.findall(name_regex, item)
            match_des = re.findall(des_regex, item)
            match_result = re.findall(result_regex, item)
            name = BeautifulSoup(match_name[0], "html.parser").get_text(separator="\n")
            des = BeautifulSoup(match_des[0], "html.parser").get_text(separator="\n")
            result = BeautifulSoup(match_result[0], "html.parser").get_text(separator="\n")
            print("match_name: " + name)
            print("match_des: " + des)
            print("match_result: " + result)
            return name, des, result


def scan_page_content(url):
    print("url: ")
    print(url)
    return content_extraction(get_page_id(url))
    # return content_extraction(get_page_id("https://bidv-ba-assistant317.atlassian.net/wiki/spaces/BAAI/pages/8028225/URD+CNR+VA+5.+BO_B+o+c+o+b+ng+k+kho+n+ph+i+thu"))


