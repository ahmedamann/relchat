from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import chat, documents, root, auth
from .db import Base, engine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

# Include Routes
app.include_router(auth.router, prefix="/auth")
app.include_router(chat.router, prefix="/chat")
app.include_router(documents.router, prefix="/documents")
app.include_router(root.router)