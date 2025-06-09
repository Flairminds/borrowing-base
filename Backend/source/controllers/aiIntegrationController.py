from source.utility.Log import Log
from source.utility.HTTPResponse import HTTPResponse

from source.services.aiIntegration.webScraping.webScraper import DiffBotScraperClient
from source.services.aiIntegration.webScraping.ScraperAPI import ScrapperApiClient

def search():
    try:
        web_url = "https://www.4wall.com/about"
        # web_url = "https://www.crunchbase.com/organization/4wall-entertainment"
        # web_url = "https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://www.spglobal.com/market-intelligence/en/solutions/products/sp-capital-iq-pro&ved=2ahUKEwi_oLvkhNyNAxV1ATQIHVuiK4AQFnoECBwQAQ"
        # web_url = "https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://www.targetedpetcare.com/&ved=2ahUKEwi19eiliNyNAxWohv0HHXdfKp8QFnoECCQQAQ"

        # scraper_client = DiffBotScraperClient()
        scraper_client = ScrapperApiClient()
        print(web_url)
        response = scraper_client.scrape(web_url)
        if response['success'] is False:
            return HTTPResponse.error(result=response["data"], message=response["message"], error_code=response.get("error_code"))
        return HTTPResponse.success(result=response["data"], message=response["message"])
    
    except Exception as e:
        Log.func_error(e)
        return HTTPResponse.error()