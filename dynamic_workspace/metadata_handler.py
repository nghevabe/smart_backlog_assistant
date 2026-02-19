import ast


def handle_string(field): return ""
def handle_number(field): return 0
def handle_date(field): pass
def handle_option(field): pass
def handle_multi_option(field): pass
def handle_user(field): pass
def handle_priority(field): pass
def handle_fallback(field): pass


def append_payload_subtask_function(cur_dict: dict, lst_key_field, lst_value_field):
    new_dict = cur_dict
    for index in range(len(lst_value_field)):
        new_dict[lst_key_field[index]] = lst_value_field[index]

    return new_dict


def handle_value_default(field_type: str, field_meta: dict | None = None):
    if field_type == "string":
        return handle_string(field_meta)

    if field_type == "number":
        return handle_number(field_meta)

    if field_type == "date":
        return handle_date(field_meta)

    if field_type == "option":
        return handle_option(field_meta)

    if field_type == "user":
        return handle_user(field_meta)

    if field_type == "priority":
        return handle_priority(field_meta)

    # fallback
    return handle_fallback(field_meta)


def parse_field(key: str, field_str: str) -> str | None:
    try:
        field_dict = ast.literal_eval(field_str)
        return field_dict.get(key)
    except (ValueError, SyntaxError):
        return None


def load_list_fields(projects):
    results = {}

    lstExceptions = [
        "project",
        "parent",
        "summary",
        "description",
        "issuetype",
        "reporter",
        "timetracking"
    ]

    for p in projects:
        pkey = p.get("key")
        print(f"📁 Project: {pkey}")

        for it in p.get("issuetypes", []):
            print("ZZZ_it: ")
            print(it)
            it_name = it.get("name")

            # 🔥 CHỈ LẤY SUBTASK
            if it_name != "Subtask":
                continue

            print(f"  🧩 IssueType: {it_name}")

            required_fields = []

            for fid, f in it.get("fields", {}).items():
                # chỉ lấy required
                if not f.get("required", False):
                    continue

                # loại bỏ exception
                if fid in lstExceptions:
                    print(f"   ⚪ SKIP (exception) | id={fid}")
                    continue

                field_data = {
                    "id": fid,
                    "name": f.get("name"),
                    "required": True,
                    "type": f.get("schema", {}).get("type"),
                    "custom": fid.startswith("customfield_")
                }

                print(
                    f"   Field | "
                    f"id={field_data['id']} | "
                    f"name={field_data['name']} | "
                    f"type={field_data['type']} | "
                    f"custom={field_data['custom']}"
                )

                required_fields.append(field_data)

            results[it_name] = required_fields

    print("=== [load_createmeta] END ===")

    for it_name, required_fields in results.items():
        print(f"\n🧩 IssueType: {it_name}")
        print(f"\n🧩 required_fields: {required_fields}")

        for item in required_fields:
            print(f"XXX ID: {parse_field("id", str(item))} - TYPE: {parse_field("type", str(item))}")


