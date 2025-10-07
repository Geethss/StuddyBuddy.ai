from typing import List
import fitz # PyMuPDF




def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> List[str]:
    """
    Extract text from a PDF (bytes) using PyMuPDF, return a list of page texts.
    """
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    pages = []
    for page in doc:
        text = page.get_text("text")
        if text and text.strip():
            pages.append(text)
    return pages