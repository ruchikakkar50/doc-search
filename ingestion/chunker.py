from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

class DocumentChunkerService:
    def __init__(self, 
                 chunk_size: int = 1000,
                 chunk_overlap: int = 200
                 ):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )

    def split_documents(self, documents: list[Document]) -> list[Document]:
        """
        Split a list of Document objects into smaller chunks.
        """
        chunked_documents = []
        for document in documents:
            chunks = self.splitter.split_text(document.page_content)
            for i, chunk in enumerate(chunks):
                chunked_documents.append(Document(
                    page_content=chunk,
                    metadata={**document.metadata, "chunk": i}
                ))
        return chunked_documents