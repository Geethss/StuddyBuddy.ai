from typing import List, Dict, Tuple
from app.config import settings


try:
    from pinecone import Pinecone
    _PC_AVAILABLE = True
except Exception:  # pragma: no cover
    _PC_AVAILABLE = False


try:
    import chromadb
    from chromadb.config import Settings as ChromaSettings
    _CHROMA_AVAILABLE = True
except Exception:  # pragma: no cover
    _CHROMA_AVAILABLE = False




class VectorStore:
    def __init__(self):
        self.backend = settings.VECTOR_DB.lower()
        if self.backend == "pinecone":
            if not _PC_AVAILABLE:
                raise RuntimeError("pinecone package not installed")
            if not settings.PINECONE_API_KEY:
                raise RuntimeError("PINECONE_API_KEY not set")
            self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
            self.index = self.pc.Index(settings.PINECONE_INDEX_NAME)
        elif self.backend == "chroma":
            if not _CHROMA_AVAILABLE:
                raise RuntimeError("chromadb package not installed")
            self.client = chromadb.PersistentClient(
                path=settings.CHROMA_DIR,
                settings=ChromaSettings(allow_reset=True),
            )
            # collection per document id; will be created on demand
        else:
            raise RuntimeError("Unsupported VECTOR_DB. Use 'pinecone' or 'chroma'.")


    # ---- Upsert ----
    def upsert(self, doc_id: str, ids: List[str], vectors: List[List[float]], metadatas: List[Dict]):
        if self.backend == "pinecone":
            # Pinecone supports metadata per vector
            vectors_to_upsert = []
            for i, (vector, metadata) in enumerate(zip(vectors, metadatas)):
                vectors_to_upsert.append({
                    "id": ids[i],
                    "values": vector,
                    "metadata": metadata
                })
            self.index.upsert(vectors=vectors_to_upsert)
        elif self.backend == "chroma":
            # Get or create collection for this document
            collection_name = f"doc_{doc_id}"
            try:
                collection = self.client.get_collection(collection_name)
            except:
                collection = self.client.create_collection(collection_name)
            
            collection.add(
                ids=ids,
                embeddings=vectors,
                metadatas=metadatas
            )

    # ---- Query ----
    def query(self, doc_id: str, vector: List[float], top_k: int = 5) -> List[Tuple[str, float, Dict]]:
        """Query for similar vectors and return (id, score, metadata) tuples."""
        if self.backend == "pinecone":
            results = self.index.query(
                vector=vector,
                top_k=top_k,
                filter={"doc_id": doc_id},
                include_metadata=True
            )
            matches = []
            for match in results.matches:
                matches.append((match.id, match.score, match.metadata))
            return matches
        elif self.backend == "chroma":
            collection_name = f"doc_{doc_id}"
            try:
                collection = self.client.get_collection(collection_name)
                results = collection.query(
                    query_embeddings=[vector],
                    n_results=top_k
                )
                matches = []
                for i, (id_val, distance, metadata) in enumerate(zip(
                    results["ids"][0], 
                    results["distances"][0], 
                    results["metadatas"][0]
                )):
                    # Convert distance to similarity score (1 - distance for cosine similarity)
                    score = 1 - distance
                    matches.append((id_val, score, metadata))
                return matches
            except:
                return []
        return []