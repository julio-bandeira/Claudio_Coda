import sys
from llm import call_llm
from parser import parse_response
from validator import validate_and_fix_action
from tools import execute_action
import platform

def get_os():
    os_name = platform.system()

    if os_name == "Windows":
        return "Windows"
    elif os_name == "Linux":
        return "Linux"
    elif os_name == "Darwin":
        return "MacOS"
    else:
        return "Unknown"

#from agent import run_agent

def main():
    if len(sys.argv) < 2:
        print("Uso: claudio <modelo>")
        return

    model = sys.argv[1]
    path = "."  # diretório atual

    os_info = get_os()

    messages = [
        {
            "role": "system",
            "content": """
                Você é um agente de código que trabalha em etapas.

                Ações disponíveis:
                - create_file
                - read_file
                - run_command

                Execute UMA ação por vez.

                Use o histórico da conversa para decidir.

                Quando terminar:
                {
                    "action": "none"
                }
            """
        },
        {
            "role": "system",
            "content": f"""
                O sistema operacional atual é: {os_info}.

                Use comandos compatíveis com esse sistema.
                - Windows → use 'dir', 'type', etc.
                - Linux/Mac → use 'ls', 'cat', etc.
            """
        }
    ]

    print(f"[Claudio] Modelo: {model}")
    print(f"[Claudio] Path: {path}")

    #run_agent(model, path)

    while True:
        user_input = input(">>> ")

        if user_input in ["exit", "quit"]:
            break

        messages.append({
            "role": "user",
            "content": user_input
        })

        for step in range(5):
            print(f"\n[STEP {step+1}]")

            response = call_llm(model, messages)

            content = response["content"]

            print("\n[RAW RESPONSE]")
            print(content)

            action = parse_response(content)
            action = validate_and_fix_action(action)

            print("\n[PARSED]")
            print(action)

            # 🔥 adiciona resposta do modelo corretamente
            messages.append({
                "role": "assistant",
                "content": content
            })

            result = execute_action(action, path)

            # 🔥 resultado como TOOL (CRÍTICO)
            messages.append({
                "role": "tool",
                "content": str(result)
            })

            if action.get("action") == "none":
                break

if __name__ == "__main__":
    main()