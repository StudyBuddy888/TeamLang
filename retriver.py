from embedding_and_vector import create_vectorstore
import os

# Step 1: Create your vector store
vectorstore = create_vectorstore("BAJHLIP23020V012223.pdf")

retriever = vectorstore.as_retriever(
    search_type="mmr",   # better than 'similarity'
    search_kwargs={
        "k": 10,          # return top 10 relevant
        "fetch_k": 25,    # fetch 25 candidates to re-rank
        "lambda_mult": 0.7  # balance relevance vs diversity
    }
)

query = "Is knee surgery covered in a 3-month-old policy?"
docs = retriever.invoke(query)

for i, doc in enumerate(docs):
    print(f"\n--- Chunk {i+1} ---")
    print(f"Source: {doc.metadata.get('source', 'unknown')}")
    print(doc.page_content[:400])


