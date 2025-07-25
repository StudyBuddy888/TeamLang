from embedding_and_vector import create_vectorstore
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain_google_genai import ChatGoogleGenerativeAI
import os

vectorstore = create_vectorstore()

retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 10, "fetch_k": 25, "lambda_mult": 0.7}
)

llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.getenv("GOOGLE_API_KEY"))
compressor = LLMChainExtractor.from_llm(llm)

compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=retriever
)

query = "Knee surgery claim for 46M in Pune, 3-month policy"
docs = compression_retriever.invoke(query)

if not docs:
    print("No documents retrieved for the query.")
else:
    print(f"Retrieved {len(docs)} document(s).")
    for i, doc in enumerate(docs):
        print(f"\n--- Document {i+1} ---\n")
        print(doc.page_content[:500]) 