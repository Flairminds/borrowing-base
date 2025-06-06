# from source.services.aiIntegration.webScraping.webScraper import DiffBotScraperClient
# from source.utility.ServiceResponse import ServiceResponse

# def scrape(web_url: str):
#     try:
#         scraper = DiffBotScraperClient()
#         response = scraper.scrape(web_url)
#         if response['status'] == False:
#             return ServiceResponse.error(data=response.data, message=response.message, error_code=response.error_code)
#         return ServiceResponse.success(data=response.data, message="Web scraping successful")
#     except Exception as e:
#         Log.func_error(e)
#         return ServiceResponse.error(message="Internal server error", error_code=500)