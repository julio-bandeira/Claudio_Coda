import ollama

class OllamaController:
    def __init__(self, model:str):
        self.model = model
        self.messages = []
    
    def generate_message(self):
        llm_output = ollama.chat(
            model= self.model,
            messages = self.messages,
            stream = True
        )

        return llm_output
    
    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})
    
    def list_models(self):
        lista: ollama.ListResponse = ollama.list()
        return lista.models

    def set_model(self, model):
        self.model = model