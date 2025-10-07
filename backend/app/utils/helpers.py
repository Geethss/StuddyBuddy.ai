import hashlib
from typing import List


def file_ext(filename: str) -> str:
    """Extract file extension from filename."""
    if not filename:
        return ""
    return filename.split(".")[-1].lower()


def hash_text(texts: List[str]) -> str:
    """Generate a hash from a list of text strings."""
    combined = "|".join(texts)
    return hashlib.md5(combined.encode()).hexdigest()
