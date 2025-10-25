# gunicorn.conf.py
# --------------------------------------------
# Cấu hình cho Gunicorn khi chạy Flask trên Render
# --------------------------------------------

# Tăng thời gian xử lý request lâu (OpenAI API)
timeout = 180           # 3 phút — bạn có thể tăng lên 300 nếu cần
