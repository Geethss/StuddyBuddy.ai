from fastapi import APIRouter, File, UploadFile, HTTPException
from app.config import settings
from app.models.schemas import UploadResponse
from app.services.pdf_parser import extract_text_from_pdf_bytes
from app.services.docs_parser import extract_text_from_docx_bytes
from app.services.txtparser import extract_text_from_txt_bytes
from app.services.chunker import recursive_character_split
from app.services.embedder import Embedder
from app.services.retriever import VectorStore
from app.utils.helpers import file_ext, hash_text
import uuid


router = APIRouter()


_embedder = Embedder()
_store = VectorStore()




@router.post("/", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    ext = file_ext(file.filename)
    if ext not in settings.ALLOWED_EXTS:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")

    raw = await file.read()
    size_mb = len(raw) / (1024 * 1024)
    if size_mb > settings.MAX_FILE_SIZE_MB:
        raise HTTPException(status_code=413, detail=f"File too large (> {settings.MAX_FILE_SIZE_MB} MB)")

    # Extract text blocks
    if ext == "pdf":
        blocks = extract_text_from_pdf_bytes(raw)
    elif ext == "docx":
        blocks = extract_text_from_docx_bytes(raw)
    else:
        blocks = extract_text_from_txt_bytes(raw)

    if not blocks:
        raise HTTPException(status_code=422, detail="Could not extract any text from the file")

    # Chunk
    chunks = recursive_character_split(blocks, chunk_size=settings.CHUNK_SIZE, chunk_overlap=settings.CHUNK_OVERLAP)
    if not chunks:
        raise HTTPException(status_code=422, detail="No chunks produced from text")

    # Embed
    vectors = _embedder.embed(chunks)

    # Persist to vector store
    doc_id = str(uuid.uuid4())
    base_id = hash_text([file.filename, doc_id])
    ids = [f"{base_id}-{i}" for i in range(len(chunks))]
    metadatas = [{"doc_id": doc_id, "filename": file.filename, "chunk": i, "text": chunks[i]} for i in range(len(chunks))]
    _store.upsert(doc_id=doc_id, ids=ids, vectors=vectors, metadatas=metadatas)

    return UploadResponse(doc_id=doc_id, chunk_count=len(chunks), filename=file.filename)