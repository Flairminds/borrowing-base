from flask import Blueprint

from source.controllers import aiIntegrationController

web_scraping_blueprint = Blueprint("web_scraping_blueprint", __name__)

@web_scraping_blueprint.route("/scrap", methods=["POST"])
def scrap():
    return aiIntegrationController.search()