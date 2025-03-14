import chromadb
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./db_data/database.db")

if DATABASE_URL.startswith("sqlite:///"):
    os.makedirs(os.path.dirname(DATABASE_URL.replace("sqlite:///", "")), exist_ok=True)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#############################################################################
#                               VECTOR DB                                   #
#############################################################################

def get_chroma_client():
    """Returns a persistent ChromaDB client instance."""
    return chromadb.PersistentClient(path="./data/chroma")

def get_chroma_collection():
    """Returns the 'documents' collection from ChromaDB."""
    chroma_client = get_chroma_client()
    return chroma_client.get_or_create_collection(name="documents")