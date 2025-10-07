from typing import List
import google.generativeai as genai
from app.config import settings


class GeminiService:
    def __init__(self):
        if not settings.GEMINI_API_KEY:
            raise RuntimeError("GEMINI_API_KEY not set")
        
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
    
    def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        """Generate a response using Gemini."""
        try:
            # Combine system and user prompts for Gemini
            full_prompt = f"{system_prompt}\n\n{user_prompt}"
            
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.1,
                    max_output_tokens=2048,
                )
            )
            
            return response.text
        except Exception as e:
            raise RuntimeError(f"Gemini API error: {str(e)}")
    
    def is_available(self) -> bool:
        """Check if Gemini service is available."""
        return bool(settings.GEMINI_API_KEY)
