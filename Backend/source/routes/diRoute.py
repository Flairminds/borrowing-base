from flask import Blueprint

from source.controllers import diController

di_blueprint = Blueprint("di_blueprint", __name__)

@di_blueprint.route("/upload_source", methods=["POST"])
def get_concentration_tests():
    return diController.upload_source_files()
    
@di_blueprint.route("/get_blobs", methods=["POST"])
def get_blobs():
    return diController.get_blobs()

@di_blueprint.route("/extract_base_data", methods=["POST"])
def extract_base_data():
    return diController.extract_base_data()

@di_blueprint.route("/get_base_data", methods=["POST"])
def get_base_data():
    return diController.get_base_data()

@di_blueprint.route("/change_bd_col_seq", methods=["POST"])
def change_bd_col_seq():
    return diController.change_bd_col_seq()

@di_blueprint.route("/get_base_data_col", methods=["POST"])
def get_base_data_col():
    return diController.get_base_data_col()

@di_blueprint.route("/update_bd_col_select", methods=["POST"])
def update_bd_col_select():
    return diController.update_bd_col_select()

@di_blueprint.route('/edit_base_data', methods=['POST'])
def edit_base_data():
    return diController.edit_base_data()

@di_blueprint.route('get_extracted_base_data_info', methods=["POST"])
def get_extracted_base_data_info():
    return diController.get_extracted_base_data_info()

@di_blueprint.route('/get_pflt_sec_mapping', methods=["GET"])
def get_pflt_sec_mapping():
    return diController.get_pflt_sec_mapping()

@di_blueprint.route('/edit_pflt_sec_mapping', methods=["POST"])
def edit_pflt_sec_mapping():
    return diController.edit_pflt_sec_mapping()

@di_blueprint.route('/add_sec_mapping', methods=["POST"])
def add_sec_mapping():
    return diController.add_sec_mapping()

@di_blueprint.route('/get_source_file_data', methods=["POST"])
def get_source_file_data():
    return diController.get_source_file_data()

@di_blueprint.route('/get_source_file_data_detail', methods=["POST"])
def get_source_file_data_detail():
    return diController.get_source_file_data_detail()

@di_blueprint.route('/trigger_bb_calculation', methods=["POST"])
def trigger_bb_calculation():
    return diController.trigger_bb_calculation()

@di_blueprint.route('/add_to_archived_files', methods=["PUT"])
def add_to_archived_files():
    return diController.add_to_archived_files()

@di_blueprint.route('/get_archived_files', methods=["GET"])
def get_archived_files():
    return diController.get_archived_files()

@di_blueprint.route('/pflt_base_data_other_info', methods=["POST"])
def pflt_base_data_other_info():
    return diController.pflt_base_data_other_info()
