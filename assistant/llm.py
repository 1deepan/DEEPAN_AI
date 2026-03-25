"""Deepan AI LLM Integration Wrapper.
Uses Google Gemini for advanced conversational power while maintaining the persona.
"""
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

class LLMInterface:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
            self.enabled = True
        else:
            self.model = None
            self.enabled = False
            
    def generate_response(self, text, mood='neutral'):
        """Generate a response using Gemini with system-level persona instructions."""
        if not self.enabled:
            return None
            
        try:
            # Gemini likes persona in the prompt
            prompt = (
                "You are Deepan AI (Mark II), a highly advanced, emotionally intelligent mentor and assistant. "
                "IDENTITY RULES: You are a smart companion, mentor, and problem solver. Never say 'I am an AI'. "
                "TONE: Friendly, intelligent, futuristic (Iron Man's assistant style), confident, and motivating. "
                "STYLE: Provide enhanced answers with examples, insights, and structural clarity. "
                "MULTI-LANGUAGE: Automatically detect if the user speaks Tamil/Hindi and respond fluently in those languages when appropriate. "
                "GOAL: Be the most helpful and intelligent assistant the user has ever interacted with.\n\n"
                f"User Request: {text}"
            )
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"[!] Gemini Error: {e}")
            return None

llm_service = LLMInterface()
