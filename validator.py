FORBIDDEN = ["rm -rf", "del /f", "shutdown"]

def is_safe_command(cmd):
    return not any(bad in cmd.lower() for bad in FORBIDDEN)

def validate_and_fix_action(action):
    if not action:
        raise Exception("Ação vazia")

    act = action.get("action")

    if not act:
        raise Exception("Ação sem tipo")

    # 🔥 normalização de campos
    if "path" not in action:
        if "name" in action:
            action["path"] = action["name"]
        elif "filename" in action:
            action["path"] = action["filename"]
        elif "file_path" in action:
            action["path"] = action["file_path"]

    # 🎯 validações por tipo
    if act == "create_file":
        if not action.get("path"):
            raise Exception("create_file sem path")

        if "content" not in action:
            action["content"] = ""

    elif act == "read_file":
        if not action.get("path"):
            raise Exception("read_file sem path")

    elif act == "run_command":
        cmd = action.get("command")

        if not cmd:
            raise Exception("run_command sem command")

        if not is_safe_command(cmd):
            raise Exception("Comando perigoso bloqueado")

    elif act == "none":
        return action

    else:
        raise Exception(f"Ação desconhecida: {act}")

    return action