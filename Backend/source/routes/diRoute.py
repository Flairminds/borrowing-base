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

@di_blueprint.route('/get_unmapped_cash_sec', methods=["POST"])
def get_unmapped_cash_sec():
    return diController.get_unmapped_cash_sec()

@di_blueprint.route('/get_cash_securities', methods=["POST"])
def get_cash_sec():
    return diController.get_cash_sec()

@di_blueprint.route('/get_unmapped_pflt_sec', methods=["POST"])
def get_unmapped_pflt_sec():
    return diController.get_unmapped_pflt_sec()

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

@di_blueprint.route('/update_archived_files', methods=["PUT"])
def add_to_archived_files():
    return diController.update_archived_files()

@di_blueprint.route('/get_archived_files', methods=["GET"])
def get_archived_files():
    return diController.get_archived_files()

@di_blueprint.route('/base_data_other_info', methods=["POST"])
def base_data_other_info():
    return diController.base_data_other_info()

@di_blueprint.route('/add_base_data', methods=["POST"])
def add_base_data():
    return diController.add_base_data()

@di_blueprint.route('/validate_add_securities', methods=["POST"])
def validate_add_securities():
    return diController.validate_add_securities()

@di_blueprint.route('/compare_file_columns', methods=["POST"])
def compare_file_columns():
    return diController.compare_file_columns()

@di_blueprint.route('/save_mapped_columns', methods=["PATCH"])
def save_mapped_columns():
    return diController.save_mapped_columns()

@di_blueprint.route('/add_vae_data', methods=["POST"])
def add_vae_data():
    return diController.add_vae_data()

@di_blueprint.route('/get_vae_data', methods=["GET"])
def get_vae_data():
    return diController.get_vae_data()