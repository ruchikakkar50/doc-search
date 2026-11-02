from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path


class PDFLoader:
    def __init__(self):
        pass
    def load_pdf(self, file_path: str) -> list[str]:
        """
        Load a PDF file and return its text content as a list of strings.
        """
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        return documents

    def load_pdfs(self, directory_path: str) -> list[str]:
        """
        Load all PDF files in a directory and return their text content as a list of strings.
        """
        documents =[]
        pdf_files = Path(directory_path).glob("*.pdf")
        for pdf_file in pdf_files:
            loader = PyPDFLoader(str(pdf_file))
            documents.extend(loader.load())
        
    

