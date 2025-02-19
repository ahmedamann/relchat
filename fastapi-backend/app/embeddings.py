from sentence_transformers import SentenceTransformer
import chromadb
import uuid

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="./data/chroma")
collection = chroma_client.get_or_create_collection(name="documents")

def embed_text(text: str):
    """Generate embeddings for a given text."""
    return model.encode(text).tolist()

def add_document(text: str):
    """Add a document to the vector store."""
    doc_id = str(uuid.uuid4())
    embedding = embed_text(text)
    collection.add(ids=[doc_id], embeddings=[embedding], metadatas=[{"text": text}])
    return doc_id

def query_documents(query: str, top_k: int = 5):
    """Retrieve top-k most relevant documents for a query."""
    query_embedding = embed_text(query)
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    return results["metadatas"][0] if results["documents"] else []