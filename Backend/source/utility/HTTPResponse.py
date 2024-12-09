class HTTPResponse:

    @staticmethod
    def success(result = [], message = "Successfully processed."):
        return {
            "success": True,
            "result": result,
            "message": message
        }, 200

    @staticmethod
    def error(message = "Error encountered.", status_code = 500, error_code = 'ERR_001', result = []):
        return {
            "success": False,
            "error_code": 'ERR_' + str(status_code),
            "result": result,
            "message": message
        }, status_code