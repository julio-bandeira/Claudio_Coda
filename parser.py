import json

def parse_response(response):
    try:
        return json.loads(response)
    except Exception as e:
        print("[ERRO] Falha ao converter JSON:", e)
        print(response)
        return None