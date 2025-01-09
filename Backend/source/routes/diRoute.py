from flask import Blueprint

from source.controllers import diController

di_blueprint = Blueprint("di_blueprint", __name__)

@di_blueprint.route("/upload_source", methods=["POST"])
def get_concentration_tests():
    return diController.upload_source_files()
    
@di_blueprint.route("/get_blobs", methods=["GET"])
def get_blobs():
    return diController.get_blobs()

@di_blueprint.route("/extract_base_data", methods=["POST"])
def extract_base_data():
    return diController.extract_base_data()

@di_blueprint.route("/get_base_data", methods=["POST"])
def get_base_data():
    return diController.get_base_data()

# @di_blueprint.route("/create_base_data", methods=["POST"])
# def create_base_data():
#     return diController.create_base_data()

@di_blueprint.route('get_extracted_base_data_info', methods=["POST"])
def get_extracted_base_data_info():
    return diController.get_extracted_base_data_info()

@di_blueprint.route('/get_pflt_sec_mapping', methods=["GET"])
def get_pflt_sec_mapping():
    return diController.get_pflt_sec_mapping()

@di_blueprint.route('/edit_pflt_sec_mapping', methods=["POST"])
def edit_pflt_sec_mapping():
    return diController.edit_pflt_sec_mapping()

@di_blueprint.route('/get_source_file_data', methods=["POST"])
def get_source_file_data():
    return diController.get_source_file_data()

@di_blueprint.route('/get_source_file_data_detail', methods=["POST"])
def get_source_file_data_detail():
    return diController.get_source_file_data_detail()