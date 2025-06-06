from flask import request, jsonify

from source.services.WIA import wiaService, assetInventory
from source.services.commons import commonServices
from source.services.PCOF.WIA import addAssetAnalyst as pcofAddAssetAnalyst
from source.services.PFLT.WIA import addAssetAnalyst as pfltAddAssetAnalyst
from source.services.PCOF.WIA import updateParameterAnalyst as pcofUpdateParameterAnalyst
from source.services.PFLT.WIA import updateParameterAnalyst as pfltUpdateParameterAnalyst
from source.services.PCOF.WIA.updateAssetAnalyst import UpdateAssetAnalyst as pcofUpdateAssetAnalyst
from source.services.PFLT.WIA.updateAssetAnalyst import UpdateAssetAnalyst as pfltUpdateAssetAnalyst
from source.services.PSSL.WIA.updateAssetAnalyst import UpdateAssetAnalyst as psslUpdateAssetAnalyst
from source.services.PCOF.standardFileFormat import add_asset_std_file_format as PCOF_STANDARD_FILE_FORMAT
from source.services.PFLT.PFLT_std_file_format import add_asset_std_file_format as PFLT_STANDARD_FILE_FORMAT
from source.services.Standard_File_Formater import validate_file as add_asset_validate_file
from source.utility.HTTPResponse import HTTPResponse
from source.utility.Log import Log
from flask_sqlalchemy import SQLAlchemy

import modified_dfs_calculation

def add_additional_columns(get_parameter_res, type):
    if type == "Ebitda":
        opposite_type = "Leverage"
    if type == "Leverage":
        opposite_type = "Ebitda"
        
    columns = get_parameter_res["data"]["columns"]
    additional_columns = [{"key": "percent", "label": f"Additive {type} change %"}, {"key": "updated_ebitda", "label": "Updated Ebitda"}, {"key": "updated_leverage", "label": "Updated Leverage"}]
    updated_columns = []
    
    for column in columns:
        if column["label"] != opposite_type:
            updated_columns.append(column)
    
    columns = updated_columns
    columns = columns + additional_columns
    get_parameter_res["data"]["columns"] = columns
    return get_parameter_res

def get_asset_overview():
    try:
        if "file" not in request.files:
            return HTTPResponse.error(message="No file part", status_code=400)
        
        excelfile = request.files["file"]
        fund_type = request.form["fund_type"]

        if fund_type == "PCOF":
            std_file_format = PCOF_STANDARD_FILE_FORMAT
        else:
            std_file_format = PFLT_STANDARD_FILE_FORMAT

        # Validate sheet name and Column name 
        error_map, _ = add_asset_validate_file(excelfile, std_file_format)

        if (
            (error_map["Sheet Modifications"])
            or (error_map["Column Modifications"])
            or (error_map["Data Format Modifications"])
            or error_map["Row Modifications"]
        ):
            return HTTPResponse.error(message="File format error", result=error_map, status_code=400)

        selected_assets = wiaService.get_asset_overview(excelfile)
        return jsonify(selected_assets)

    except Exception as e:
        return HTTPResponse.error(message="Internal server error")


def add_assets():
    try:
        data = request.get_json()
        base_data_file_id = data.get("base_data_file_id")
        selected_assets = data.get("selected_assets")

        base_data_file = commonServices.get_base_data_file(
            base_data_file_id=base_data_file_id
        )

        fund_type = base_data_file.fund_type

        errors = wiaService.validate_selected_assets(selected_assets, fund_type)
        if len(errors) > 0:
            return HTTPResponse.error(result=errors)

        if fund_type == "PCOF":
            return pcofAddAssetAnalyst.add_asset(base_data_file, selected_assets)
        else:
            return pfltAddAssetAnalyst.add_asset(base_data_file, selected_assets)
        
    except Exception as e:
       Log.func_error(e)
       return HTTPResponse.error(message="Internal Server Error")


def get_parameters():
    try:
        data = request.get_json()
        base_data_file_id = data.get("base_data_file_id")
        type = data.get("type")

        base_data_file = commonServices.get_base_data_file(
            base_data_file_id=base_data_file_id
        )
        if base_data_file.fund_type == "PCOF":
            get_parameter_res = pcofUpdateParameterAnalyst.get_parameters(base_data_file, type)
        else:
            get_parameter_res = pfltUpdateParameterAnalyst.get_parameters(base_data_file, type)
        
        if get_parameter_res["success"] is False:
            return HTTPResponse.error(message=get_parameter_res["message"], status_code=get_parameter_res["status_code"])
        
        get_parameter_res  = add_additional_columns(get_parameter_res, type)
        return HTTPResponse.success(message=get_parameter_res.get("message"), result=get_parameter_res["data"])

    except Exception as e:
        Log.func_error(e)
        return HTTPResponse.error(message="Internal server error")

def update_parameters():
    try:
        data = request.get_json()
        base_data_file_id = data.get("base_data_file_id")
        type = data.get("type")
        asset_percent_list = data.get("asset_percent_list")


        base_data_file = commonServices.get_base_data_file(
            base_data_file_id=base_data_file_id
        )
        if base_data_file.fund_type == "PCOF":
            return jsonify(pcofUpdateParameterAnalyst.update_parameters(base_data_file, type, asset_percent_list)), 200
        else:
            return jsonify(pfltUpdateParameterAnalyst.update_parameters(base_data_file, type, asset_percent_list)), 200
    except Exception as e:
        return {
            "error": str(e),
            "error_status": True,
        }, 500
    
def save_analysis():
    try:
        data = request.get_json()
        what_if_analysis_id = data.get("what_if_analysis_id")
        analysis_type = data.get("analysis_type")
        simulation_name = data.get("simulation_name")
        note = data.get("note")

        save_analysis_res = wiaService.save_analysis(what_if_analysis_id, analysis_type, simulation_name, note)
        if save_analysis_res["success"] is False:
            return HTTPResponse.error(message=save_analysis_res["message"], status_code=save_analysis_res["status_code"])
        
        return HTTPResponse.success(message=save_analysis_res.get("message"), result=save_analysis_res["data"])
    except Exception as e:
        Log.func_error(e)
        return HTTPResponse.error(message="Internal server error")
    

def wia_library():
    try:
        data = request.get_json()
        user_id = data["user_id"]

        if not user_id:
            return HTTPResponse.error(message="User ID is required", status_code=400)
        
        wia_library_service_result = wiaService.wia_library(user_id)

        response = {
            "columns": [
                {"key":"name", "label": "Name"},
                {"key":"simulation_type", "label": "Simulation Type"},
                {"key":"note", "label": "Note"},
                {"key":"base_file_name", "label": "Base File Name"},
                {"key":"created_date", "label": "Created Date"},
                {"key":"fund_type", "label": "Fund Type"},
                ],
            "data": wia_library_service_result["data"]
        }

        return HTTPResponse.success(message=wia_library_service_result.get("message"), result=response)

    except Exception as e:
        return HTTPResponse.error(message="Internal Server Error")
    
def get_asset_inventry():
    try:
        data = request.get_json()
        what_if_analysis_id = data["what_if_analysis_id"]
        what_if_analysis_type = data["what_if_analysis_type"]

        fund_type = commonServices.get_fundType_of_wia(what_if_analysis_id, what_if_analysis_type)
        if not fund_type["success"]:
            return HTTPResponse.error(status_code= 404, message=fund_type["message"]  )
        
        fund_type=fund_type["data"]

        asset_inventry = assetInventory.get_asset_inventry(what_if_analysis_id, what_if_analysis_type, fund_type)
        
        return HTTPResponse.success(message="What if analysis inventory data fetched successfully", result=asset_inventry["data"])

    except Exception as e:
        return HTTPResponse.error(message="Internal server error")
    

def get_base_data_file_sheet_data():
    try:
        data = request.get_json()

        request_validation_result = wiaService.validate_get_sheet_data_request(data)
        if request_validation_result:
            return HTTPResponse.error(message=request_validation_result, status_code=400)

        response_data = wiaService.get_file_data(data)
        table_dict, changes = response_data["data"]["table_dict"], response_data["data"]["changes"]

        return HTTPResponse.success(
            result={"table_data": table_dict, "changes": changes}
        )

    except Exception as e:
        return HTTPResponse.error(message="Internal Server Error")
    
def update_values_in_sheet():
    try:
        data = request.get_json()

        request_validation_status = wiaService.validate_update_value_request(data)
        if request_validation_status is not None and not request_validation_status.get("success"):
            return HTTPResponse.error(message=request_validation_status["message"], status_code=400)

        updated_df, initial_df = wiaService.update_add_df(data)

        response_data = wiaService.save_updated_df(data, updated_df, initial_df)
        if not response_data["success"]:
            return HTTPResponse.error(message="Internal Server Error")
        
        return HTTPResponse.success(result={
            "modified_base_data_file_id": response_data["data"]["modified_base_data_file_id"]
        })
    except Exception as e:
        return HTTPResponse.error(message="Internal Server Error")
    

def calculate_bb_modified_sheets():
    request_data = request.get_json()
    try:
        service_response = commonServices.validate_request_data(request_data)
        if not service_response["success"]:
            return HTTPResponse.error(message = service_response["message"], status_code = 400)
        
        modified_base_data_file = service_response["data"]
        base_data_file = commonServices.get_base_data_file(base_data_file_id=modified_base_data_file.base_data_file_id)

        match base_data_file.fund_type:
            case "PCOF":
                response_data = pcofUpdateAssetAnalyst.update_assset(base_data_file, modified_base_data_file)
                update_asset_response = response_data["data"]
            case "PFLT":
                response_data = pfltUpdateAssetAnalyst.update_assset(base_data_file, modified_base_data_file)
                update_asset_response = response_data["data"]
            case "PSSL":
                response_data = psslUpdateAssetAnalyst.update_assset(base_data_file, modified_base_data_file)
                update_asset_response = response_data["data"]

        update_asset_response["what_if_analysis_id"] = request_data.get("modified_base_data_file_id")
        update_asset_response["what_if_analysis_type"] = "Update asset"

        return HTTPResponse.success(result = update_asset_response, message = "Successfully processed.")

    except Exception as e:
        return HTTPResponse.error(message = "Internal Server Error")


def select_what_if_analysis():
    try:
        request_data = request.get_json()
        what_if_analysis_id = request_data.get('what_if_analysis_id')
        simulation_type = request_data.get('simulation_type')
        what_if_analysis_res = wiaService.select_what_if_analysis(what_if_analysis_id, simulation_type)
        return what_if_analysis_res
    except Exception as e:
        print(e)
        return (
            jsonify(
                {
                    "error": str(e),
                    "error_type": str(type(e).__name__),
                    "error_file_details": f"error on line {e.__traceback__.tb_lineno} inside {__file__}",
                }
            ),
            500,
        )