from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter(prefix="/information", tags=["Authentication"])


@router.post("/")
async def upload_markdown(file: UploadFile = File(...)):

    if not file.filename.endswith(".md"):
        raise HTTPException(
            status_code=400, detail="Only markdown (.md) files are allowed"
        )

    content = await file.read()

    text = content.decode("utf-8")

    return {"filename": file.filename, "content": text}
