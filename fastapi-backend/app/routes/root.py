from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def home():
    return {"message": "FastAPI is running!"}