from fastapi import APIRouter, UploadFile, File, HTTPException
from app.vector_db.vector_store import save_text_to_vector_db


router = APIRouter(prefix="/information", tags=["Information"])


@router.post("/")
async def upload_markdown(file: UploadFile = File(...)):

    if not file.filename.endswith(".md"):
        raise HTTPException(
            status_code=400, detail="Only markdown (.md) files are allowed"
        )

    content = await file.read()

    text = content.decode("utf-8")

    save_text_to_vector_db(text=text, filename=file.filename)

    return {
        "message": "Markdown stored in vector database",
        "filename": file.filename,
        "characters": len(text),
    }
