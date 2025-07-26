from document_loader import load_document
from document_spliting import split_document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import DocArrayInMemorySearch
from dotenv import load_dotenv
import os
import warnings

warnings.filterwarnings("ignore", message=".*ValidationError.*has been moved.*")
load_dotenv()

def create_vectorstore(pdf_path: str) -> DocArrayInMemorySearch:
    """
    Loads a PDF, splits it into chunks, embeds them using Gemini,
    and stores them in an in-memory vector store.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        DocArrayInMemorySearch: The populated vector store.
    """
    # Step 1: Split document into chunks
    chunks = split_document(pdf_path)

    # Step 2: Create embedding model
    embedding = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    # Step 3: Create vector store
    db = DocArrayInMemorySearch.from_documents(chunks, embedding=embedding)

    print(f"Vector store created with {db.doc_index.num_docs()} document(s).")
    return db