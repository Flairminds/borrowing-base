from flask import jsonify
import pickle
from datetime import date, datetime, timezone
import json

from models import db, BaseDataFile, WhatIfAnalysis
from Exceptions.StdFileFormatException import StdFileFormatException
from source.services.PCOF import utility as PCOFUtility
from source.services.PCOF.PcofDashboardService import PcofDashboardService
from source.services.PFLT.PfltDashboardService import PfltDashboardService
from source.utility.ServiceResponse import ServiceResponse

pcofDashboardService = PcofDashboardService()
pfltDashboardService = PfltDashboardService()


def validate_file(excel_file, closing_date, fund_type, over_write):
    try:
        if not excel_file:
            return jsonify({"error": "No file part"})

        if not closing_date:
            closing_date = date.today()

        base_data_file = BaseDataFile.query.filter_by(
            user_id=1, closing_date=closing_date, fund_type=fund_type
        ).first()

        if base_data_file and base_data_file.fund_type == fund_type:
            if bool(int(over_write)) == False:
                return True, base_data_file
            else:
                return False, base_data_file
        else:
            return False, base_data_file

    except StdFileFormatException as ffe:
        return ServiceResponse.error(
            message = ffe.error_map, 
            status_code = 400,
        )
    
    except Exception as e:
        return ServiceResponse.error(
            message = str(e), 
            status_code = 500, 
            data = f"error on line {e.__traceback__.tb_lineno} inside {__file__}"
        )


def latest_closing_date(user_id):
    user_id = int(user_id)
    latest_data = (
        BaseDataFile.query.filter(
            BaseDataFile.user_id == user_id,
            BaseDataFile.response != None,
        )
        .order_by(BaseDataFile.closing_date.desc())
        .first()
    )
    if latest_data:
        data = pickle.loads(latest_data.response)
    else:
        return jsonify({"message": "Previous data does not exist"}), 404
    data["closing_date"] = latest_data.closing_date.strftime("%Y-%m-%d")
    data["base_data_file_id"] = latest_data.id
    data["file_name"] = latest_data.file_name
    data["fund_name"] = latest_data.fund_type

    base_data_files = BaseDataFile.query.filter_by(user_id=user_id).all()
    closing_dates = [
        base_data_file.closing_date.strftime("%Y-%m-%d")
        for base_data_file in base_data_files
    ]
    data["closing_dates"] = closing_dates

    base_data_files = BaseDataFile.query.filter(
        BaseDataFile.user_id == user_id, BaseDataFile.response != None
    ).all()
    closing_dates = [
        base_data_file.closing_date.strftime("%Y-%m-%d")
        for base_data_file in base_data_files
    ]
    data["closing_dates"] = closing_dates
    return jsonify(data), 200


def get_files_list(user_id):
    base_data_files = (
        BaseDataFile.query.filter_by(user_id=user_id)
        .order_by(BaseDataFile.closing_date.desc())
        .all()
    )
    # If no data found for the user_id, return an error response
    if not base_data_files:
        return (
            jsonify({"error": True, "message": "No data found for the user_id"}),
            404,
        )
    # Extract file names from the retrieved data
    file_names = [
        {
            "user_id": file.user_id,
            "file_name": file.file_name,
            "base_data_file_id": file.id,
            "closing_date": file.closing_date.strftime("%Y-%m-%d"),
            "fund_type": file.fund_type,
            "extracted_base_data_info_id": file.extracted_base_data_info_id
        }
        for file in base_data_files
    ]

    return jsonify({"error_status": False, "files_list": file_names}), 200


def get_bb_data_of_date(selected_date, user_id, base_data_file_id):
    if base_data_file_id:
        borrowing_base_results = BaseDataFile.query.filter_by(id=base_data_file_id).first()
    else:
        borrowing_base_results = BaseDataFile.query.filter_by(user_id=user_id, closing_date=selected_date).first()

    if not borrowing_base_results:
        return (
            jsonify(
                {
                    "error": True,
                    "message": f"File is not uploaded on {selected_date}",
                }
            ),
            404,
        )

    # If no response found for selected date base_data_file
    if not borrowing_base_results.response:
        return (
            jsonify({"error": True, "message": f"No data found for {selected_date}"}),
            404,
        )
    
    base_data_files = BaseDataFile.query.filter_by(user_id=user_id).all()
    closing_dates = [
        base_data_file.closing_date.strftime("%Y-%m-%d")
        for base_data_file in base_data_files
    ]

    pickle_borrowing_base_date_wise_results = borrowing_base_results.response
    borrowing_base_date_wise_results = pickle.loads(
        pickle_borrowing_base_date_wise_results
    )
    borrowing_base_date_wise_results["base_data_file_id"] = borrowing_base_results.id
    borrowing_base_date_wise_results["file_name"] = borrowing_base_results.file_name
    borrowing_base_date_wise_results["fund_name"] = borrowing_base_results.fund_type
    borrowing_base_date_wise_results["closing_date"] = borrowing_base_results.closing_date.strftime("%Y-%m-%d")
    borrowing_base_date_wise_results["closing_dates"] = closing_dates
    return jsonify(borrowing_base_date_wise_results)


# def get_base_data_file(**kwargs):
#     if "base_data_file_id" in kwargs.keys():
#         base_data_file_id = kwargs["base_data_file_id"]
#         base_data_file = BaseDataFile.query.filter_by(id=base_data_file_id).first()
#     else:
#         user_id = kwargs["user_id"]
#         if "closing_date" not in kwargs.keys():
#             base_data_file = (
#                 BaseDataFile.query.filter_by(user_id=user_id)
#                 .order_by(BaseDataFile.closing_date.desc())
#                 .first()
#             )
#         else:
#             closing_date = kwargs["closing_date"]
#             base_data_file = BaseDataFile.query.filter_by(
#                 closing_date=closing_date, user_id=user_id
#             ).first()
#     return base_data_file


def get_sorted_base_data_closing_date(user_id, start_date, end_date, fund_type):
    if fund_type == "":
        latest_base_data_file = (
            BaseDataFile.query.filter(
                BaseDataFile.user_id == user_id, BaseDataFile.response != None
            )
            .order_by(BaseDataFile.closing_date.desc(), BaseDataFile.id.desc())
            .first()
        )
        fund_type = latest_base_data_file.fund_type
    if start_date and end_date:  # Check if both start_date and end_date are provided
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        base_data_file = BaseDataFile.query.filter(
            BaseDataFile.user_id == user_id,
            BaseDataFile.closing_date.between(start_date, end_date),
            BaseDataFile.response != None,
            BaseDataFile.fund_type == fund_type,
        ).all()
    else:
        base_data_file = BaseDataFile.query.filter(
            BaseDataFile.user_id == user_id,
            BaseDataFile.response != None,
            BaseDataFile.fund_type == fund_type,
        ).all()

    base_data_file_sorted = sorted(base_data_file, key=lambda x: x.closing_date)
    closing_date = [
        datetime.strftime(file.closing_date, "%Y-%m-%d")
        for file in base_data_file_sorted
    ]
    return base_data_file_sorted, closing_date, fund_type

def upload_file(excel_file, xl_sheet_df_map, closing_date, fund_type, included_excluded_assets_map):
    try:
        pickled_xl_sheet_df_map = pickle.dumps(xl_sheet_df_map)

        if fund_type == "PFLT":
            included_excluded_assets_map=json.dumps(included_excluded_assets_map)

        base_data_file = BaseDataFile(
            user_id=1,
            closing_date=closing_date,
            fund_type=fund_type,
            file_data=pickled_xl_sheet_df_map,
            file_name=excel_file.filename,
            included_excluded_assets_map=included_excluded_assets_map,
        )
        
        db.session.add(base_data_file)
        db.session.commit()
        return base_data_file
    
    except Exception as e:
        return ServiceResponse.error(message=f"An unexpected error occurred: {str(e)}")

def override_file(base_data_file, excel_file, xl_sheet_df_map, fund_type, included_excluded_assets_map):
    try:
        pickled_xl_sheet_df_map = pickle.dumps(xl_sheet_df_map)

        if fund_type == "PFLT":
            included_excluded_assets_map = json.dumps(
                included_excluded_assets_map
            )

        base_data_file.file_data = pickled_xl_sheet_df_map
        base_data_file.file_name = excel_file.filename
        base_data_file.updated_at = datetime.now(timezone.utc)
        base_data_file.included_excluded_assets_map = included_excluded_assets_map
        base_data_file.response = None
        base_data_file.intermediate_calculation = None

        what_if_analysis_list = WhatIfAnalysis.query.filter_by(
            base_data_file_id=base_data_file.id
        ).all()

        if what_if_analysis_list:
            WhatIfAnalysis.query.filter_by(
                base_data_file_id=base_data_file.id
            ).delete()
            
            what_if_analysis_list = WhatIfAnalysis.query.filter_by(
                base_data_file_id=base_data_file.id
            ).all()
            
            if what_if_analysis_list:
                return jsonify(
                    {"error": True, "message": "Could not update file."}
                ), 500
                
        db.session.commit()
        db.session.refresh(base_data_file)

        return base_data_file
    
    except Exception as e:
        return ServiceResponse.error(message=f"An unexpected error occurred: {str(e)}")

def get_closing_dates_list():
    user_id = 1
    base_data_files = BaseDataFile.query.filter_by(user_id=user_id).all()
    closing_dates = [base_data_file.closing_date.strftime("%Y-%m-%d") for base_data_file in base_data_files]
    return closing_dates