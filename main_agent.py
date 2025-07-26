from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template(
    """
You are an insurance claims assistant. Based on the user's query and the retrieved policy documents, provide a structured JSON response.

Respond in this format:
{
  "decision": "Approved | Rejected",
  "amount": "If applicable, mention amount covered",
  "justification": [
    {
      "clause_excerpt": "Short quote from policy",
      "reasoning": "Why this clause applies"
    }
  ]
}

Query: {query}

Relevant policy context:
{context}
"""
)
