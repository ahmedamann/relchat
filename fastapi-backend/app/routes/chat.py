from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    Query,
)
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from .auth import get_db
from ..models import User, Conversation
from ..retriever import pipeline
from .dependencies import get_current_user

router = APIRouter() 


def store_chat_entry(
    user: User,
    conversation_id: int,
    query: str,
    response_text: str,
    db: Session,
):
    """Store the chat entry with a conversation ID."""
    chat_entry = Conversation(
        user_id=user.id,
        conversation_id=conversation_id,
        query=query,
        response=response_text,
    )
    db.add(chat_entry)
    db.commit()


def get_prev_conversation(
    db: Session,
    user: User,
    conversation_id: int,
) -> str | None:
    """
    Retrieve and format previous conversation entries for the given user and conversation ID.
    """
    entries = (
        db.query(Conversation)
        .filter(
            Conversation.user_id == user.id,
            Conversation.conversation_id == conversation_id,
        )
        .order_by(Conversation.id)
        .all()
    )

    if entries:
        formatted = "\n".join(
            f"User: {entry.query}\nBot: {entry.response}" for entry in entries
        )
        return formatted
    else:
        return None


@router.post("/")
async def chat(
    background_tasks: BackgroundTasks,
    query: str = Query(..., min_length=1),
    conversation_id: int | None = Query(None),
    new_conversation: bool = Query(False),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    if new_conversation or conversation_id is None:
        latest_convo = (
            db.query(Conversation)
            .filter(Conversation.user_id == user.id)
            .order_by(Conversation.conversation_id.desc())
            .first()
        )
        conversation_id = (latest_convo.conversation_id + 1) if latest_convo else 1

    response_buffer: list[str] = []

    chain, query = pipeline(
        user.id, get_prev_conversation(db, user, conversation_id), query
    )

    async def streamer(q: str):
        async for chunk in chain.astream(q):
            if chunk.content:
                response_buffer.append(chunk.content)
                yield chunk.content

    async def finalizer():
        full_response = "".join(response_buffer)
        store_chat_entry(user, conversation_id, query, full_response, db)

    background_tasks.add_task(finalizer)
    return StreamingResponse(streamer(query), media_type="text/plain")


@router.get("/")
async def get_chat_history(
    conversation_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieve chat messages for a specific conversation."""
    chat_history = (
        db.query(Conversation)
        .filter(
            Conversation.conversation_id == conversation_id,
            Conversation.user_id == user.id,
        )
        .all()
    )

    return [{"query": chat.query, "response": chat.response} for chat in chat_history]


@router.get("/list/")
async def list_conversation(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return a list of past Conversation for a user."""
    conversations = (
        db.query(Conversation.conversation_id)
        .filter(Conversation.user_id == user.id)
        .distinct()
        .all()
    )
    return [{"id": convo[0], "title": f"Conversation {convo[0]}"} for convo in conversations]


@router.delete("/")
async def delete_conversation(
    conversation_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a conversation and its messages."""
    deleted = (
        db.query(Conversation)
        .filter(
            Conversation.conversation_id == conversation_id,
            Conversation.user_id == user.id,
        )
        .delete()
    )

    if deleted == 0:
        raise HTTPException(status_code=404, detail="Conversation not found")

    db.commit()
    return {"message": "Conversation deleted successfully"}

