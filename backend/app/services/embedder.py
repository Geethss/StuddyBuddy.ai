from typing import List
from app.config import settings


# OpenAI v1 SDK
try:
    from openai import OpenAI  # type: ignore
    _OPENAI_AVAILABLE = True
except Exception:  # pragma: no cover
    _OPENAI_AVAILABLE = False


# Local fallback
try:
    from sentence_transformers import SentenceTransformer  # type: ignore
    _ST_AVAILABLE = True
except Exception:  # pragma: no cover
    _ST_AVAILABLE = False


class Embedder:
    def __init__(self):
        self.use_openai = _OPENAI_AVAILABLE and bool(settings.OPENAI_API_KEY)
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY) if self.use_openai else None
        self.local_model = (
            SentenceTransformer("all-MiniLM-L6-v2") if (not self.use_openai and _ST_AVAILABLE) else None
        )
        if not self.use_openai and not self.local_model:
            raise RuntimeError(
                "No embedding backend available. Provide OPENAI_API_KEY or install sentence-transformers."
            )

    def embed(self, texts: List[str]) -> List[List[float]]:
        if self.use_openai:
            resp = self.client.embeddings.create(
                model=settings.OPENAI_EMBEDDING_MODEL,
                input=texts,
            )
            return [d.embedding for d in resp.data]
        # Local fallback
        return self.local_model.encode(texts, normalize_embeddings=True).tolist()