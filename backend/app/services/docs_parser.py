from typing import List
from docx import Document
from io import BytesIO




def extract_text_from_docx_bytes(docx_bytes: bytes) -> List[str]:
    """Extract paragraphs from a DOCX file as a list of strings."""
    document = Document(BytesIO(docx_bytes))
    paras = []
    for para in document.paragraphs:
        text = para.text.strip()
        if text:
            paras.append(text)
    return paras