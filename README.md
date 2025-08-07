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
