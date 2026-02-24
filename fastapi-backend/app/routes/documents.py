from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session
from io import BytesIO
from PyPDF2 import PdfReader

from ..embeddings import delete_document, add_document, vector_store
from ..models import User, Document
from .auth import get_db
from .dependencies import get_current_user

router = APIRouter()


@router.post("/")
async def upload_file(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Upload PDF or text files, process and store them only in the vector database, and track them in SQLite."""
    if file.content_type not in ["application/pdf", "text/plain"]:
        raise HTTPException(
            status_code=400, detail="Only PDF and text files are allowed."
        )

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

    document_id = add_document(user.id, file.filename, text)

    new_doc = Document(user_id=user.id, file_name=file.filename, doc_id=document_id)
    db.add(new_doc)
    db.commit()

    return {
        "message": "File processed and stored in vector database successfully",
        "filename": file.filename,
    }


@router.get("/")
async def list_uploaded_files(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return a list of uploaded files for the authenticated user from the database."""
    docs = set()
    results = vector_store.get(where={"user_id": user.id})["metadatas"]

    for r in results:
        docs.add(r["file_name"])

    return list(docs)


@router.delete("/")
async def delete_uploaded_document(
    file_name: str = Query(..., description="The name of the document to delete"),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a document for the authenticated user."""

    deletion_result = delete_document(user.id, file_name)
    print(deletion_result)

    selected_doc = (
        db.query(Document)
        .filter(Document.user_id == user.id, Document.file_name == file_name)
        .first()
    )
    if not selected_doc:
        raise HTTPException(
            status_code=404, detail="Document not found for this user."
        )

    # delete from the sql database
    db.delete(selected_doc)
    db.commit()

    return {
        "message": f"Document '{file_name}' and its chunks have been deleted successfully"
    }

