import google.generativeai as genai
import os
from serpapi import SerpApiClient

class GeminiClient:
    def __init__(self, api_key=None):
        if api_key is None:
            api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Gemini API key must be provided via argument or GEMINI_API_KEY env variable.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
    
    def search(self):
        try:
            # Define parameters for the SerpApi search
            params = {
                "engine": "google",
                "q": 'Pegasus Steel company details',
                "api_key": "10ef535b00fe562340523ffa69d27b417a77f1680f14b3c3044dfa448c6739b4",
                "location": "New York, United States" # Current location, as per your request
            }

            # Perform the search using SerpApi
            search = SerpApiClient(params)
            results = search.get_json()
            print(results)
            return results

        except Exception as e:
            raise Exception(e)

    def generate_content(self, prompt: str) -> str:
        """
        Generate content using Gemini API given a prompt.
        """
        response = self.model.generate_content(prompt)
        return response.text
