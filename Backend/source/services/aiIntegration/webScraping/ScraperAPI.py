import os
import requests

from source.utility.ServiceResponse import ServiceResponse

class ScrapperApiClient:
    def scrape(self, target_url: str):
        print(target_url)
        SCRAPER_API_KEY = os.getenv("SCRAPPER_API_KEY")
        
        params = {
            'api_key': SCRAPER_API_KEY,
            'url': target_url,
            'render': 'true'
        }

        response = requests.get('http://api.scraperapi.com/', params=params)

        if response.status_code == 200:
            # data = response.json()
            html_content = response.text
            print(html_content[:500])  # print first 500 characters
        else:
            print("Error:", response.status_code, response.text)
            return ServiceResponse.error(data=response.text, message="Failed to scrape the URL", error_code=response.status_code)
        return ServiceResponse.success(message=f"Scraped content from {target_url}")