from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from pypdf import PdfReader
import os
from .embeddings import add_document, query_documents
from .llm import generate_response

router = APIRouter()

@router.get("/chat/")
async def chat(query: str):
    """Retrieve documents and generate a response using LLM."""
    retrieved_docs = query_documents(query)
    
    # Format retrieved context
    context = "\n".join([doc["text"] for doc in retrieved_docs]) if retrieved_docs else "No relevant documents found."

    # Build final prompt for LLM
    prompt = f"User Query: {query}\n\nRelevant Context:\n{context}\n\nAssistant:"
    
    response = generate_response(prompt)
    
    return {"response": response}

