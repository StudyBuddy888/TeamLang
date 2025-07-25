from document_loader import load_document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_document(file_path):
    pages = load_document(file_path)
    
    if not pages:
        raise ValueError("No pages loaded from the document.")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    
    texts = text_splitter.split_documents(pages)
    return texts




