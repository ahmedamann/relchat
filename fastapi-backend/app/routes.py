from fastapi import Depends, APIRouter, HTTPException, UploadFile, File, Header, Query, BackgroundTasks
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from .auth import SECRET_KEY, ALGORITHM, get_db
from .embeddings import query_documents
from .llm import generate_response
from .models import User, Conversation
from fastapi.responses import StreamingResponse
import asyncio
import os
import aiofiles

router = APIRouter()

def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")
    token = authorization.split("Bearer ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def stream_chat_response(prompt: str, delay: float = 0.05):
    """
    Generate and stream response token by token without re-sending past tokens.
    """
    response_text = generate_response(prompt)
    words = response_text.split()

    for i in range(len(words)):
        yield words[i] + " "
        if delay > 0:
            await asyncio.sleep(delay)

def store_chat_entry(user, conversation_id, query, response_text, db: Session):
    """Store the chat entry with a conversation ID."""
    chat_entry = Conversation(user_id=user.username, conversation_id=conversation_id, query=query, response=response_text)
    db.add(chat_entry)
    db.commit()

@router.get("/chat/")
async def chat(
    background_tasks: BackgroundTasks,
    query: str = Query(..., min_length=1),
    conversation_id: int = Query(None),
    new_conversation: bool = Query(False),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    # Only create a new conversation if explicitly requested
    if new_conversation or conversation_id is None:
        latest_convo = db.query(Conversation).filter(Conversation.user_id == user.username).order_by(Conversation.conversation_id.desc()).first()
        conversation_id = (latest_convo.conversation_id + 1) if latest_convo else 1

    retrieved_docs = query_documents(query)
    context = "\n".join([doc["text"] for doc in retrieved_docs]) if retrieved_docs else "No relevant documents found."
    prompt = f""" 
    You are a helpful assistant that answers questions based on only the following Relevant Context:\n{context}\n\n
    Question: {query}\n

    Answer:
    """

    response_buffer = []

    async def streamer():
        async for chunk in stream_chat_response(prompt):
            response_buffer.append(chunk)
            yield chunk

    async def finalizer():
        full_response = "".join(response_buffer)
        store_chat_entry(user, conversation_id, query, full_response, db)

    background_tasks.add_task(finalizer)
    return StreamingResponse(streamer(), media_type="text/plain")

@router.get("/chat/history/")
async def get_chat_history(conversation_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Retrieve chat messages for a specific conversation."""
    chat_history = db.query(Conversation).filter(
        Conversation.conversation_id == conversation_id,
        Conversation.user_id == user.username
    ).all()
    
    return [{"query": chat.query, "response": chat.response} for chat in chat_history]

@router.get("/conversations/")
async def list_Conversation(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Return a list of past Conversation for a user."""
    conversations = db.query(Conversation.conversation_id).filter(
        Conversation.user_id == user.username).distinct().all()
    return [{"id": convo[0], "title": f"Conversation {convo[0]}"} for convo in conversations]


@router.post("/upload/")
async def upload_file(file: UploadFile = File(...), token: str = Depends(get_current_user)):
    """Upload PDF or text files."""
    if file.content_type not in ["application/pdf", "text/plain"]:
        raise HTTPException(status_code=400, detail="Only PDF and text files are allowed.")

    file_path = f"./uploads/{file.filename}"
    os.makedirs("./uploads", exist_ok=True)
    
    async with aiofiles.open(file_path, "wb") as f:
        content = await file.read()
        await f.write(content)

    return {"message": "File uploaded successfully", "filename": file.filename}


@router.delete("/conversations/delete/")
async def delete_conversation(conversation_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Delete a conversation and its messages."""
    deleted = db.query(Conversation).filter(
        Conversation.conversation_id == conversation_id,
        Conversation.user_id == user.username
    ).delete()

    if deleted == 0:
        raise HTTPException(status_code=404, detail="Conversation not found")

    db.commit()
    return {"message": "Conversation deleted successfully"}