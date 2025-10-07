from typing import List




def recursive_character_split(
    texts: List[str],
    chunk_size: int = 1200,
    chunk_overlap: int = 200,
) -> List[str]:
    """
    Simple, robust splitter by characters with overlap.
    Takes a list of raw strings (e.g., pages/paragraphs), returns chunks.
    """
    chunks: List[str] = []
    for t in texts:
        t = " ".join(t.split())  # normalize whitespace
        if len(t) <= chunk_size:
            chunks.append(t)
            continue
        start = 0
        end = chunk_size
        while start < len(t):
            chunks.append(t[start:end])
            start = max(0, end - chunk_overlap)
            end = start + chunk_size
    return [c for c in chunks if c.strip()]