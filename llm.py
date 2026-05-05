import ollama

def call_llm(model, messages):
    response = ollama.chat(
        model=model,
        messages=messages,
        format="json"
    )

    return response["message"]