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