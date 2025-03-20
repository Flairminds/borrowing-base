import traceback
class Log:

    @staticmethod
    def func_success(result = [], message = "Successfully processed."):
        print({
            "error": False,
            "result": result,
            "message": message
        })

    @staticmethod
    def func_error(e):
        print("Error: True")
        # print(e)
        traceback.print_exc()
        # print("bell", traceback.print_stack(), "bell2")
        # print({
        #     "error": True,
        #     "error_msg": str(e)[:150],
        #     "error_type": str(type(e).__name__),
        #     "error_file_details": f"error on line {e.__traceback__.tb_lineno} inside {__file__}",
        # })