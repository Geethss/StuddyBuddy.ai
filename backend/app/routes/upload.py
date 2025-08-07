from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    return JSONResponse(content={"filename": file.filename, "status": "received"})