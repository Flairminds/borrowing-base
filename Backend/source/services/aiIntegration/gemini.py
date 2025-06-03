import google.generativeai as genai
import os

class GeminiClient:
    def __init__(self, api_key=None):
        if api_key is None:
            api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Gemini API key must be provided via argument or GEMINI_API_KEY env variable.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def generate_content(self, prompt: str) -> str:
        """
        Generate content using Gemini API given a prompt.
        """
        response = self.model.generate_content(prompt)
        return response.text
