from fastapi import Depends, APIRouter, HTTPException, UploadFile, File, Header, Query, BackgroundTasks
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from .auth import SECRET_KEY, ALGORITHM, get_db
from .embeddings import delete_document, add_document, retriever
from .models import User, Conversation, Document
from fastapi.responses import StreamingResponse
from .llm import llm
from .prompts import main_prompt
from io import BytesIO
from PyPDF2 import PdfReader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

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
    

########################################################################################################
#                                           DOCUMENTS                                                  #
########################################################################################################

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Upload PDF or text files, process and store them only in the vector database, and track them in SQLite."""
    if file.content_type not in ["application/pdf", "text/plain"]:
        raise HTTPException(status_code=400, detail="Only PDF and text files are allowed.")
    
    file_bytes = await file.read()
    
    if file.content_type == "application/pdf":
        pdf_file = BytesIO(file_bytes)
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    else:
        text = file_bytes.decode("utf-8", errors="ignore")

    document_id = add_document(user.username, file.filename, text)

    new_doc = Document(user_id=user.username, file_name=file.filename, doc_id=document_id)
    db.add(new_doc)
    db.commit()

    return {"message": "File processed and stored in vector database successfully", "filename": file.filename}


@router.get("/files/")
async def list_uploaded_files(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Return a list of uploaded files for the authenticated user from the database."""
    documents = db.query(Document).filter(Document.user_id == user.username).all()
    # Return only the file names (or additional info if needed)
    return [doc.file_name for doc in documents]


@router.delete("/documents/delete/")
async def delete_uploaded_document(
    file_name: str = Query(..., description="The name of the document to delete"),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a document for the authenticated user."""
    selected_doc = db.query(Document).filter(Document.user_id == user.username, Document.file_name == file_name).first()
    if not selected_doc:
        raise HTTPException(status_code=404, detail="Document not found for this user.")
    deletion_result = delete_document(user.username, file_name)

    # Delete the database record
    db.delete(selected_doc)
    db.commit()

    return {"message": f"Document '{file_name}' and its chunks have been deleted successfully"}


########################################################################################################
#                                           CHATS                                                      #
########################################################################################################

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

    # Create a new conversation if explicitly requested or if no conversation_id exists.
    if new_conversation or conversation_id is None:
        latest_convo = (
            db.query(Conversation)
            .filter(Conversation.user_id == user.username)
            .order_by(Conversation.conversation_id.desc())
            .first()
        )
        conversation_id = (latest_convo.conversation_id + 1) if latest_convo else 1

    response_buffer = []

    rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | main_prompt
    | llm
    | StrOutputParser()
    )

    async def streamer(query):
        try:
            for chunk in rag_chain.stream(query):
                response_buffer.append(chunk)
                yield chunk
        except Exception as e:
            print("Error in streaming:", e)

    async def finalizer():
        full_response = "".join(response_buffer)
        store_chat_entry(user, conversation_id, query, full_response, db)

    background_tasks.add_task(finalizer)
    return StreamingResponse(streamer(query), media_type="text/plain")

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