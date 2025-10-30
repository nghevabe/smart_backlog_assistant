import re
from pathlib import Path


def normalize_urd_text(source_str: str) -> str:
    """
    Chuẩn hoá text URD để GPT hiểu được cấu trúc rõ ràng.
    """

    text = source_str

    # 1️⃣ Làm sạch cơ bản
    text = text.replace('\r', ' ')
    text = re.sub(r'\s+', ' ', text)                 # bỏ khoảng trắng thừa
    text = re.sub(r'\n\s*\n+', '\n', text).strip()   # bỏ dòng trống
    text = re.sub(r' +', ' ', text)                  # bỏ khoảng trắng lặp

    # 2️⃣ Đảm bảo heading xuống dòng rõ ràng (ví dụ "3.2.1 " → xuống dòng mới)
    text = re.sub(r'(\d+(\.\d+)+\s+)', r'\n\1', text)
    text = re.sub(r'(^|\n)(MỤC LỤC)', r'\n\2', text, flags=re.IGNORECASE)
    text = re.sub(r'(^|\n)(PHIÊN BẢN|VERSION)', r'\n\2', text, flags=re.IGNORECASE)

    # 3️⃣ Chuẩn hoá heading → GPT hiểu phân cấp
    def heading_replacer(match):
        section = match.group(1).strip()
        title = match.group(2).strip()
        return f"\n# SECTION_{section} {title.upper()}\n"

    text = re.sub(r'\n(\d+(\.\d+)*)\s+([^\n]+)', lambda m: heading_replacer((m.group(1), m.group(3)))
                  if False else f"\n# SECTION_{m.group(1)} {m.group(3).strip()}", text)

    # 4️⃣ Giữ khoảng trắng hợp lý quanh heading
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = text.strip()

    # 5️⃣ Làm nổi bật các keyword thường gặp trong URD
    keywords = [
        "Mô tả", "Mockup", "Luồng xử lý", "Dữ liệu", "Exception",
        "Điều kiện", "Kết quả", "Quy trình", "Phạm vi", "Mục đích"
    ]
    for kw in keywords:
        text = re.sub(rf'(\b{kw}\b)', r'**\1**', text, flags=re.IGNORECASE)

    return text


# 🧪 Ví dụ sử dụng:
# Giả sử bạn đã có biến source_str (chứa nội dung text_only_output.txt)
# normalized = normalize_urd_text(source_str)

# Xuất ra file để xem hoặc feed GPT
# Path("normalized_urd.txt").write_text(normalized, encoding="utf-8")
# print(normalized[:1500])  # xem trước 1500 ký tự đầu
