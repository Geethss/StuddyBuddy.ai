from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import upload, qa


app = FastAPI(
title="StudyBuddy.ai API",
description="Backend for document-grounded Q&A, summaries, and quizzes",
version="0.1.0",
)


# CORS (allow all in dev; tighten for prod)
app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)


# Routers
app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(qa.router, prefix="/qa", tags=["QA"])