from ollama import chat
from ollama import ChatResponse

class LocalLLM:
    def __init__(self, model_name: str):
        self.model_name = model_name

    def query(self, prompt: str) -> str:
        message = [
            {
                "role": "user",
                "content": prompt
            }
        ]
        response = chat(self.model_name, message)
        return response

llm = LocalLLM("llama3.2:1b")
print(llm.query("are you able to connect with the API"))


