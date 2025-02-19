import chromadb

chroma_client = chromadb.PersistentClient(path="./data/chroma")

collection = chroma_client.get_or_create_collection(name="documents")