from openai import OpenAI
import os
from bs4 import BeautifulSoup
import requests
import urllib.parse

class OpenAIClient:
    def __init__(self, api_key=None):
        if api_key is None:
            api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key must be provided via argument or OPENAI_API_KEY env variable.")
        self.client = OpenAI(api_key=api_key)

    # Step 1: Web scraping
    def scrape_website(self):
        try:
            query = "Pegasus Steel company profile"
            response = requests.get(f"https://www.google.com/search?q={urllib.parse.quote_plus(query)}")
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Extract all text (or customize to target specific elements)
            text = soup.get_text(separator=' ', strip=True)
            print(text)
            return text[:4000]  # Limit for GPT context
        except Exception as e:
            print(str(e)[:200])

    def chat_completion(self, messages, model="gpt-4.1", store=False, temperature=0.7, **kwargs):
        """
        Generate a chat completion using OpenAI API.
        Args:
            messages (list): List of message dicts, e.g., [{"role": "user", "content": "..."}]
            model (str): Model name, default is 'gpt-4.1'.
            store (bool): Whether to store the conversation (OpenAI param).
            **kwargs: Additional parameters for the API call.
        Returns:
            str: The content of the response message.
        """
        try:
            completion = self.client.chat.completions.create(
                model=model,
                store=store,
                messages=messages,
                temperature=temperature,
                **kwargs
            )
            message = completion.choices[0].message
            return {
                "role": message.role,
                "content": message.content
            }
        except Exception as e:
            raise Exception(e)

# Example usage:
# client = OpenAIClient()
# response = client.chat_completion([
#     {"role": "user", "content": "write a haiku about ai"}
# ])
# print(response)