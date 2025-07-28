from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import List
import tempfile
import requests
import os

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.runnables import RunnableLambda
from retriver import get_mmr_retriever
from embedding_and_vector import create_vectorstore
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Request & Response Schema 

class QueryRequest(BaseModel):
    documents: str  # URL to PDF/DOCX/EML
    questions: List[str]

class QueryResponse(BaseModel):
    answers: List[str]

# Prompt Template

prompt = ChatPromptTemplate.from_template(
    """
You are an insurance claims assistant. Based on the user's query and the retrieved policy documents, provide a structured JSON response.

Respond in this format:
{{
  "decision": "Approved | Rejected | Conditional",
  "amount": "If applicable, mention amount covered or limits",
  "justification": [
    {{
      "clause_excerpt": "Relevant short quote from the document",
      "reasoning": "Explain why this clause supports your decision"
    }}
  ]
}}

Query: {question}

Relevant policy context:
{context}
"""
)

# LLM Setup

llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.0-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

combine_docs_chain = create_stuff_documents_chain(llm=llm, prompt=prompt)

# API Route 

@app.post("/api/v1/hackrx/run", response_model=QueryResponse)
async def run_query(request: QueryRequest):
    try:
        # Step 1: Download the document
        doc_url = request.documents
        response = requests.get(doc_url)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to download document.")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(response.content)
            tmp_path = tmp_file.name

        # Step 2: Create vectorstore ONCE for the document
        vectordb = create_vectorstore(tmp_path)
        retriever = get_mmr_retriever(vectordb)

        # Step 3: Create retrieval chain
        retrieval_chain = (
            RunnableLambda(lambda x: {
                "context": retriever.invoke(x["question"]),
                "question": x["question"]
            }) | combine_docs_chain
        )

        # Step 4: Loop through all questions
        all_answers = []
        for question in request.questions:
            result = retrieval_chain.invoke({"question": question})
            if isinstance(result, dict) and "answer" in result:
                all_answers.append(result["answer"])
            else:
                all_answers.append("No clear answer found.")

        return QueryResponse(answers=all_answers)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
