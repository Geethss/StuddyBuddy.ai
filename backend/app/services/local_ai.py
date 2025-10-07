from typing import List
import re


class LocalAI:
    """Simple local AI service that provides basic responses without requiring API keys."""
    
    def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        """Generate a simple response based on the context provided."""
        
        # Extract the question from the user prompt
        question_match = re.search(r'Question:\s*(.+?)\s*Answer:', user_prompt, re.DOTALL)
        if question_match:
            question = question_match.group(1).strip()
        else:
            question = "your question"
        
        # Extract context from the user prompt
        context_match = re.search(r'Context:\s*(.+?)\s*Question:', user_prompt, re.DOTALL)
        if context_match:
            context = context_match.group(1).strip()
        else:
            context = "the provided context"
        
        # Generate a simple response
        response = f"""Based on the document content, here's what I found regarding your question about "{question}":

{context}

Note: This is a basic local response. For more sophisticated AI-powered answers, please configure either an OpenAI API key or Google Gemini API key in your environment variables.

To get better responses:
1. Get an OpenAI API key from https://platform.openai.com/api-keys
2. Or get a Gemini API key from https://aistudio.google.com/app/apikey
3. Add the key to your backend/.env file

The document has been successfully processed and indexed. You can see the relevant chunks above that match your question."""
        
        return response
    
    def is_available(self) -> bool:
        """Local AI is always available."""
        return True
