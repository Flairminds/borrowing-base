import flask

from source.utility.Log import Log
from source.utility.HTTPResponse import HTTPResponse

from source.services.mappingServices import LoanTypeMappingService
from source.services.mappingServices import LienTypeMappingService

def get_loan_type_data():
    try:
        service_response = LoanTypeMappingService.get_loan_type_data()
        if service_response["success"] is False:
            return HTTPResponse.error(message=service_response["message"], status_code=service_response["status_code"], result=service_response.get('data'))
        
        return HTTPResponse.success(message=service_response["message"], result=service_response.get('data'))
    except Exception as e:
        Log.func_error(e)
        return HTTPResponse.error(message="Internal server error", error_code=500)

def map_loan_type():
    try:
        req_body = flask.request.get_json()
        mappings = req_body.get("mappings")
        
        service_response = LoanTypeMappingService.map_loan_type(mappings)
        if service_response["success"] is False:
            return HTTPResponse.error(message=service_response["message"], status_code=service_response["status_code"])
        
        return HTTPResponse.success(message=service_response["message"], result=service_response.get('data'))
    except Exception as e:
        Log.func_error(e)
        return HTTPResponse.error(message="Internal server error", error_code=500)

def get_lien_type_data():
    try:
        service_response = LienTypeMappingService.get_lien_type_data()
        if service_response["success"] is False:
            return HTTPResponse.error(message=service_response["message"], status_code=service_response["status_code"], result=service_response.get('data'))
        
        return HTTPResponse.success(message=service_response["message"], result=service_response.get('data'))
    except Exception as e:
        Log.func_error(e)
        return HTTPResponse.error(message="Internal server error", error_code=500)
    
def map_lien_type():
    try:
        req_body = flask.request.get_json()
        mappings = req_body.get("mappings")
        
        service_response = LienTypeMappingService.map_lien_type(mappings)
        if service_response["success"] is False:
            return HTTPResponse.error(message=service_response["message"], status_code=service_response["status_code"])
        
        return HTTPResponse.success(message=service_response["message"], result=service_response.get('data'))
    except Exception as e:
        Log.func_error(e)
        return HTTPResponse.error(message="Internal server error", error_code=500)