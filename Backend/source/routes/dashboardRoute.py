from flask import Blueprint

# from source.controllers import fileValidation
from source.controllers import dashboardController

dashboard_blueprint = Blueprint("dashboard_blueprint", __name__)


@dashboard_blueprint.route("/upload_fund_file", methods=["POST"])
def handle_upload_fund_file():
    return dashboardController.handle_upload_fund_file()


@dashboard_blueprint.route("/get_card_overview_data", methods=["POST"])
def get_card_overview_data():
    return dashboardController.get_card_overview_data()


@dashboard_blueprint.route("/get_assets_list", methods=["POST"])
def get_asset_selection_table():
    return dashboardController.get_assets_list()


@dashboard_blueprint.route("/latest_closing_date", methods=["POST"])
def get_landing_page_data():
    return dashboardController.latest_closing_date()


@dashboard_blueprint.route("/get_files_list", methods=["POST"])
def get_files_list():
    return dashboardController.get_files_list()


@dashboard_blueprint.route("/get_bb_data_of_date", methods=["POST"])
def get_response_of_date():
    return dashboardController.get_bb_data_of_date()


@dashboard_blueprint.route("/trend_graph", methods=["POST"])
def get_trend_graph():
    return dashboardController.get_trend_graph()


@dashboard_blueprint.route("/calculate_bb", methods=["POST"])
def calculate_bb():
    return dashboardController.calculate_bb()
