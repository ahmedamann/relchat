from fastapi import APIRouter

from .root import router as root_router
from .documents import router as documents_router
from .chat import router as chat_router

router = APIRouter()

router.include_router(root_router)
router.include_router(documents_router)
router.include_router(chat_router)

