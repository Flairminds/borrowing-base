import os

import requests

from source.utility.ServiceResponse import ServiceResponse

class DiffBotScraperClient:
    # def __init__(self):
    #     self.diff_bot_token = os.getenv("DIFFBOT_TOKEN")
    #     self.api_url = "https://kg.diffbot.com/kg/v3/enhancedSearch"

    def scrape(self, url_to_scrape: str):
        print(url_to_scrape)
        diff_bot_token = os.getenv("DIFFBOT_TOKEN")
        api_url = "https://api.diffbot.com/v3/analyze"

        headers = {}
        params = {
            'token': diff_bot_token,
            'url': url_to_scrape
        }
        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data.get('objects'):
                print(data.get('objects')[0])
            # print("Title:", data.get('objects')[0].get('title') if data.get('objects') else "")
            # print("Author:", data.get('objects')[0].get('author') if data.get('objects') else "")
            # print("Text:", data.get('objects')[0].get('text') if data.get('objects') else "")
        else:
            print("Error:", response.status_code, response.text)
            return ServiceResponse.error(data=response.text, message="Failed to scrape the URL", error_code=response.status_code)
        return ServiceResponse.success(data=data['objects'][0].get('title'), message=f"Scraped content from {url_to_scrape}")

    def extract_data(self, content: str):
        # Placeholder for data extraction logic
        # This should include parsing the content to extract relevant information
        return f"Extracted data from content: {content}"