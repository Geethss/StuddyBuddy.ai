from fastapi import FastAPI
from app.routes import upload, qa

app = FastAPI(
    title="StudyBuddy.ai API",
    description="Backend for document-based AI assistant",
    version="1.0.0"
)

app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(qa.router, prefix="/qa", tags=["QA"])

@app.get("/")
def root():
    return {"message": "Welcome to StudyBuddy.ai API"}