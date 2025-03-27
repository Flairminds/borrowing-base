class ServiceResponse:

    @staticmethod
    def success(data = [], message = ""):
        return {
            "success": True,
            "message": message,
            "data": data
        }

    @staticmethod
    def error(message = "Error encountered.", status_code = 500, error_code = 'ERR_001', data = []):
        return {
            "success": False,
            "error_code": 'ERR_' + str(status_code),
            "data": data,
            "message": message,
            "status_code": status_code
        }
    
    @staticmethod
    def info(success=True ,data = [], message = "",):
        return {
            "success": success,
            "message": message,
            "data": data
        }