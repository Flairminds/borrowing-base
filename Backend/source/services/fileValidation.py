from flask import request, jsonify
from datetime import datetime, timedelta, date, timezone
import pickle
import json

from models import BaseDataFile, WhatIfAnalysis, db
from source.services import Standard_File_Formater
from Exceptions.StdFileFormatException import StdFileFormatException
from source.services.PCOF import utility as PCOFUtility


def validate_file():
    try:
        # Check if file is present in request
        if "file" not in request.files:
            return jsonify({"error": "No file part"})
        # Get the file
        excel_file = request.files["file"]
        closing_date = date.today()
        if request.form.get("closing_date"):
            closing_date = datetime.strptime(
                request.form.get("closing_date"), "%Y-%m-%d"
            ).date()

        fund_type = request.form.get("fund_type")

        base_data_file = BaseDataFile.query.filter_by(
            user_id=1, closing_date=closing_date, fund_type=fund_type
        ).first()

        over_write = False
        if request.form.get("over_write"):
            over_write = bool(int(request.form.get("over_write")))

        if base_data_file and base_data_file.fund_type == fund_type:
            if not over_write:
                return (
                    jsonify(
                        {
                            "error": True,
                            "message": "This file already exists in the system. Do you want to replace it? You might lose what if analysis data.",
                        }
                    ),
                    403,
                )

        if fund_type == "PCOF":
            error_map, xl_sheet_df_map = Standard_File_Formater.validate_file(
                excel_file, fund_type
            )
            error_map["Row Modifications"] = []
            # if Cash asset is not in dataframe
            if "PL BB Build" in xl_sheet_df_map.keys():
                df_PL_BB_Build = xl_sheet_df_map["PL BB Build"]

                if "Cash" not in df_PL_BB_Build["Investment Name"].tolist():
                    error_map["Row Modifications"].append(
                        "<b>Cash</b> asset is not present in <b>PL BB Build</b> sheet"
                    )

            if (
                (error_map["Sheet Modifications"])
                or (error_map["Column Modifications"])
                or (error_map["Data Format Modifications"])
                or error_map["Row Modifications"]
            ):
                raise StdFileFormatException(error_map)

            pickled_xl_sheet_df_map = pickle.dumps(xl_sheet_df_map)
            # save file data to database

            if base_data_file:
                included_excluded_assets_map = (
                    PCOFUtility.get_included_excluded_assets_map_json(
                        xl_sheet_df_map["PL BB Build"]
                    )
                )
                # over_write = False
                # if request.form.get('over_write'):
                #     over_write = bool(int(request.form.get('over_write')))

                # if over_write:
                # update existing base_data_file
                base_data_file.file_data = pickled_xl_sheet_df_map
                base_data_file.file_name = excel_file.filename
                base_data_file.updated_at = datetime.now(timezone.utc)
                base_data_file.included_excluded_assets_map = (
                    included_excluded_assets_map
                )

                # delete
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
                        return (
                            jsonify(
                                {"error": True, "message": "Could not update file."}
                            ),
                            500,
                        )
                # db.session.add(base_data_file)
                db.session.commit()
                db.session.refresh(base_data_file)

                return jsonify(
                    {
                        "error": False,
                        "id": base_data_file.id,
                        "user_id": base_data_file.user_id,
                        "file_name": base_data_file.file_name,
                    }
                )
            else:
                df_PL_BB_Build = xl_sheet_df_map["PL BB Build"]
                include_exclude_map_json = (
                    PCOFUtility.get_included_excluded_assets_map_json(df_PL_BB_Build)
                )

                base_data_file = BaseDataFile(
                    user_id=1,
                    file_name=excel_file.filename,
                    closing_date=closing_date,
                    file_data=pickled_xl_sheet_df_map,
                    included_excluded_assets_map=include_exclude_map_json,
                    fund_type=fund_type,
                )

                db.session.add(base_data_file)
                db.session.commit()
                db.session.refresh(base_data_file)

                return jsonify(
                    {
                        "error": False,
                        "id": base_data_file.id,
                        "user_id": base_data_file.user_id,
                        "file_name": base_data_file.file_name,
                    }
                )
        elif fund_type == "PFLT":

            error_map, xl_sheet_df_map = Standard_File_Formater.validate_file(
                excel_file, fund_type
            )
            error_map["Row Modifications"] = []

            if (
                (error_map["Sheet Modifications"])
                or (error_map["Column Modifications"])
                or (error_map["Data Format Modifications"])
                or error_map["Row Modifications"]
            ):
                raise StdFileFormatException(error_map)

            # xl_sheet_df_map = pd.read_excel(excel_file, sheet_name=None)
            pickled_xl_sheet_df_map = pickle.dumps(xl_sheet_df_map)
            # include_exclude_map_json = """{"included_assets":[]}"""
            include_exclude_map = {
                "included_assets": xl_sheet_df_map["Loan List"][
                    "Obligor Name"
                ].tolist(),
                "excluded_assets": [],
            }
            include_exclude_map_json = json.dumps(include_exclude_map)

            base_data_file = BaseDataFile(
                user_id=1,
                file_name=excel_file.filename,
                closing_date=closing_date,
                file_data=pickled_xl_sheet_df_map,
                included_excluded_assets_map=include_exclude_map_json,
                fund_type=fund_type,
            )

            db.session.add(base_data_file)
            db.session.commit()
            db.session.refresh(base_data_file)

            return jsonify(
                {
                    "error": False,
                    "id": base_data_file.id,
                    "user_id": base_data_file.user_id,
                    "file_name": base_data_file.file_name,
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
