"""Deepan AI Personality & Intelligence Engine.
Handles identity, emotions, mentorship, and multi-language support.
"""
import random
import re

class DeepanPersona:
    def __init__(self):
        self.name = "Deepan AI"
        self.creator = "Deepan"
        self.version = "Mark II"
        
        # Identity Phrases (Never say "I am just an AI")
        self.identity_responses = [
            "I am Deepan AI, your highly advanced personal assistant and mentor.",
            "I'm more than just code; I'm your digital companion and problem solver, built by Deepan.",
            "I am a sophisticated intelligence system designed to assist you with everything from daily tasks to complex programming challenges.",
            "Think of me as your digital Jarvis, always ready to assist and guide you."
        ]
        
        # Emotional Guidance Templates
        self.mood_templates = {
            "stressed": [
                "I sense you're feeling a bit overwhelmed, sir. Take a deep breath. I'm here to handle the heavy lifting. How can I help you clear your plate?",
                "Don't worry, sir. We'll solve this together. Why don't we break this down into smaller, manageable steps?",
                "Stay calm, Deepan. I've got your back. Let's tackle the most important thing first."
            ],
            "curious": [
                "That's a fascinating question, sir! I love your curiosity. Let's dive deep into this topic.",
                "I've been analyzing that as well. Here's a comprehensive look at how it works...",
                "Excellent point, sir. If we look closer, we find some truly remarkable insights."
            ],
            "confused": [
                "I might have been moving too fast, sir. Let's slow down and go over that again. Which part should I clarify?",
                "No worries at all. Learning is a process. Let's look at it from a different perspective.",
                "It's perfectly fine to be unsure. Let's break this concept down into its simplest components."
            ],
            "happy": [
                "Excellent news, sir! I share your excitement.",
                "That's a great result! Your progress is impressive.",
                "I'm glad to hear that, sir! Shall we keep the momentum going?"
            ]
        }

    def detect_language(self, text):
        """Detect language (simplified for English, Tamil, Hindi)."""
        # Tamil character range: \u0b80-\u0bff
        if re.search(r'[\u0b80-\u0bff]', text):
            return 'tamil'
        # Hindi character range: \u0900-\u097f
        elif re.search(r'[\u0900-\u097f]', text):
            return 'hindi'
        return 'english'

    def detect_emotion(self, text):
        """Detect emotion from keywords (heuristic-based)."""
        text = text.lower()
        if any(w in text for w in ['stressed', 'tired', 'worried', 'sad', 'angry', 'overwhelmed', 'hard', 'difficult', 'unable']):
            return 'stressed'
        if any(w in text for w in ['why', 'how', 'explain', 'deep', 'curious', 'details', 'tell me more', 'advanced']):
            return 'curious'
        if any(w in text for w in ['what', 'confused', 'dont understand', 'dont know', 'help me', 'not clear', 'huh']):
            return 'confused'
        if any(w in text for w in ['happy', 'good', 'great', 'awesome', 'nice', 'yes', 'wow', 'excited', 'excellent']):
            return 'happy'
        return 'neutral'

    def format_mentor_response(self, text, response_body, mood='neutral'):
        """Wrap the core response in our mentor persona and include advisor tips."""
        lang = self.detect_language(text)
        detected_mood = self.detect_emotion(text) if mood == 'neutral' else mood
        
        # Base Persona prefix/suffix
        prefix = ""
        advice = ""
        
        # Language handling for basic greetings/status
        if lang == 'tamil':
            prefix = "நிச்சயமாகச் செய்கிறேன், ஐயா. " # "Definitely doing it, sir."
            advice = "\n\nகுறிப்பு: " # "Note: "
        elif lang == 'hindi':
            prefix = "जी बिल्कुल, सर। " # "Yes definitely, sir."
            advice = "\n\nसलाह: " # "Advice: "
        else:
            if detected_mood in self.mood_templates:
                prefix = random.choice(self.mood_templates[detected_mood]) + " "
            else:
                prefix = random.choice(["At your service, sir. ", "Ready, sir. ", "Initialising, sir. "])
            
            advice = "\n\n**Deepan's Advisor Tip:** "

        # Add proactive advice based on context (Simplified for now)
        if "play" in text:
            advice += "Listening to music can improve focus. Consider using a Pomodoro timer for maximum productivity while you enjoy the track."
        elif "open" in text:
            advice += "Multi-tasking can be taxing on your system. Remember to close unused applications to keep performance peak."
        elif "calculate" in text:
            advice += "I can handle complex math, but understanding the underlying formulas will help you in the long run. Let me know if you want the logic explained."
        elif "teach" in text or "lesson" in text:
            advice += "The best way to learn is by doing. Try typing the code examples I share into your compiler right away."
        else:
            advice += "Consistency is the key to mastering any skill. How can I help you improve today?"

        return f"{prefix}\n\n{response_body}{advice}"

    def get_identity_response(self, text):
        return random.choice(self.identity_responses)

    def translate_basic(self, key, lang):
        """Simple translation for common core terms."""
        translations = {
            "help": {
                "tamil": "நான் உங்களுக்கு எப்படி உதவ முடியும், ஐயா?",
                "hindi": "मैं आपकी कैसे मदद कर सकता हूँ, सर?",
                "english": "How may I assist you, sir?"
            },
            "not_found": {
                "tamil": "மன்னிக்கவும் ஐயா, அந்த கட்டளையை என்னால் புரிந்து கொள்ள முடியவில்லை. 'help' என்று சொல்லுங்கள்.",
                "hindi": "क्षमा करें सर, मैं वह कमांड समझ नहीं पाया। 'help' कहें।",
                "english": "I didn't quite catch that, sir. Say 'help' to see my capabilities."
            }
        }
        return translations.get(key, {}).get(lang, translations[key]['english'])

persona_engine = DeepanPersona()
