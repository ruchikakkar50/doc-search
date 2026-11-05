from ingestion.loaders import PDFLoaderService
from ingestion.embeddings import EmbeddingService
from ingestion.chunker import DocumentChunkerService
from vectorstore.store import QdrantStore

COLLECTION_NAME = "business-docs"

def ingest_documents(folder_path: str):
    print("starting ingestion process...")

    loader = PDFLoaderService()
    documents = loader.load_pdfs(folder_path)
    if not documents:
        print(f"No PDF documents found in {folder_path}")
        return

    splitter = DocumentChunkerService(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(documents)

    embedding_service = EmbeddingService()
    vector_size = embedding_service.get_vector_size()

    #fetch vector size from embedding model 
    qdrant_store = QdrantStore(collection_name=COLLECTION_NAME, vector_size=vector_size)
    qdrant_store.create_collection()

ingest_documents("./documents")