import os
import subprocess

def create_file(base_path, relative_path, content):
    full_path = os.path.join(base_path, relative_path)

    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[OK] Arquivo criado: {full_path}")

def execute_action(action, base_path):
    if not action:
        return

    act = action.get("action")

    if act == "create_file":
        create_file(
            base_path,
            action.get("path", "file.txt"),
            action.get("content", "")
        )

    elif act == "read_file":
        result = read_file(
            base_path,
            action.get("path", "")
        )
        return result
    
    elif act == "run_command":
        result = run_command(
            action.get("command", ""),
            base_path
        )
        return result

    else:
        print("[INFO] Ação não implementada:", act)



def safe_path(base_path, relative_path):
    full_path = os.path.abspath(os.path.join(base_path, relative_path))
    base_path = os.path.abspath(base_path)

    if not full_path.startswith(base_path):
        raise Exception("Acesso fora do diretório permitido")

    return full_path


def read_file(base_path, relative_path):
    try:
        full_path = safe_path(base_path, relative_path)

        if not os.path.exists(full_path):
            return f"[ERRO] Arquivo não encontrado: {relative_path}"

        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()

        print(f"\n[FILE CONTENT: {relative_path}]\n")
        print(content)

        return content  # 🔥 IMPORTANTE

    except Exception as e:
        return f"[ERRO] {str(e)}"

def run_command(command, base_path):
    try:
        print(f"\n[RUNNING COMMAND]\n{command}\n")

        result = subprocess.run(
            command,
            shell=True,
            cwd=base_path,  # 🔥 executa dentro do projeto
            capture_output=True,
            text=True,
            timeout=10  # evita travar
        )

        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        if stdout:
            print("[STDOUT]")
            print(stdout)

        if stderr:
            print("\n[STDERR]")
            print(stderr)

        return {
            "stdout": stdout,
            "stderr": stderr,
            "returncode": result.returncode
        }

    except subprocess.TimeoutExpired:
        print("[ERRO] Comando excedeu tempo limite")
        return {"error": "timeout"}

    except Exception as e:
        print("[ERRO]", str(e))
        return {"error": str(e)}