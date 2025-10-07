from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # OpenAI
    OPENAI_API_KEY: str = Field(default="", description="OpenAI API key")
    OPENAI_EMBEDDING_MODEL: str = Field(default="text-embedding-3-small")
    OPENAI_CHAT_MODEL: str = Field(default="gpt-4o-mini")

    # Google Gemini
    GEMINI_API_KEY: str = Field(default="", description="Google Gemini API key")
    GEMINI_MODEL: str = Field(default="gemini-2.5-flash", description="Gemini model to use")
    
    # AI Provider Selection
    AI_PROVIDER: str = Field(default="openai", description="AI provider: 'openai' or 'gemini'")


    # Vector DB
    VECTOR_DB: str = Field(default="chroma", description="pinecone | chroma")

    # Pinecone
    PINECONE_API_KEY: str = Field(default="")
    PINECONE_ENV: str = Field(default="")  # kept for legacy dashboards
    PINECONE_INDEX_NAME: str = Field(default="studybuddy-index")

    # Chroma (local dev)
    CHROMA_DIR: str = Field(default=".chroma_store")

    # Chunking
    CHUNK_SIZE: int = Field(default=1200)
    CHUNK_OVERLAP: int = Field(default=200)

    # Misc
    MAX_FILE_SIZE_MB: int = Field(default=40)
    ALLOWED_EXTS: tuple = ("pdf", "docx", "txt")

    class Config:
        env_file = ".env"


settings = Settings()