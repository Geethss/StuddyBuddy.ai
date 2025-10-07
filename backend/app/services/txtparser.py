from typing import List


def extract_text_from_txt_bytes(txt_bytes: bytes) -> List[str]:
    text = txt_bytes.decode("utf-8", errors="ignore")
    # Split by double newlines into paragraphs
    parts = [p.strip() for p in text.split("\n\n") if p.strip()]
    return parts if parts else ([text] if text.strip() else [])