from embedding_and_vector import create_vectorstore
import os

# Step 1: Create your vector store

def get_mmr_retriever(vectorstore):
    return vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 10,
            "fetch_k": 25,
            "lambda_mult": 0.7
        }
    )




