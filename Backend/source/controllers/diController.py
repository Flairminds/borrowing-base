import flask

from source.services.diServices import diService
from source.utility.HTTPResponse import HTTPResponse
from source.utility.Log import Log
from Exceptions.StdFileFormatException import StdFileFormatException

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
        service_response = diService.get_blob_list()
        return HTTPResponse.success(message=service_response["message"], result=service_response["data"])
    except Exception as e:
        Log.func_error(e)
        return HTTPResponse.error(message="Could not get files", status_code=500)
    
def extract_base_data():
    try:
        req_body = flask.request.get_json()
        files_list = req_body.get("files_list")
        service_response = diService.extract_base_data(files_list)
        if not service_response["success"]:
            return HTTPResponse.error(message=service_response.get("message"), status_code=service_response.get("status_code"))

        return HTTPResponse.success(message=service_response["message"], result=service_response["data"])
    except Exception as e:
        Log.func_error(e)
        return HTTPResponse.error(message="Could not generate base data", status_code=500)
    
def get_base_data():
    try:
        req_body = flask.request.get_json()
        report_date = req_body.get("report_date")
        company_id = req_body.get("company_id")
        service_response = diService.get_base_data(report_date, company_id)
        if not service_response["success"]:
            return HTTPResponse.error(message="Could not get base data")
        return HTTPResponse.success(message=service_response["message"], result=service_response["data"])
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

def get_extracted_files_list():
    try:
        req_body = flask.request.get_json()
        report_date = req_body.get("report_date")
        company_id = req_body.get("company_id")
        extracted_base_data_status_id = req_body.get("extracted_base_data_status_id")
        service_response = diService.get_extracted_files_list(report_date, company_id, extracted_base_data_status_id)
        if not service_response["success"]:
            return HTTPResponse.error(message="Could not get extracted files list")
        return HTTPResponse.success(message=service_response.get("message"), result=service_response["data"])
    except Exception as e:
        Log.func_error(e)
        return HTTPResponse.error(message="Internal Server Error", status_code=500)