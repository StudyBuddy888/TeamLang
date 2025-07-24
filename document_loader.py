import os
import sys
sys.path.append('../..')

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_community.document_loaders import UnstructuredEmailLoader


file_path = "BAJHLIP23020V012223.pdf"

def load_document(file_path):  
    ext = os.path.splitext(file_path)[-1].lower()

    if ext == ".pdf":
        loader = PyMuPDFLoader(file_path)
    elif ext in [".docx", ".doc"]:
        loader = UnstructuredWordDocumentLoader(file_path)
    elif ext in [".eml", ".msg"]:
        loader = UnstructuredEmailLoader(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")

    return loader.load()

if __name__ == "__main__":
    pages = load_document(file_path)
    page1 = pages[0]
    print(page1.metadata)  

