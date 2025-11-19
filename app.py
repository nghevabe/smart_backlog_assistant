import requests
from flask import Flask, render_template, redirect, url_for, session

from alllatsian.confluence.confluence_service_handle import create_table_est_for_doc_step
from alllatsian.jira.jira_task_controller import create_lst_task_preview_step
from alllatsian.jira.jira_task_preview_handle import create_lst_user_story_preview_step
from alllatsian.jira.jira_task_service_handle import create_list_user_story_jira_step, create_task_jira_step
from extracter import scaner
from data.data_app import lstUserStoryPreview, lstTaskItemPreview


app = Flask(__name__)
app.secret_key = "dev-secret-key"


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/config_jira")


@app.route("/config_jira")
def config_jira():
    return render_template("login_workspace.html")


@app.route("/", methods=["GET"])
def index():
    # Nếu chưa login Jira → yêu cầu nhập namespace/email/token
    if "atlassian_namespace" not in session or "atlassian_user" not in session or "atlassian_api_token" not in session:
        return redirect(url_for("config_jira"))

    # Nếu đã có session → vào trang chính
    return render_template("index.html", result=None)


@app.route("/check_namespace")
def check_namespace():
    ns = request.args.get("ns", "").strip()

    if not ns.startswith("http"):
        ns = "https://" + ns

    if not ns.endswith(".atlassian.net"):
        return {"ok": False, "message": "Domain phải có dạng *.atlassian.net"}

    try:
        r = requests.get(ns + "/rest/api/2/serverInfo", timeout=5)
        if r.status_code == 200:
            return {"ok": True}
        else:
            return {"ok": False, "message": "HTTP " + str(r.status_code)}

    except Exception as e:
        return {"ok": False, "message": str(e)}


@app.route("/save_jira_config", methods=["POST"])
def save_jira_config():
    data = request.json

    session["atlassian_namespace"] = data["namespace"]
    session["atlassian_user"] = data["email"]
    session["atlassian_api_token"] = data["token"]

    return {"ok": True, "message": "Đã lưu cấu hình Jira!"}


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
            create_lst_user_story_preview_step(epic, goal, desc)
            lst = lstUserStoryPreview
            # list of UserStoryItem → dict để gửi ra JSON
            result = [
                {"uid": x.uid, "title": x.title, "content": x.content, "criteria": x.criteria}
                for x in lst
            ]
            return jsonify({"status": "success", "result": result, "step": 1})

        elif step == 2:
            create_list_user_story_jira_step()
            return jsonify({"status": "success", "result": [], "step": 2})

        elif step == 3:
            create_lst_task_preview_step("0")
            lst = lstTaskItemPreview

            result = [
                {"uid": x.user_story_id, "title": x.title, "content": x.des, "team": x.team, "manday": x.manday}
                for x in lst
            ]
            return jsonify({"status": "success", "result": result, "step": 3})
        # ... Step 4–5 tương tự ...
        elif step == 4:
            create_task_jira_step()
            return jsonify({"status": "success", "result": [], "step": 4})
        # ... Step 5 tương tự ...
        elif step == 5:
            create_table_est_for_doc_step()
            return jsonify({"status": "success", "result": [], "step": 5})
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
