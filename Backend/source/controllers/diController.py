import flask
import threading

from source.services.diServices import diService
from source.utility.HTTPResponse import HTTPResponse
from source.utility.Log import Log
from Exceptions.StdFileFormatException import StdFileFormatException

def upload_source_files():
    try:
        files = flask.request.files.getlist("files")
        reporting_date = flask.request.form.get("reporting_date")
        fund_type = flask.request.form.getlist("fund_type")
        # diservice.storeSourceinDB (source_file and upload file to db table)
        source_files_list = []
        service_response = diService.upload_src_file_to_az_storage(files, reporting_date, fund_type, source_files_list)
        
        if not service_response["success"]:
            return HTTPResponse.error(message = service_response["message"], status_code = service_response["status_code"])
        
        Log.func_success(message=service_response["message"])

        threading.Thread(target=diService.extract_validate_store_update,
            kwargs={"source_files_list" : source_files_list}
        ).start()

        return HTTPResponse.success(message=service_response["message"])
    except Exception as e:
        Log.func_error(e)
        return HTTPResponse.error(message="Internal server error", status_code=500)

def get_blobs():
    try:
        req_body = flask.request.get_json()
        fund_type = req_body.get("fund_type")
        service_response = diService.get_blob_list(fund_type)
        return HTTPResponse.success(message=service_response["message"], result=service_response["data"])
    except Exception as e:
        Log.func_error(e)
        return HTTPResponse.error(message="Could not get files", status_code=500)
    
def extract_base_data():
    try:
        req_body = flask.request.get_json()
        file_ids = req_body.get("files_list")
        fund_type = req_body.get("fund_type")
        service_response = diService.extract_base_data(file_ids, fund_type)
        if not service_response["success"]:
            return HTTPResponse.error(message=service_response.get("message"), status_code=service_response.get("status_code"))

        return HTTPResponse.success(message=service_response["message"], result=service_response["data"])
    except Exception as e:
        Log.func_error(e)
        return HTTPResponse.error(message="Could not generate base data", status_code=500)
    
def get_base_data():
    try:
        req_body = flask.request.get_json()
        info_id = req_body.get("info_id")
        service_response = diService.get_base_data(info_id)
        if not service_response["success"]:
            return HTTPResponse.error(message="Could not get base data")
        # base_data_map_res = diService.get_base_data_mapping(info_id)
        fund_type = service_response["data"]["fund_type"]
        other_info = diService.get_base_data_other_info(info_id, fund_type)
        result = {
            "base_data_table": service_response["data"]["base_data_table"],
            "report_date": service_response["data"]["report_date"],
            "fund_type": service_response["data"]["fund_type"],
            "card_data": service_response["data"]["card_data"],
            "other_info": other_info["data"]
            # "base_data_mapping": base_data_map_res["data"]
        }
        return HTTPResponse.success(message=service_response["message"], result=result)
    except Exception as e:
        Log.func_error(e)
        return HTTPResponse.error(message="Internal Server Error", status_code=500)

def change_bd_col_seq():
    try:
        req_body = flask.request.get_json()
        updated_sequence = req_body.get("updated_sequence")
        service_response = diService.change_bd_col_seq(updated_sequence)
        if not service_response["success"]:
            return HTTPResponse.error(message="Could not change sequence of base data columns")
        # base_data_map_res = diService.get_base_data_mapping(info_id)
        
        return HTTPResponse.success(message=service_response["message"], result=service_response["data"])
    except Exception as e:
        Log.func_error(e)
        return HTTPResponse.error(message="Internal Server Error", status_code=500)
    
def get_base_data_col():
    try:
        req_body = flask.request.get_json()
        fund_type = req_body.get("fund_type")
        service_response = diService.get_base_data_col(fund_type)
        if not service_response["success"]:
            return HTTPResponse.error(message="Could not get base data columns")
        
        return HTTPResponse.success(message=service_response["message"], result=service_response["data"])
    except Exception as e:
        Log.func_error(e)
        return HTTPResponse.error(message="Internal Server Error", status_code=500)
    
def update_bd_col_select():
    try:
        req_body = flask.request.get_json()
        selected_col_ids = req_body.get("selected_col_ids")
        fund_type = req_body.get('fund_type')
        service_response = diService.update_bd_col_select(selected_col_ids, fund_type)
        if not service_response["success"]:
            return HTTPResponse.error(message="Could not update base data columns selection")
        
        return HTTPResponse.success(message=service_response["message"], result=service_response["data"])
    except Exception as e:
        Log.func_error(e)
        return HTTPResponse.error(message="Internal Server Error", status_code=500)
    
def edit_base_data():
    try:
        req_body = flask.request.get_json()
        changes = req_body.get("changes")
        service_response = diService.edit_base_data(changes)
        if not service_response["success"]:
            return HTTPResponse.error(message="Could not edit base data")
        return HTTPResponse.success(message=service_response["message"])
    except Exception as e:
        Log.func_error(e)
        return HTTPResponse.error(message="Internal Server Error", status_code=500)
    
def create_base_data():
    try:
        req_body = flask.request.get_json()
        report_date = req_body.get("report_date")
        company_id = req_body.get("company_id")
        service_response = diService.create_base_data(report_date, company_id)
        if not service_response["success"]:
            return HTTPResponse.error(message="Could not get base data")
        return HTTPResponse.success(message=service_response["message"], result=service_response["data"])
    except StdFileFormatException as ffe:
        return (
            flask.jsonify(
                {
                    "error": True,
                    "error_type": "File Format Error",
                    "error_message": ffe.error_map,
                }
            ),
            400,
        )
    except Exception as e:
        Log.func_error(e)
        return HTTPResponse.error(message="Internal Server Error", status_code=500)

def get_extracted_base_data_info():
    try:
        req_body = flask.request.get_json()
        # report_date = req_body.get("report_date")
        # company_id = req_body.get("company_id")
        company_id = 1
        extracted_base_data_info_id = req_body.get("extracted_base_data_info_id")
        fund_type = req_body.get("fund_type")
        service_response = diService.get_extracted_base_data_info(company_id, extracted_base_data_info_id, fund_type)
        if not service_response["success"]:
            return HTTPResponse.error(message="Could not get extracted files list")
        return HTTPResponse.success(message=service_response.get("message"), result=service_response["data"])
    except Exception as e:
        Log.func_error(e)
        return HTTPResponse.error(message="Internal Server Error", status_code=500)
    

def get_pflt_sec_mapping():
    try:
        service_response = diService.get_pflt_sec_mapping()
        if not service_response["success"]:
            return HTTPResponse.error(message="Could not get PFLT Security Mapping")
        return HTTPResponse.success(message=service_response.get("message"), result=service_response["data"])
    except Exception as e:
        Log.func_error(e)
        return HTTPResponse.error(message="Internal Server Error", status_code=500)
    
def edit_pflt_sec_mapping():
    try:
        req_body = flask.request.get_json()
        changes = req_body.get('changes')

        service_response = diService.edit_pflt_sec_mapping(changes)
        if not service_response["success"]:
            return HTTPResponse.error(message="Could not edit PFLT Security Mapping")
        return HTTPResponse.success(message=service_response.get("message"))
    except Exception as e:
        Log.func_error(e)
        return HTTPResponse.error(message="Internal Server Error", status_code=500)

def add_sec_mapping():
    try:
        req_body = flask.request.get_json()
        cashfile_security_name = req_body.get("cashfile_security_name")
        family_name = req_body.get("family_name")
        master_comp_security_name = req_body.get("master_comp_security_name")
        security_type = req_body.get("security_type")
        soi_name = req_body.get("soi_name")

        service_response = diService.add_pflt_sec_mapping(cashfile_security_name, family_name, master_comp_security_name, security_type, soi_name)
        if not service_response["success"]:
            return HTTPResponse.error(message="Could not add Security Mapping")
        return HTTPResponse.success(message=service_response.get("message"))
    except Exception as e:
        Log.func_error(e)
        return HTTPResponse.error(message="Internal Server Error", status_code=500)

def get_source_file_data():
    try:
        req_body = flask.request.get_json()
        source_file_id = req_body.get('source_file_id')
        source_file_type = req_body.get('source_file_type')
        sheet_name = req_body.get('sheet_name')
        service_response = diService.get_source_file_data(source_file_id, source_file_type, sheet_name)
        if not service_response["success"]:
            return HTTPResponse.error(message="Could not get source file data")
        return HTTPResponse.success(message=service_response.get("message"), result=service_response["data"])
    except Exception as e:
        Log.func_error(e)
        return HTTPResponse.error(message="Internal Server Error", status_code=500)

def get_source_file_data_detail():
    try:
        if not flask.request.data:
            return HTTPResponse.error(message="Request body not provided", status_code=400)
        req_body = flask.request.get_json()
        ebd_id = req_body.get('ebd_id')
        column_key = req_body.get('column_key')
        data_id = req_body.get('data_id')
        if not ebd_id or not column_key:
            return HTTPResponse.error(message="Bad Request", status_code=400)
        service_response = diService.get_source_file_data_detail(ebd_id, column_key, data_id)
        if not service_response["success"]:
            return HTTPResponse.error(message=service_response['message'], status_code=service_response['status_code'])
        return HTTPResponse.success(result=service_response["data"])
    except Exception as e:
        Log.func_error(e)
        return HTTPResponse.error(message="Internal Server Error", status_code=500)

def trigger_bb_calculation():
    try:
        req_body = flask.request.get_json()
        bdi_id = req_body.get('bdi_id')
        service_response = diService.trigger_bb_calculation(bdi_id)
        # if not service_response["success"]:
        #     return HTTPResponse.error(message="Could not get source file data")
        return HTTPResponse.success(message="Successfully processed. Visit the Borrowing Base module to check the data.", result=[])
    except Exception as e:
        # Log.func_error(e)
        print("here",e)
        return HTTPResponse.error(message="Internal Server Error", status_code=500)
    
def update_archived_files():
    try:
        data = flask.request.get_json()
        list_of_ids = data.get("list_of_ids", [])
        to_archive =  data.get("to_archive")
        response = diService.update_archive(list_of_ids, to_archive)
        if (response["success"]):
            return HTTPResponse.success()
            
        return HTTPResponse.success()
    except Exception as e:
        Log.func_error(e)
        return HTTPResponse.error(message="Internal Server Error", status_code=500)

def get_archived_files():
    try:
        response = diService.get_archived_file_list()
        if (response["success"]):
            return HTTPResponse.success(result=response)
        
        return HTTPResponse.error(message="Internal Server Error")
    except Exception as e:
        Log.func_error(e)
        return HTTPResponse.error(message="Internal Server Error")
    
def base_data_other_info():
    try:
        req_body = flask.request.get_json()
        extraction_info_id = req_body.get("extraction_info_id")
        determination_date= req_body.get("determination_date")
        fund_type = req_body.get("fund_type")
        other_data = req_body.get("other_data")

        if(fund_type == "PFLT"):
            minimum_equity_amount_floor= req_body.get("minimum_equity_amount_floor")
            service_response = diService.pflt_add_base_data_other_info(extraction_info_id, determination_date, minimum_equity_amount_floor,fund_type, other_data)
        if(fund_type == "PCOF"):
            revolving_closing_date= req_body.get("revolving_closing_date")
            service_response = diService.pcof_add_base_data_other_info(extraction_info_id, determination_date, revolving_closing_date, fund_type, other_data)

        
        if(service_response["success"]):
            return HTTPResponse.success(message=service_response.get("message"))

        return HTTPResponse.error(message=service_response.get('message'), status_code=500)
    except Exception as e:
        Log.func_error(e=e)
        return HTTPResponse.error(message="Internal Server Error", status_code=500)
