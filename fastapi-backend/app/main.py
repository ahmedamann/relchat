import os
os.environ.setdefault("LANGSMITH_API_KEY", "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")
os.environ['LANGSMITH_TRACING'] = 'true'
LANGSMITH_ENDPOINT = os.environ.get("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")
LANGSMITH_PROJECT = os.environ.get("LANGSMITH_PROJECT", "relchat")
os.environ.setdefault("LANGCHAIN_API_KEY", "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")


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router
from .auth import router as auth_router
from .db import Base, engine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

# Include Routes
app.include_router(auth_router, prefix="/auth")
app.include_router(router)