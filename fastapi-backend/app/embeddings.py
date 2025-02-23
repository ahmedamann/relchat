from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import uuid

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      
    chunk_overlap=200,   
    separators=["\n\n", "\n", " ", ""],  
)

vector_store = Chroma(
    persist_directory="./data/chroma",
    embedding_function=embedding_model
)

def add_document(username: str, file_name: str, text: str):
    """Split and store document chunks in ChromaDB's vector store with metadata, including user_id."""
    doc_id = str(uuid.uuid4())

    unique_name = f"{username}_{file_name}"

    chunks = text_splitter.split_text(text)

    chunk_ids = [f"{unique_name}-{i}" for i in range(len(chunks))]

    vector_store.add_texts(
        texts=chunks,
        ids=chunk_ids,
        metadatas=[{"user_id": username, "file_name": file_name, "doc_id": doc_id, "chunk": i} for i in range(len(chunks))]
    )
    print(f"Document '{file_name}' added for user '{username}'")
    print("Stored Metadata:", vector_store.get())

    return doc_id

def delete_document(user_id: str, file_name: str):
    """Delete all document chunks related to the given file name and user."""
    
    results = vector_store.get(where={"file_name": file_name})
    
    if not results["ids"]:
        return "No chunks found for this document"

    vector_store.delete(ids=results["ids"])
    return f"Document '{file_name}' and its chunks have been deleted successfully"