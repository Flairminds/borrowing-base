from flask import request

from source.services import fundSetupService
from source.utility.HTTPResponse import HTTPResponse
from source.utility.Log import Log


def get_concentration_tests():
    try:
        req_body = request.get_json()
        fund_name = req_body.get("fund_name")
        return fundSetupService.get_concentration_tests(fund_name)
    except Exception as e:
        return {
            "error": str(e),
            "error_type": str(type(e).__name__),
            "error_file_details": f"error on line {e.__traceback__.tb_lineno} inside {__file__}",
        }, 500


def update_limit():
    try:
        req_body = request.get_json()
        test_changes = req_body["changes"]
        upd_limit_res = fundSetupService.update_limit(test_changes)
        if upd_limit_res["success"] is False:
            return HTTPResponse.error(message=upd_limit_res["message"], status_code=upd_limit_res["status_code"])

        base_data_files = fundSetupService.get_base_files(user_id=1)
        fundSetupService.recalculate_bb(base_data_files, upd_limit_res["data"])
        return HTTPResponse.success(message=upd_limit_res["message"])
    except Exception as e:
        Log.func_error(e)
        return HTTPResponse.error(message="Internal server error")