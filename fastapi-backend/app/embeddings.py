from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import uuid
from .db import get_chroma_collection
# from .routes import get_current_user

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      
    chunk_overlap=200,   
    separators=["\n\n", "\n", " ", ""],  
)

retriever = Chroma(
    persist_directory="./data/chroma",
    embedding_function=embedding_model
).as_retriever(search_kwargs={"k":1, "filter": {"user_id": "ahmed"}})

# def query_documents(query: str, user_id: str, top_k: int = 3):
#     """Retrieve relevant document chunks for a given user."""
#     docs = retriever.invoke(query, search_kwargs={"k": top_k, "filter": {"user_id": user_id}})
#     return [{"text": doc.page_content} for doc in docs] if docs else []

def add_document(user_id: str, file_name: str, text: str):
    """Split and store document chunks in ChromaDB with metadata, including user_id."""
    collection = get_chroma_collection()
    doc_id = str(uuid.uuid4())
    
    # Create a unique name to avoid collisions between users
    unique_name = f"{user_id}_{file_name}"
    
    # Split text into smaller chunks
    chunks = text_splitter.split_text(text)
    
    collection.add(
        ids=[f"{unique_name}-{i}" for i in range(len(chunks))],
        documents=chunks,
        metadatas=[{"user_id": user_id, "file_name": file_name, "doc_id": doc_id, "chunk": i} for i in range(len(chunks))]
    )
    return doc_id

def delete_document(user_id: str, file_name: str):
    """Delete all document chunks related to the given file name and user."""
    collection = get_chroma_collection()
    
    # Combine filters using the "$and" operator
    results = collection.get(where={"$and": [{"user_id": user_id}, {"file_name": file_name}]})
    
    if not results["ids"]:
        return {"message": "No chunks found for this document"}

    collection.delete(ids=results["ids"])
    return {"message": f"Document '{file_name}' and its chunks have been deleted successfully"}