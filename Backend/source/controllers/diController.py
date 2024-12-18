import flask

from source.services.diServices import diService
from source.utility.HTTPResponse import HTTPResponse
from source.utility.Log import Log

def upload_source_files():
    try:
        files = flask.request.files.getlist("files")
        reporting_date = flask.request.form.get("reporting_date")
        
        service_response = diService.upload_src_file_to_az_storage(files, reporting_date)
        
        if not service_response["success"]:
            return HTTPResponse.error(message = service_response["message"], status_code = service_response["status_code"])
        
        Log.func_success(message=service_response["message"])
        return HTTPResponse.success(message=service_response["message"])

    except Exception as e:
        Log.func_error(e)
        return HTTPResponse.error(message="Internal server error", status_code=500)

def get_blobs():
    try:
        service_response = diService.get_files_list()
        return HTTPResponse.success(message=service_response["message"], result=service_response["data"])
    except Exception as e:
        Log.func_error(e)
        return HTTPResponse.error(message="Could not get files", status_code=500)
    
def extract_base_data():
    try:
        req_body = flask.request.get_json()
        cash_file_id = req_body.get("cash_file_id")
        master_comp_file_id = req_body.get("master_comp_file_id")
        service_response = diService.extract_base_data(cash_file_id, master_comp_file_id)
        if not service_response["success"]:
            return HTTPResponse.error(message=service_response.get("message"), status_code=service_response.get("status_code"), data=service_response.get("data"))

        return HTTPResponse.success(message=service_response["message"], result=service_response["data"])
    except Exception as e:
        Log.func_error(e)
        return HTTPResponse.error(message="Could not generate base data", status_code=500)