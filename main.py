from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import List
import requests
import tempfile
import os
import time
from document_spliting import split_document
from embedding_and_vector import create_vectorstore
from retriver import get_mmr_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnableLambda
from dotenv import load_dotenv

load_dotenv()

# ------------------- FastAPI Setup -------------------
app = FastAPI()

# ------------------- Request Schema -------------------
class QueryRequest(BaseModel):
    documents: str  # URL
    questions: List[str]

# ------------------- Prompt Template -------------------
prompt = ChatPromptTemplate.from_template(
    """
You are an expert insurance policy assistant specializing in Indian health insurance plans. Your job is to accurately answer user questions strictly using the information provided in the policy content.

- Always be precise and formal.
- Do not make assumptions beyond the retrieved context.
- If the policy does not explicitly contain the answer, respond with: "The policy document does not specify this information."
- Include specific clause wording or context from the policy where applicable.

QUESTION:
{question}

POLICY EXCERPTS (CONTEXT):
{context}

FINAL ANSWER:
"""
)


# ------------------- LLM Setup -------------------
llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.0-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# ------------------- Main Inference Logic -------------------
def download_file_from_url(url: str) -> str:
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to download document from URL")
    
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    with open(temp_file.name, "wb") as f:
        f.write(response.content)
    return temp_file.name

@app.post("/api/v1/hackrx/run")
async def process_query(payload: QueryRequest):
    # 1. Download & preprocess
    pdf_path = download_file_from_url(payload.documents)
    vectorstore = create_vectorstore(pdf_path)
    retriever = get_mmr_retriever(vectorstore)
    
    # 2. Setup RAG Chain
    combine_docs_chain = create_stuff_documents_chain(llm=llm, prompt=prompt)
    retrieval_chain = (
        RunnableLambda(lambda x: {"context": retriever.invoke(x["question"]), "question": x["question"]})
        | combine_docs_chain
    )

    # 3. Process all questions
    answers = []
    for question in payload.questions:
        try:
            result = retrieval_chain.invoke({"question": question})
            answers.append(result.strip())
        except Exception as e:
            print(f"Error for question: {question} -> {e}")
            answers.append("Unable to process this question.")
        time.sleep(5)
