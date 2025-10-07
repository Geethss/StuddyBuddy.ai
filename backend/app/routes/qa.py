from fastapi import APIRouter, HTTPException
from app.models.schemas import QARequest, QAResponse
from app.services.embedder import Embedder
from app.services.retriever import VectorStore
from app.config import settings


# OpenAI chat
from openai import OpenAI

# Gemini service
from app.services.gemini_service import GeminiService

# Local AI service
from app.services.local_ai import LocalAI


router = APIRouter()


_embedder = Embedder()
_store = VectorStore()
_openai_client = OpenAI() if settings.OPENAI_API_KEY else None
_gemini_service = GeminiService() if settings.GEMINI_API_KEY else None
_local_ai = LocalAI()


SYSTEM_PROMPT = (
"You are StudyBuddy, a helpful assistant that answers strictly using the provided context. "
"If the answer is not in the context, say you don't know and suggest where to look in the document."
)


@router.post("/", response_model=QAResponse)
async def ask_qna(payload: QARequest):
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="Question is empty")

    q_vec = _embedder.embed([payload.question])[0]

    matches = _store.query(doc_id=payload.doc_id, vector=q_vec, top_k=payload.top_k)
    if not matches:
        raise HTTPException(status_code=404, detail="No context found for the given document id")

    # Build context
    ctx_parts = []
    sources = []
    for mid, score, meta in matches:
        txt = meta.get("text", "")
        ctx_parts.append(f"- {txt}")
        sources.append({
            "id": mid,
            "score": score,
            "chunk": meta.get("chunk"),
            "filename": meta.get("filename"),
        })
    context = "\n".join(ctx_parts)

    user_prompt = (
        f"Answer the question using only the context below.\n\nContext:\n{context}\n\n"
        f"Question: {payload.question}\n\nAnswer:"
    )

    # Generate answer using the configured AI provider
    if settings.AI_PROVIDER.lower() == "gemini" and _gemini_service:
        answer = _gemini_service.generate_response(SYSTEM_PROMPT, user_prompt)
    elif settings.AI_PROVIDER.lower() == "openai" and _openai_client:
        chat = _openai_client.chat.completions.create(
            model=settings.OPENAI_CHAT_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1
        )
        answer = chat.choices[0].message.content
    else:
        # Fallback logic: use whichever service is available
        if _gemini_service and _gemini_service.is_available():
            answer = _gemini_service.generate_response(SYSTEM_PROMPT, user_prompt)
        elif _openai_client and settings.OPENAI_API_KEY:
            chat = _openai_client.chat.completions.create(
                model=settings.OPENAI_CHAT_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1
            )
            answer = chat.choices[0].message.content
        else:
            # Use local AI as final fallback
            answer = _local_ai.generate_response(SYSTEM_PROMPT, user_prompt)

    return QAResponse(answer=answer, sources=sources, used_chunks=len(matches))