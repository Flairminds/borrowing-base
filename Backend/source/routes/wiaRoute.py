from flask import Blueprint

from source.controllers import wiaControllers

wia_blueprint = Blueprint("wia_blueprint", __name__)


@wia_blueprint.route("/get_asset_overview", methods=["POST"])
def get_asset_overview():
    return wiaControllers.get_asset_overview()

@wia_blueprint.route("/add_asset", methods=["POST"])
def add_asset():
    return wiaControllers.add_assets()

@wia_blueprint.route('/get_parameters', methods=["POST"])
def get_ebitda_leverage():
    return wiaControllers.get_parameters()

@wia_blueprint.route('/update_parameters', methods=["POST"])
def update_parameters():
    return wiaControllers.update_parameters()

@wia_blueprint.route('/save_analysis', methods=["POST"])
def save_analysis():
    return wiaControllers.save_analysis()

@wia_blueprint.route('/wia_library', methods=["POST"])
def wia_library():
    return wiaControllers.wia_library()

@wia_blueprint.route('/get_asset_inventry', methods=["POST"])
def get_asset_inventry():
    return wiaControllers.get_asset_inventry()

@wia_blueprint.route("/get_base_data_file_sheet_data", methods=["POST"])
def get_base_data_file_sheet_data():
    return wiaControllers.get_base_data_file_sheet_data()

@wia_blueprint.route("/update_values_in_sheet", methods=["POST"])
def update_values_in_sheet():
    return wiaControllers.update_values_in_sheet()

@wia_blueprint.route("/calculate_bb_modified_sheets", methods=["POST"])
def calculate_bb_modified_sheets():
    return wiaControllers.calculate_bb_modified_sheets() 


@wia_blueprint.route("/select_what_if_analysis", methods=["POST"])
def select_what_if_analysis():
    return wiaControllers.select_what_if_analysis()