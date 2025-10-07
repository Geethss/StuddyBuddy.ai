import os

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# Streamlit Configuration
PAGE_TITLE = "StudyBuddy.ai"
PAGE_ICON = "📚"
LAYOUT = "wide"

# File Upload Configuration
ALLOWED_FILE_TYPES = ['pdf', 'docx', 'txt']
MAX_FILE_SIZE_MB = 40

# Chat Configuration
DEFAULT_TOP_K = 5
MAX_TOP_K = 10
