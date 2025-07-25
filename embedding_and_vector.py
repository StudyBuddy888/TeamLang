from document_spliting import split_document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.docstore.document import Document
from dotenv import load_dotenv
import os
import time

load_dotenv()

# Split + clean
chunks = split_document("BAJHLIP23020V012223.pdf")
print(f"📄 Total chunks created: {len(chunks)}")

clean_chunks = [
    Document(
        page_content=doc.page_content,
        metadata={k: str(v) for k, v in doc.metadata.items() if isinstance(v, (str, int, float))}
    )
    for doc in chunks
]

# Init embedding model
embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)
print("✅ Gemini embedding model ready.")

# Extract texts
texts = [doc.page_content for doc in clean_chunks]
print("🧠 Embedding all texts...")

start = time.time()
embeddings = embedding_model.embed_documents(texts)
print(f"✅ Embedding complete in {time.time() - start:.2f}s")

# Final build and persist using from_embeddings
persist_path = os.path.expanduser("~/chroma_db")

print("💾 Saving to Chroma using from_embeddings...")
vectordb = Chroma.from_embeddings(
    embeddings=embeddings,
    documents=clean_chunks,
    embedding=embedding_model,
    persist_directory=persist_path,
    collection_name="insurance_policy_chunks"
)
vectordb.persist()
print(f"✅ All done! Vectorstore saved to {persist_path}")
