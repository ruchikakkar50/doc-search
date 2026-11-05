import ollama
from langchain_ollama import OllamaEmbeddings

class EmbeddingService:
    def __init__(self, model: str = "nomic-embed-text"):
        self.model = model
        self.embeddings=OllamaEmbeddings(model="nomic-embed-text")

    def get_embeddings(self):
        return self.embeddings

    def get_vector_size(self) -> str:
        response = ollama.show(self.model)
        model_info = response.modelinfo
        for key, value in model_info.items():
            if key.endswith(".embedding_length"):
                return value

        raise ValueError(
            f"Could not find embedding length for model: {self.model}"
        )