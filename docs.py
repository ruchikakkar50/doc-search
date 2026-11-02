from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from vectorstore.store import QdrantStore

COLLECTION_NAME = "business-docs"
load_dotenv()
embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small")

sentences = [
    "The quick brown fox jumps over the lazy dog.",
    "I love programming in Python.",
    "Artificial intelligence is transforming the world.",
]

vectors = embeddings_model.embed_documents(sentences)

qdrant_object = QdrantStore(
    url="http://localhost:6333",
    collection_name=COLLECTION_NAME,
    vector_size=1536)

qdrant_object.create_collection()

qdrant_object.upsert_documents(
    texts=sentences,
    vectors=vectors,
)