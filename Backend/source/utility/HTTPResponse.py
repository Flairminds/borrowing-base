class HTTPResponse:

    ERROR_CODES = {
        "VALIDATION_FAILED": "ERR_400",
        "SERVER_ERROR": "ERR_500",
    }

    @staticmethod
    def success(result = [], message = "Successfully processed."):
        return {
            "success": True,
            "result": result,
            "message": message
        }, 200

    @staticmethod
    def error(message = "Error encountered.", status_code = 500, error_code = 'ERR_001', result = [], error='SERVER_ERROR'):
        return {
            "success": False,
            "error_code": HTTPResponse.ERROR_CODES[error],
            "result": result,
            "message": message
        }, status_code