<<<<<<< HEAD
# StudyBuddy.ai

A document-grounded Q&A system with support for both OpenAI and Google Gemini AI.

## Features

- Document upload and processing (PDF, DOCX, TXT)
- Text chunking and embedding
- Vector database storage (Pinecone or Chroma)
- Q&A with context-aware responses
- Support for both OpenAI and Google Gemini AI providers

## Project Structure

```
StudyBuddy.ai/
├── backend/
│   ├── app/
│   │   ├── config.py          # Configuration settings
│   │   ├── main.py            # FastAPI application
│   │   ├── models/            # Pydantic models and schemas
│   │   ├── routes/            # API routes
│   │   ├── services/          # Business logic services
│   │   └── utils/             # Utility functions
│   ├── requirements.txt       # Python dependencies
│   └── README.md             # Backend-specific documentation
├── frontend/
│   ├── app.py                 # Streamlit application
│   ├── config.py              # Frontend configuration
│   ├── utils.py               # API utility functions
│   ├── requirements.txt       # Frontend dependencies
│   └── README.md             # Frontend-specific documentation
└── README.md                 # This file
```

## Setup

### 1. Create and Activate Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the `backend/` directory:

```env
# AI Provider Configuration
AI_PROVIDER=openai  # or "gemini"

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_CHAT_MODEL=gpt-4o-mini

# Google Gemini Configuration
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash

# Vector Database Configuration
VECTOR_DB=chroma  # or "pinecone"

# Pinecone Configuration (if using Pinecone)
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX_NAME=studybuddy-index

# Chroma Configuration (if using Chroma)
CHROMA_DIR=.chroma_store

# Chunking Configuration
CHUNK_SIZE=1200
CHUNK_OVERLAP=200

# File Upload Configuration
MAX_FILE_SIZE_MB=40
```

### 4. Run the Backend Server

```bash
cd backend
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### 5. Run the Frontend Application

In a new terminal:

```bash
cd frontend
streamlit run app.py
```

The frontend will be available at `http://localhost:8501`

## API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## API Endpoints

### Upload Document
- **POST** `/upload/`
- Upload and process documents (PDF, DOCX, TXT)
- Returns document ID and chunk count

### Ask Questions
- **POST** `/qa/`
- Ask questions about uploaded documents
- Requires document ID from upload response

## AI Provider Selection

The system supports both OpenAI and Google Gemini:

- Set `AI_PROVIDER=openai` to use OpenAI
- Set `AI_PROVIDER=gemini` to use Google Gemini
- If both APIs are configured, the system will use the specified provider
- If only one API is configured, it will automatically fall back to the available provider

## Vector Database Options

- **Chroma**: Local development (default, no additional setup required)
- **Pinecone**: Production use (requires Pinecone account and API key)

## Development

### Backend Development

The backend is built with:
- **FastAPI**: Modern, fast web framework
- **Pydantic**: Data validation and settings management
- **Google Generative AI**: Gemini API integration
- **OpenAI**: GPT API integration
- **ChromaDB/Pinecone**: Vector database storage

### Frontend Development

The frontend is built with:
- **Streamlit**: Modern web app framework for Python
- **Requests**: HTTP client for API communication
- **Custom CSS**: Styled components and responsive design

## Quick Start

1. **Setup Environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  
   ```

2. **Install Backend Dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Install Frontend Dependencies**:
   ```bash
   cd ../frontend
   pip install -r requirements.txt
   ```

4. **Configure Environment**:
   - Create `backend/.env` with your API keys (see setup section above)

5. **Run Both Services**:
   ```bash
   # Terminal 1 - Backend
   cd backend
   uvicorn app.main:app --reload
   
   # Terminal 2 - Frontend
   cd frontend
   streamlit run app.py
   ```

6. **Access the Application**:
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Next Steps

- [ ] Add authentication and user management
- [ ] Implement document summarization features
- [ ] Add quiz generation capabilities
=======
# StudyBuddy.ai (Backend)

This is the FastAPI backend for StudyBuddy.ai — an intelligent assistant that helps students summarize, understand, and chat with documents.

## Features
- Upload and parse PDFs
- Store and search using vector DBs
- Chat with your content using LLMs

## Setup

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
>>>>>>> c961582dd42b560241688411659da3cb2cf2b1d3
