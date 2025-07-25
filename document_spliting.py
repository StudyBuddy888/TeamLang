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

if __name__ == "__main__":
    file_path = "BAJHLIP23020V012223.pdf"
    texts = split_document(file_path)
    
    for i, text in enumerate(texts):
        print(f"Chunk {i+1}:")
        print(text.page_content[:200])  # Print first 200 characters of each chunk
        print("Metadata:", text.metadata)
        print("-" * 40)  # Separator for readability


