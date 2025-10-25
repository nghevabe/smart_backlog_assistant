from bs4 import BeautifulSoup
from urllib.parse import unquote
import re
import unicodedata

# -----------------------------------
# 2️⃣  Hàm tách TOC từ HTML render
# -----------------------------------
TOC_SELECTORS = [
    'div.conf-macro.output-block[data-macro-name="toc"]',
    'div.macro-core.toc-macro.conf-macro.output-block[data-macro-name="toc"]',
    'div[data-macro-name="toc"]',
    'div.toc-macro',
    'div[title="Macro (toc)"]',
    'div[data-vc="toc"]',
]


def _clean_href(href: str) -> str:
    if not href:
        return ""

    href = unquote(href)
    href = href.strip()

    # 🔹 1. Bỏ phần prefix Confluence pageId / slug dài đầu
    # Ví dụ: "#URDCNR&VA7.FO_Báocáolịchsửcậpnhậtkhoảnphảithu-3.2.XemChitiết"
    # Giữ lại phần sau dấu "-" mà có số hoặc chữ cái viết hoa đầu
    m = re.search(r"#(?:[^#\-]*-)*(?P<anchor>(\d+(\.\d+)*[^\s]*)|([A-Za-zÀ-ỹ].*))$", href)
    if m:
        href = "#" + m.group("anchor")

    # 🔹 2. Bỏ ký tự đặc biệt, hardBreak
    href = href.replace("[hardBreak]", "").replace("%5BhardBreak%5D", "")
    href = re.sub(r"[\s]+", "-", href)

    # 🔹 3. Chuẩn hoá Unicode (tránh kí tự lạ)
    href = unicodedata.normalize("NFC", href)

    # 🔹 4. Giữ ngắn gọn (chỉ khoảng 100 ký tự)
    if len(href) > 100:
        href = href[:100]

    return href


def _normalize_title(title: str, outline: str | None) -> str:
    t = title.strip()
    if outline:
        t = re.sub(r"^\s*" + re.escape(outline) + r"[\.\s\-:]*", "", t).strip()

    t = re.sub(r"^\s*\d+(\.\d+)*[\.\s\-:]*\s*", "", t).strip()
    t = re.sub(r"\s{2,}", " ", t)

    # 🔹 chuẩn hóa Unicode + bỏ ký tự điều khiển
    t = unicodedata.normalize("NFC", t)
    t = re.sub(r"[\x00-\x1F]+", "", t)

    return t


def _find_toc_root(soup: BeautifulSoup):
    for sel in TOC_SELECTORS:
        node = soup.select_one(sel)
        if node:
            return node
    # fallback: tìm <ul> có a.toc-link
    for ul in soup.find_all("ul"):
        if ul.select_one("a.toc-link"):
            return ul.parent if ul.parent else ul
    return None


def extract_confluence_toc_string_from_html(
        html_view: str,
        min_level: int | None = None,
        max_level: int | None = None,
        include_href: bool = False,
        include_outline_prefix: bool = True
) -> str:
    """Trả về TOC dạng chuỗi bullet từ HTML body.view"""
    soup = BeautifulSoup(html_view, "html.parser")
    toc_root = _find_toc_root(soup)
    if not toc_root:
        print("️ Không tìm thấy macro TOC trong trang này.")
        return ""

    ul_root = toc_root.find("ul")
    if not ul_root:
        print(" TOC macro chưa render thành <ul>/<li> (có thể lỗi quyền xem).")
        return ""

    lines = []

    def walk(ul_tag, fallback_level=1):
        for li in ul_tag.find_all("li", recursive=False):
            body = li.select_one(".toc-item-body")
            a = li.select_one("a.toc-link") or li.find("a")
            outline = body.get("data-outline") if body else None

            if a:
                level = outline.count(".") + 1 if outline else fallback_level

                # Bỏ qua nếu ngoài khoảng level
                if (min_level and level < min_level) or (max_level and level > max_level):
                    return  # hoặc continue nếu bạn trong vòng for

                # Chuẩn hoá tiêu đề
                title = _normalize_title(a.get_text(strip=True), outline)

                # Làm sạch href (chỉ khi bạn muốn giữ lại)
                href = _clean_href(a.get("href", "")) if include_href else ""

                # Sinh prefix và indent
                prefix = f"{outline}. " if (include_outline_prefix and outline) else ""
                indent = "  " * (level - 1)

                # ⚙️ Xuất dòng TOC — chỉ thêm href nếu được bật
                if include_href and href:
                    lines.append(f"{indent}- {prefix}{title} ({href})")
                else:
                    lines.append(f"{indent}- {prefix}{title}")

            child_ul = li.find("ul", recursive=False)
            if child_ul:
                next_level = outline.count(".") + 1 if outline else (fallback_level + 1)
                walk(child_ul, next_level)

    walk(ul_root, 1)
    return "\n".join(lines)
