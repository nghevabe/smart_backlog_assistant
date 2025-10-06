from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

import main
from extracter import scaner

# Nếu main_app nằm trong module khác, import vào đây. Ví dụ:
# from your_module import main_app

app = Flask(__name__)
app.secret_key = "dev-secret-key"  # đổi khi deploy

# --- STUB: Thay bằng hàm main_app thật của bạn ---


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", result=None)


@app.route("/get_fill_data", methods=["GET"])
def get_fill_data():
    url = request.args.get("doc")
    epic_name, business_goal, des = scaner.scan_page_content(url)
    return jsonify({
        "epic_name": epic_name,
        "business_goal": business_goal,
        "high_level_desc": des
    })


@app.route("/run", methods=["POST"])
def run():
    epic = request.form.get("epic_name", "").strip()
    goal = request.form.get("business_goal", "").strip()
    desc = request.form.get("high_level_desc", "").strip()
    requirement = request.form.get("requirement_type", "").strip()


    if not epic:
        flash("Epic Name is required", "error")
        return redirect(url_for("index"))

    try:
        # Gọi hàm main_app (thực tế)
        result = main.main_app(epic, goal, desc, requirement)
    except Exception as e:
        # Bắt lỗi để debug; production cần logging chi tiết
        flash(f"Lỗi khi chạy main_app: {e}", "error")
        result = None

    return render_template("index.html", result=result, epic=epic, goal=goal, desc=desc)

if __name__ == "__main__":
    app.run(debug=True, port=5000)

    # http://127.0.0.1:5000/
