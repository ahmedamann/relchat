from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import uuid

# Load embedding model via LangChain
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Initialize ChromaDB using LangChain
vector_store = Chroma(
    persist_directory="./data/chroma",
    embedding_function=embedding_model
)

# Configure recursive text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # Each chunk is ~500 characters
    chunk_overlap=200,   # Overlap for better context continuity
    separators=["\n\n", "\n", " ", ""],  # Tries splitting at paragraphs, lines, then words
)

def add_document(text: str):
    """Split and store document chunks in ChromaDB."""
    doc_id = str(uuid.uuid4())
    
    # Dynamically split text into smaller chunks
    chunks = text_splitter.split_text(text)
    
    # Store each chunk separately in the vector store
    vector_store.add_texts(
        texts=chunks,
        metadatas=[{"id": doc_id, "chunk": i, "text": chunk} for i, chunk in enumerate(chunks)]
    )
    return doc_id

def query_documents(query: str, top_k: int = 3):
    """Retrieve the most relevant document chunks."""
    results = vector_store.similarity_search(query, k=top_k)
    return [{"text": doc.metadata["text"]} for doc in results] if results else []