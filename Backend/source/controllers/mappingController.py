import flask

from source.utility.Log import Log
from source.utility.HTTPResponse import HTTPResponse

from source.services.mappingServices import LoanTypeMappingService
from source.services.mappingServices import LienTypeMappingService

def get_loan_type_data(fund_name):
    try:
        response_data = {}
        unmapped_sr = LoanTypeMappingService.get_unmapped_loan_types(fund_name)
        if unmapped_sr["success"] is False:
            return HTTPResponse.error(message='Could not get Unmapped Loan Types', status_code=unmapped_sr["status_code"], result=unmapped_sr.get('data'))
        
        mapped_sr = LoanTypeMappingService.get_mapped_loan_types(fund_name)
        if mapped_sr["success"] is False:
            return HTTPResponse.error(message='Could not get Mapped Loan Types', status_code=mapped_sr["status_code"], result=mapped_sr.get('data'))
        
        master_sr = LoanTypeMappingService.get_master_loan_types(fund_name)
        if master_sr["success"] is False:
            return HTTPResponse.error(message='Could not get Master Loan Types', status_code=mapped_sr["status_code"], result=mapped_sr.get('data'))

        response_data['unmapped_loan_types'] = unmapped_sr['data']
        response_data['mapped_loan_types'] = mapped_sr['data']
        response_data['master_loan_types'] = master_sr['data']
        
        return HTTPResponse.success(message='Loan Type data', result=response_data)
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

def get_lien_type_data(fund_name):
    try:
        response_data = {}
        unmapped_sr = LienTypeMappingService.get_unmapped_lien_types(fund_name)
        if unmapped_sr["success"] is False:
            return HTTPResponse.error(message='Could not get Unmapped Lien Types', status_code=unmapped_sr["status_code"], result=unmapped_sr.get('data'))
        
        mapped_sr = LienTypeMappingService.get_mapped_lien_types(fund_name)
        if mapped_sr["success"] is False:
            return HTTPResponse.error(message='Could not get Mapped Lien Types', status_code=mapped_sr["status_code"], result=mapped_sr.get('data'))
        
        master_sr = LienTypeMappingService.get_master_lien_types(fund_name)
        if master_sr["success"] is False:
            return HTTPResponse.error(message='Could not get Master Lien Types', status_code=mapped_sr["status_code"], result=mapped_sr.get('data'))

        response_data['unmapped_lien_types'] = unmapped_sr['data']
        response_data['mapped_lien_types'] = mapped_sr['data']
        response_data['master_lien_types'] = master_sr['data']
        
        return HTTPResponse.success(message='Lien Type data', result=response_data)
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

def add_loan_type_master():
    try:
        req_body = flask.request.get_json()
        master_loan_type = req_body.get("master_loan_type")
        fund_type = req_body.get("fund_type")
        discription = req_body.get("description")
        
        service_response = LoanTypeMappingService.add_loan_type_master(fund_type, master_loan_type, discription)
        if service_response["success"] is False:
            return HTTPResponse.error(message=service_response["message"], status_code=service_response["status_code"])
        
        return HTTPResponse.success(message=service_response["message"], result=service_response.get('data'))
    except Exception as e:
        Log.func_error(e)
        return HTTPResponse.error(message="Internal server error", error_code=500)

def add_lien_type_master():
    try:
        req_body = flask.request.get_json()
        master_lien_type = req_body.get("master_lien_type")
        fund_type = req_body.get("fund_type")
        discription = req_body.get("description")
        
        service_response = LienTypeMappingService.add_loan_type_master(fund_type, master_lien_type, discription)
        if service_response["success"] is False:
            return HTTPResponse.error(message=service_response["message"], status_code=service_response["status_code"])
        
        return HTTPResponse.success(message=service_response["message"], result=service_response.get('data'))
    except Exception as e:
        Log.func_error(e)
        return HTTPResponse.error(message="Internal server error", error_code=500)

def delete_loan_type_mapping():
    try:
        req_body = flask.request.get_json()
        mapping_id = req_body.get("mapping_id")
        
        service_response = LoanTypeMappingService.delete_mapping(mapping_id)
        if service_response["success"] is False:
            return HTTPResponse.error(message=service_response["message"], status_code=service_response["status_code"])
        
        return HTTPResponse.success(message=service_response["message"], result=service_response.get('data'))
    except Exception as e:
        Log.func_error(e)
        return HTTPResponse.error(message="Internal server error", error_code=500)
    
def delete_lien_type_mapping():
    try:
        req_body = flask.request.get_json()
        mapping_id = req_body.get("mapping_id")
        
        service_response = LienTypeMappingService.delete_mapping(mapping_id)
        if service_response["success"] is False:
            return HTTPResponse.error(message=service_response["message"], status_code=service_response["status_code"])
        
        return HTTPResponse.success(message=service_response["message"], result=service_response.get('data'))
    except Exception as e:
        Log.func_error(e)
        return HTTPResponse.error(message="Internal server error", error_code=500)