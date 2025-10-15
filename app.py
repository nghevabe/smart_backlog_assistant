from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

import main
from extracter import scaner
from data.data_app import lstUserStoryItem, lstUserStoryPreview, lstTaskItem, lstTaskItemPreview


app = Flask(__name__)
app.secret_key = "dev-secret-key"

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

# Trang processing: nhận form và render trang loading
@app.route("/processing", methods=["POST"])
def processing():
    epic = request.form.get("epic_name", "").strip()
    goal = request.form.get("business_goal", "").strip()
    desc = request.form.get("high_level_desc", "").strip()
    requirement = request.form.get("requirement_type", "").strip()

    # Trả về trang hiển thị loading + auto fetch /run_async
    return render_template(
        "processing.html",
        epic=epic, goal=goal, desc=desc, requirement=requirement
    )

# API thực thi xử lý thật
@app.route("/run_async", methods=["POST"])
def run_async():
    data = request.get_json(silent=True) or {}
    epic = data.get("epic_name", "")
    goal = data.get("business_goal", "")
    desc = data.get("high_level_desc", "")
    requirement = data.get("requirement_type", "")

    try:
        # Gọi xử lý chính
        result = main.main_app(epic, goal, desc, requirement)

        # Trả về JSON có cả status và nội dung
        return jsonify({
            "status": "success",
            "result": result
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "result": f"Lỗi: {e}"
        }), 500


@app.route("/run_step", methods=["POST"])
def run_step():
    data = request.get_json()
    step = data.get("step")
    epic = data.get("epic_name", "")
    goal = data.get("business_goal", "")
    desc = data.get("high_level_desc", "")
    task_type = data.get("requirement_type", "")

    try:
        if step == 1:
            main.create_lst_user_story_preview_step(epic, goal, desc)
            lst = lstUserStoryPreview
            # list of UserStoryItem → dict để gửi ra JSON
            result = [
                {"uid": x.uid, "title": x.title, "content": x.content, "criteria": x.criteria}
                for x in lst
            ]
            return jsonify({"status": "success", "result": result, "step": 1})

        elif step == 2:
            main.create_list_user_story_jira_step()
            return jsonify({"status": "success", "result": [], "step": 2})

        elif step == 3:
            main.create_lst_task_preview_step("0")
            lst = lstTaskItemPreview

            result = [
                {"uid": x.user_story_id, "title": x.title, "content": x.des, "team": x.team, "manday": x.manday}
                for x in lst
            ]
            return jsonify({"status": "success", "result": result, "step": 3})
        # ... Step 4–5 tương tự ...
        elif step == 4:
            main.create_task_jira_step()
            return jsonify({"status": "success", "result": [], "step": 4})
        # ... Step 4–5 tương tự ...
        else:
            return jsonify({"status": "error", "message": "Invalid step"}), 400

        return jsonify({"status": "success", "step": step, "result": result})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500



from flask import request, jsonify


@app.route("/update_all_items", methods=["POST"])
def update_all_items():
    """
    Cập nhật toàn bộ item trong lstUserStoryPreview theo thứ tự index.
    Fix: đảm bảo mỗi item được cập nhật riêng biệt, không ghi đè lẫn nhau.
    """

    data = request.get_json(silent=True) or {}
    items = data.get("items") or []

    try:
        n = min(len(items), len(lstUserStoryPreview))
        for i in range(n):
            upd = dict(items[i])  # tạo bản copy riêng biệt, tránh tham chiếu
            itm = lstUserStoryPreview[i]

            # Cập nhật từng field riêng rẽ, không tạo lại object
            if "title" in upd and upd["title"] is not None:
                itm.title = str(upd["title"])
            if "content" in upd and upd["content"] is not None:
                itm.content = str(upd["content"])
            if "criteria" in upd and upd["criteria"] is not None:
                itm.criteria = str(upd["criteria"])

        return jsonify({
            "status": "success",
            "updated": n,
            "mode": "index"
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route("/update_all_sub_tasks", methods=["POST"])
def update_all_sub_tasks():
    """
    Cập nhật toàn bộ item trong lstUserStoryPreview theo thứ tự index.
    Fix: đảm bảo mỗi item được cập nhật riêng biệt, không ghi đè lẫn nhau.
    """

    data = request.get_json(silent=True) or {}
    items = data.get("items") or []

    try:
        n = min(len(items), len(lstTaskItemPreview))
        for i in range(n):
            upd = dict(items[i])  # tạo bản copy riêng biệt, tránh tham chiếu
            itm = lstTaskItemPreview[i]

            # Cập nhật từng field riêng rẽ, không tạo lại object
            if "title" in upd and upd["title"] is not None:
                itm.title = str(upd["title"])
            if "content" in upd and upd["content"] is not None:
                itm.des = str(upd["content"])

        return jsonify({
            "status": "success",
            "updated": n,
            "mode": "index"
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# Trang kết quả (đơn giản)
@app.route("/result", methods=["GET"])
def result():
    status = request.args.get("status", "unknown")
    return render_template("result.html", status=status)

if __name__ == "__main__":
    # Bật threaded để xử lý tốt nhiều request liên tiếp
    app.run(debug=True, port=5000, threaded=True)
