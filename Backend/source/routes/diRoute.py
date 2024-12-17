from flask import Blueprint

from source.controllers import diController

di_blueprint = Blueprint("di_blueprint", __name__)

@di_blueprint.route("/upload_source", methods=["POST"])
def get_concentration_tests():
    return diController.upload_source_files()
    
@di_blueprint.route("/get_blobs", methods=["GET"])
def get_blobs():
    return diController.get_blobs()