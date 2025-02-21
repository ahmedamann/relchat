from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router
from .auth import router as auth_router
from .db import Base, engine

app = FastAPI()

# Allow frontend (React) to access FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

Base.metadata.create_all(bind=engine)

# Include Routes
app.include_router(auth_router, prefix="/auth")
app.include_router(router)