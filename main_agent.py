from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from embedding_and_vector import create_vectorstore
from retriver import get_mmr_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.runnables import RunnableLambda
from dotenv import load_dotenv
import os

load_dotenv()

# Step 1: Prompt
prompt = ChatPromptTemplate.from_template(
    """
You are an insurance claims assistant. Based on the user's query and the retrieved policy documents, provide a structured JSON response.

Respond in this format:
{{
  "decision": "Approved | Rejected",
  "amount": "If applicable, mention amount covered",
  "justification": [
    {{
      "clause_excerpt": "Short quote from policy",
      "reasoning": "Why this clause applies"
    }}
  ]
}}

Query: {question}

Relevant policy context:
{context}
"""
)

# Step 2: Vectorstore + retriever
vectordb = create_vectorstore("BAJHLIP23020V012223.pdf")
 # Optional count log

retriever = get_mmr_retriever(vectordb)

# Step 3: LLM
llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.0-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Step 4: Combine doc chain (answer generation chain)
combine_docs_chain = create_stuff_documents_chain(
    llm=llm,
    prompt=prompt
)

# Step 5: Create retriever chain manually
# This replaces deprecated `create_retrieval_chain` usage
retrieval_chain = (
    RunnableLambda(lambda x: {"context": retriever.invoke(x["question"]), "question": x["question"]})
    | combine_docs_chain
)

# Step 6: Run it
if __name__ == "__main__":
    query = "46-year-old male, knee surgery in Pune, 3-month-old insurance policy"
    response = retrieval_chain.invoke({"question": query})
    print("\n🧾 Final Structured Output:\n", response)



