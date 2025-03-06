from flask import Blueprint

from source.controllers import mappingController

mapping_setup_blueprint = Blueprint("mapping_setup_blueprint", __name__)

@mapping_setup_blueprint.route("/loan_type", methods=["GET"])
def get_loan_type_data():
    return mappingController.get_loan_type_data()

@mapping_setup_blueprint.route("/map_loan_type", methods=["POST"])
def map_loan_type():
    return mappingController.map_loan_type()

@mapping_setup_blueprint.route("/lien_type", methods=["GET"])
def get_lien_type_data():
    return mappingController.get_lien_type_data()

@mapping_setup_blueprint.route("/map_lien_type", methods=["POST"])
def map_lien_type():
    return mappingController.map_lien_type()