from datetime import datetime
from flask import jsonify, request
import json

from models import BaseDataFile, ModifiedBaseDataFile, WhatIfAnalysis
from source.utility.HTTPResponse import HTTPResponse
from source.services.commons import commonServices
from source.services import dashboardService
from source.services.PCOF.PcofDashboardService import PcofDashboardService
from source.services.PFLT.PfltDashboardService import PfltDashboardService
from source.services.PSSL.PsslDashboardService import PsslDashboardService
from Exceptions.StdFileFormatException import StdFileFormatException
from source.services.PCOF.standardFileFormat import std_file_format as PCOF_STANDARD_FILE_FORMAT
from source.services.PFLT.PFLT_std_file_format import std_file_format as PFLT_STANDARD_FILE_FORMAT
from source.utility.Log import Log

pcofDashboardService = PcofDashboardService()
pfltDashboardService = PfltDashboardService()
pssl_dashboard_service = PsslDashboardService()


def handle_upload_fund_file():
    try:
        excel_file = request.files.get("file")
        closing_date = datetime.strptime(
            request.form.get("closing_date"), "%Y-%m-%d"
        ).date()
        fund_type = request.form.get("fund_type")
        over_write = request.form.get("over_write")
        
        isExist, base_data_file = dashboardService.validate_file(
            excel_file, closing_date, fund_type, over_write
        )

        if(isExist):
            return HTTPResponse.error(
                message="This file already exists in the system. Do you want to replace it? You might lose what if analysis data.",
                status_code=409
            )

        xl_sheet_df_map = None
        included_excluded_assets_map = None
        
        if fund_type == "PCOF":
            std_file_format = PCOF_STANDARD_FILE_FORMAT
            xl_sheet_df_map =  pcofDashboardService.validate_standard_file_format(excel_file, std_file_format)
            included_excluded_assets_map = pcofDashboardService.pcof_included_excluded_assets(xl_sheet_df_map)

        if fund_type == "PFLT":
            std_file_format = PFLT_STANDARD_FILE_FORMAT
            xl_sheet_df_map = pfltDashboardService.validate_standard_file_format(excel_file, std_file_format)
            included_excluded_assets_map = pfltDashboardService.pflt_included_excluded_assets(xl_sheet_df_map)

        if bool(int(over_write)) == False:
            base_data_file = dashboardService.upload_file(excel_file, xl_sheet_df_map, closing_date, fund_type, included_excluded_assets_map)
        else:
            base_data_file = dashboardService.override_file(base_data_file, excel_file, xl_sheet_df_map, fund_type, included_excluded_assets_map)

        return HTTPResponse.success(
            result={
                "id": base_data_file.id,
                "user_id": base_data_file.user_id,
                "file_name": base_data_file.file_name
            }
        )
    
    except StdFileFormatException as ffe:
        return (
            jsonify(
                {
                    "error": True,
                    "error_type": "File Format Error",
                    "error_message": ffe.error_map,
                }
            ),
            400,
        )
    except Exception as e:
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

def get_card_overview_data():
    try:
        data = request.get_json()
        base_data_file_id = data.get("base_data_file_id")
        card_name = data["card_name"]
        user_id = data.get("user_id")
        what_if_analysis_id = data.get("what_if_analysis_id")
        what_if_analysis_type = data.get("what_if_analysis_type")

        base_data_file = commonServices.get_base_data_file(
            base_data_file_id=base_data_file_id, user_id=user_id
        )
        what_if_analysis = None
        if what_if_analysis_id and what_if_analysis_type:
            if what_if_analysis_type == "Update asset":
                what_if_analysis = ModifiedBaseDataFile.query.filter_by(id=what_if_analysis_id).first()
                base_data_file = BaseDataFile.query.filter_by(id=what_if_analysis.base_data_file_id).first()
            else:
                what_if_analysis = WhatIfAnalysis.query.filter_by(id=what_if_analysis_id).first()
                base_data_file = BaseDataFile.query.filter_by(id=what_if_analysis.base_data_file_id).first()
        if base_data_file.fund_type == "PCOF":
            card_overview_response = pcofDashboardService.get_card_overview(
                base_data_file, card_name, what_if_analysis
            )
        if base_data_file.fund_type == "PFLT":
            pfltDashbardService = PfltDashboardService()
            card_overview_response = pfltDashbardService.get_card_overview(
                base_data_file, card_name, what_if_analysis
            )
        if base_data_file.fund_type == "PSSL":
            psslDashbardService = PsslDashboardService()
            card_overview_response = psslDashbardService.get_card_overview(
                base_data_file, card_name, what_if_analysis
            )

        return card_overview_response
    except Exception as e:
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


def get_assets_list():
    try:
        data = request.get_json()
        base_data_file_id = data.get("base_data_file_id")
        base_data_file = commonServices.get_base_data_file(
            base_data_file_id=base_data_file_id
        )
        if base_data_file.fund_type == "PCOF":
            return pcofDashboardService.get_asset_list(base_data_file)
        else:
            return pfltDashboardService.get_asset_list(base_data_file)
    except Exception as e:
        return {
            "error": str(e),
            "error_type": str(type(e).__name__),
            "error_file_details": f"error on line {e.__traceback__.tb_lineno} inside {__file__}",
        }, 500


def latest_closing_date():
    try:
        user_id = request.form["user_id"]
        return dashboardService.latest_closing_date(user_id)
    except Exception as e:
        return {
            "error": str(e),
            "error_type": str(type(e).__name__),
            "error_file_details": f"error on line {e.__traceback__.tb_lineno} inside {__file__}",
        }, 500


def get_files_list():
    try:
        data = request.get_json()
        user_id = data["user_id"]
        return dashboardService.get_files_list(user_id)
    except Exception as e:
        return {
            "error": str(e),
            "error_type": str(type(e).__name__),
            "error_file_details": f"error on line {e.__traceback__.tb_lineno} inside {__file__}",
        }, 500


def get_bb_data_of_date():
    try:
        data = request.get_json()
        selected_date = data.get("closing_date")
        fund_type = data.get("fund_type")
        user_id = data.get("user_id")
        base_data_file_id = data.get("base_data_file_id")
        return dashboardService.get_bb_data_of_date(selected_date, user_id, base_data_file_id, fund_type)
    except Exception as e:
        return {
            "error": str(e),
            "error_type": str(type(e).__name__),
            "error_file_details": f"error on line {e.__traceback__.tb_lineno} inside {__file__}",
        }, 500


def get_trend_graph():
    try:
        user_id = int(request.form["user_id"])
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        fund_type = request.form.get("fund_type")

        base_data_file_sorted, closing_date, fund_type = (
            dashboardService.get_sorted_base_data_closing_date(
                user_id, start_date, end_date, fund_type
            )
        )

        # if fund_type == "PCOF":
        #     return pcofDashboardService.get_trend_graph(
        #         base_data_file_sorted, closing_date
        #     )
        # else:
        #     return pfltDashboardService.get_trend_graph(
        #         base_data_file_sorted, closing_date
        #     )
        
        match fund_type:
            case "PCOF": return pcofDashboardService.get_trend_graph(base_data_file_sorted, closing_date)
            case "PFLT": return pfltDashboardService.get_trend_graph(base_data_file_sorted, closing_date)
            case "PSSL": return pssl_dashboard_service.get_trend_graph(base_data_file_sorted, closing_date)

    except Exception as e:
        return {
            "error": str(e),
            "error_type": str(type(e).__name__),
            "error_file_details": f"error on line {e.__traceback__.tb_lineno} inside {__file__}",
        }, 500


def calculate_bb():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        base_data_file_id = data["base_data_file_id"]
        selected_assets = data.get("selected_assets")

        base_data_file = commonServices.get_base_data_file(
            base_data_file_id=base_data_file_id
        )

        base_data_files = BaseDataFile.query.filter_by(user_id=user_id).all()
        closing_dates = [
            base_data_file.closing_date.strftime("%Y-%m-%d")
            for base_data_file in base_data_files
        ]

        match base_data_file.fund_type:
            case 'PCOF': response = pcofDashboardService.calculate_bb(base_data_file, selected_assets, user_id)
            case 'PFLT': response = pfltDashboardService.calculate_bb(base_data_file, selected_assets, user_id)
            case 'PSSL': response = pssl_dashboard_service.get_bb_calculation(base_data_file, selected_assets, user_id)

        response["closing_dates"] = closing_dates

        return HTTPResponse.success(result=response)
    except Exception as e:
        Log.func_error(e)
        return HTTPResponse.error(message="Internal Server Error")

def get_intermediate_metrics():
    try:
        request_body = request.get_json()
        base_data_file_id = request_body.get("base_data_file_id")
        
        base_data_file = commonServices.get_base_data_file(base_data_file_id=base_data_file_id)

        if base_data_file.fund_type == "PCOF":
            service_response = pcofDashboardService.get_intermediate_metrics(base_data_file)
        else:
            service_response = pfltDashboardService.get_intermediate_metrics(base_data_file)

        return service_response
    except Exception as e:
        return HTTPResponse.error(message="Internal Server Error")

def get_mathematical_formula():
    try:
        request_body = request.get_json()
        user_id = request_body.get("user_id")
        base_data_file_id = request_body["base_data_file_id"]
        col_name = request_body["col_name"]
        row_name = request_body["row_name"]
        
        base_data_file = commonServices.get_base_data_file(base_data_file_id=base_data_file_id)

        if base_data_file.fund_type == "PCOF":
            service_response = pcofDashboardService.get_mathematical_formula(base_data_file, col_name, row_name)
        else:
            service_response = pfltDashboardService.get_mathematical_formula(base_data_file, col_name, row_name)

        return service_response
    except Exception as e:
        return HTTPResponse.error(message="Internal Server Error")
    
def download_calculated_df():
    request_body = request.get_json()
    base_data_file_id = request_body["base_data_file_id"]
    base_data_file = commonServices.get_base_data_file(base_data_file_id=base_data_file_id)
    return dashboardService.download_calculated_df(base_data_file)

def get_closing_dates():
    try: 
        data = json.loads(request.data)
        fund_type = data.get("fund_type")
        closing_dates = dashboardService.get_closing_dates_list(fund_type)
        return HTTPResponse.success(result=closing_dates)
    except Exception as e:
        return HTTPResponse.error(message="Internal Server Error")

def get_company_insights():
    data = json.loads(request.data)
    company_name = data.get("company_name")
    if not company_name:
        return HTTPResponse.error(message="Missing 'company_name' in request body.", status_code=400)
    try:
        result = dashboardService.get_company_insights(company_name)
        return HTTPResponse.success(result=result)
    except Exception as e:
        Log.func_error(e)
        return HTTPResponse.error(message="Internal Server Error")