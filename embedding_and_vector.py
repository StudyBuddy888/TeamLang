
from document_spliting import split_document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
import os

load_dotenv()

def create_vectorstore():
    """Create a vector store from the document chunks."""
    embedding = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",  # Gemini embedding model
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    chunks = split_document("BAJHLIP23020V012223.pdf")

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding,
        persist_directory="chroma_db"  # directory to store the index
    )
    
    return vectorstore

