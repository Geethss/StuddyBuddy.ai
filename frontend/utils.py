import requests
import streamlit as st
from typing import Optional, Dict, List
from config import API_BASE_URL

def check_api_connection() -> bool:
    """Check if the backend API is accessible"""
    try:
        response = requests.get(f"{API_BASE_URL}/docs", timeout=5)
        return response.status_code == 200
    except:
        return False

def upload_document(file) -> Optional[Dict]:
    """Upload document to backend API"""
    try:
        files = {"file": (file.name, file.getvalue(), file.type)}
        response = requests.post(f"{API_BASE_URL}/upload/", files=files)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Upload failed: {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to backend API. Make sure the backend server is running on http://localhost:8000")
        return None
    except Exception as e:
        st.error(f"Upload error: {str(e)}")
        return None

def ask_question(question: str, doc_id: str, top_k: int = 5) -> Optional[Dict]:
    """Ask question to backend API"""
    try:
        payload = {
            "question": question,
            "doc_id": doc_id,
            "top_k": top_k
        }
        response = requests.post(f"{API_BASE_URL}/qa/", json=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Question failed: {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to backend API. Make sure the backend server is running on http://localhost:8000")
        return None
    except Exception as e:
        st.error(f"Question error: {str(e)}")
        return None

def format_sources(sources: List[Dict]) -> str:
    """Format sources for display"""
    if not sources:
        return "No sources available"
    
    formatted = []
    for source in sources:
        chunk = source.get('chunk', 'N/A')
        score = source.get('score', 0)
        filename = source.get('filename', 'Unknown file')
        formatted.append(f"**Chunk {chunk}** (Score: {score:.3f}) - *{filename}*")
    
    return "\n".join(formatted)
