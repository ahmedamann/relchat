import chromadb
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#############################################################################
#                               VECTOR DB                                   #
#############################################################################

chroma_client = chromadb.PersistentClient(path="./data/chroma")

collection = chroma_client.get_or_create_collection(name="documents")