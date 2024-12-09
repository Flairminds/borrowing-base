from flask import (
    Flask,
    request,
    jsonify,
    render_template,
    send_from_directory,
    session,
    send_file,
    make_response,
)
import sys
import pathlib
import os

source_dir = pathlib.Path().absolute() / "source"
sys.path.append(str(source_dir))

from flask_cors import CORS
import pandas as pd
from pandas import ExcelWriter
import math
from functionsCall import *
from utility_functions import *
import pathlib
import numpy as np
import json
import locale
from flask_session import Session
from datetime import timedelta, date
import copy

# from std_file_formater import find_file_format_change, rename_columns#, rename_sheets
from source.services.Standard_File_Formater import validate_file
from Exceptions.StdFileFormatException import StdFileFormatException
from intermediate_metrics_formulas import formula_info
from response import *
from session_files import *
from concentration_test import (
    get_data_concentration_test,
    change_haircut_number,
    lock_concentration_test_data,
)
import os
from flask_migrate import Migrate
from models import *
from urllib.parse import quote_plus
import pickle
from dotenv import load_dotenv
from io import BytesIO
from numerize import numerize

# PFLT files import
from source.PFLT_Borrowing_Base.pflt_borrowing_base import PFLTBorrowingBase as PBC
import PFLT_Borrowing_Base.TrendGraphResponseGenerator as PFLTTrendGraphResponseGenerator


def landing_page_function():
    try:
        if request.method == "POST":
            user_id = int(request.form["user_id"])
            latest_data = (
                BaseDataFile.query.filter(
                    BaseDataFile.user_id == user_id,
                    BaseDataFile.response != None,
                    # BaseDataFile.fund_type == "PCOF",
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


def validate_function():
    try:
        if request.method == "POST":
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
                error_map, xl_sheet_df_map = validate_file(excel_file, fund_type)
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
                        get_included_excluded_assets_map_json(
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
                    include_exclude_map_json = get_included_excluded_assets_map_json(
                        df_PL_BB_Build
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

                error_map, xl_sheet_df_map = validate_file(excel_file, fund_type)
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


def calculate_function():
    if request.method == "POST":
        try:
            data = request.get_json()
            user_id = data.get("user_id")
            base_data_file_id = data["base_data_file_id"]
            selected_assets = data.get("selected_assets")

            # retrive sheet names and respective dataframe map from database
            base_data_file = BaseDataFile.query.filter_by(id=base_data_file_id).first()

            xl_sheet_df_map = pickle.loads(base_data_file.file_data)

            if base_data_file.fund_type == "PCOF":
                # Read data from Excel file
                (
                    df_PL_BB_Build,
                    df_Inputs_Other_Metrics,
                    df_Availability_Borrower,
                    df_PL_BB_Results,
                    df_subscriptionBB,
                    df_security,
                    df_industry,
                    df_Input_pricing,
                    df_Inputs_Portfolio_LeverageBorrowingBase,
                    df_Obligors_Net_Capital,
                    df_Inputs_Advance_Rates,
                    df_Inputs_Concentration_limit,
                    df_principle_obligations,
                ) = read_excels(xl_sheet_df_map)

                included_excluded_assets_list_map_json = (
                    get_included_excluded_assets_map_json(df_PL_BB_Build)
                )

                original_PL_BB_Build = df_PL_BB_Build.copy()
                selected_assets_mask = df_PL_BB_Build["Investment Name"].isin(
                    selected_assets
                )

                df_PL_BB_Build = df_PL_BB_Build[selected_assets_mask].reset_index(
                    drop=True
                )
                df_PL_BB_Build = df_PL_BB_Build[
                    df_PL_BB_Build["Is Eligible Issuer"] == "Yes"
                ]

                if "Cash" not in selected_assets:
                    cash_row = original_PL_BB_Build[
                        original_PL_BB_Build["Investment Name"] == "Cash"
                    ]
                    df_PL_BB_Build = pd.concat(
                        [df_PL_BB_Build, cash_row], ignore_index=True
                    )
                else:
                    cash_row = original_PL_BB_Build[
                        original_PL_BB_Build["Investment Name"] == "Cash"
                    ]
                    if cash_row["Is Eligible Issuer"].tolist()[0] == "No":
                        df_PL_BB_Build = pd.concat(
                            [df_PL_BB_Build, cash_row], ignore_index=True
                        )
                # Calculate the result files
                (
                    df_PL_BB_Build,
                    df_Inputs_Other_Metrics,
                    df_Availability_Borrower,
                    df_PL_BB_Results,
                    df_subscriptionBB,
                    df_security,
                    df_industry,
                    df_Input_pricing,
                    df_Inputs_Portfolio_LeverageBorrowingBase,
                    df_Obligors_Net_Capital,
                    df_Inputs_Advance_Rates,
                    df_Inputs_Concentration_limit,
                    df_principle_obligations,
                    df_segmentation_overview,
                    df_PL_BB_Output,
                ) = functions_call_calculation(
                    df_PL_BB_Build,
                    df_Inputs_Other_Metrics,
                    df_Availability_Borrower,
                    df_PL_BB_Results,
                    df_subscriptionBB,
                    df_security,
                    df_industry,
                    df_Input_pricing,
                    df_Inputs_Portfolio_LeverageBorrowingBase,
                    df_Obligors_Net_Capital,
                    df_Inputs_Advance_Rates,
                    df_Inputs_Concentration_limit,
                    df_principle_obligations,
                )
                # Save calculated files to Session
                save_calculated_files(
                    df_PL_BB_Build,
                    df_Inputs_Other_Metrics,
                    df_Availability_Borrower,
                    df_PL_BB_Results,
                    df_subscriptionBB,
                    df_security,
                    df_industry,
                    df_Input_pricing,
                    df_Inputs_Portfolio_LeverageBorrowingBase,
                    df_Obligors_Net_Capital,
                    df_Inputs_Advance_Rates,
                    df_Inputs_Concentration_limit,
                    df_principle_obligations,
                    df_segmentation_overview,
                    df_PL_BB_Output,
                )

                # Save calculated files to DB
                intermediate_calculation = {
                    "df_PL_BB_Build": df_PL_BB_Build,
                    "df_Inputs_Other_Metrics": df_Inputs_Other_Metrics,
                    "df_Availability_Borrower": df_Availability_Borrower,
                    "df_PL_BB_Results": df_PL_BB_Results,
                    "df_subscriptionBB": df_subscriptionBB,
                    "df_subscriptionBB": df_subscriptionBB,
                    "df_security": df_security,
                    "df_industry": df_industry,
                    "df_Input_pricing": df_Input_pricing,
                    "df_Inputs_Portfolio_LeverageBorrowingBase": df_Inputs_Portfolio_LeverageBorrowingBase,
                    "df_Obligors_Net_Capital": df_Obligors_Net_Capital,
                    "df_Inputs_Advance_Rates": df_Inputs_Advance_Rates,
                    "df_Inputs_Concentration_limit": df_Inputs_Concentration_limit,
                    "df_principle_obligations": df_principle_obligations,
                    "df_segmentation_overview": df_segmentation_overview,
                    "df_PL_BB_Output": df_PL_BB_Output,
                }

                pickled_intermediate_calculation = pickle.dumps(
                    intermediate_calculation
                )
                base_data_file.intermediate_calculation = (
                    pickled_intermediate_calculation
                )

                latest_data = (
                    BaseDataFile.query.filter(BaseDataFile.user_id == user_id)
                    .order_by(BaseDataFile.closing_date.desc())
                    .first()
                )
                closing_date = latest_data.closing_date.strftime("%Y-%m-%d")
                # generate response to send
                (
                    card_data,
                    segmentation_Overview_data,
                    security_data,
                    concentration_Test_data,
                    principal_obligation_data,
                    segmentation_chart_data,
                    security_chart_data,
                ) = formatted_data(
                    df_PL_BB_Results,
                    df_security,
                    df_segmentation_overview,
                    df_principle_obligations,
                    df_Availability_Borrower,
                )  # Construct response dictionary
                response_data = {
                    "card_data": card_data,
                    "segmentation_overview_data": segmentation_Overview_data,
                    "security_data": security_data,
                    "concentration_test_data": concentration_Test_data,
                    "principal_obligation_data": principal_obligation_data,
                    "segmentation_chart_data": segmentation_chart_data,
                    "security_chart_data": security_chart_data,
                    "closing_date": closing_date,
                }

                # upsert pickled_response_data
                pickled_response_data = pickle.dumps(response_data)
                base_data_file.response = pickled_response_data

                # update json_include_exclude_map
                included_excluded_assets_list_map = json.loads(
                    included_excluded_assets_list_map_json
                )
                all_assets_list = included_excluded_assets_list_map["included_assets"]

                excluded_assets = all_assets_list.copy()
                for included_asset in selected_assets:
                    if included_asset in all_assets_list:
                        excluded_assets.remove(included_asset)

                included_excluded_assets_map = {
                    "included_assets": selected_assets,
                    "excluded_assets": excluded_assets,
                }

                json_include_exclude_map = json.dumps(included_excluded_assets_map)
                base_data_file.included_excluded_assets_map = json_include_exclude_map
            elif (
                base_data_file.fund_type == "PFLT" or base_data_file.fund_type == "PLFT"
            ):
                PFLT_xl_sheet_df_map = copy.deepcopy(xl_sheet_df_map)
                pbc = PBC(file_df=PFLT_xl_sheet_df_map)
                pbc.calculate()

                # save into the session
                session["PFLT_file_df"] = pbc.file_df
                intermediate_calculation = pbc.file_df
                # intermediate_calculations
                # intermediate_calculation = {"random_calculation": "random_calculation"}
                pickled_intermediate_calculation = pickle.dumps(
                    intermediate_calculation
                )
                base_data_file.intermediate_calculation = (
                    pickled_intermediate_calculation
                )

                latest_data = (
                    BaseDataFile.query.filter(BaseDataFile.user_id == user_id)
                    .order_by(BaseDataFile.closing_date.desc())
                    .first()
                )
                closing_date = latest_data.closing_date.strftime("%Y-%m-%d")
                # generate response
                response_data = pbc.generate_response()
                # upsert pickled_response_data
                pickled_response_data = pickle.dumps(response_data)
                base_data_file.response = pickled_response_data

                # included_excluded_assets_map = {}
                # json_include_exclude_map = json.dumps(included_excluded_assets_map)
                # base_data_file.included_excluded_assets_map = json_include_exclude_map
                response_data["closing_date"] = closing_date

            response_data["fund_type"] = base_data_file.fund_type
            # update base_data_file object
            db.session.add(base_data_file)
            db.session.commit()
            return jsonify(response_data)

        except Exception as e:
            print(str(e))
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
    if request.method == "DELETE":
        try:
            data = request.get_json()
            user_id = data.get("user_id")
            base_data_file_id = data.get("base_data_file_id")
            base_data_file = BaseDataFile.query.filter_by(id=base_data_file_id).first()
            if base_data_file:
                what_if_analysis_list = WhatIfAnalysis.query.filter_by(
                    base_data_file_id=base_data_file.id
                ).all()
                for what_if_analysis in what_if_analysis_list:
                    WiaRefSheets.query.filter_by(
                        what_if_analysis_id=what_if_analysis.id
                    ).delete()
                    db.session.delete(what_if_analysis)
                db.session.delete(base_data_file)
                db.session.commit()
                return (
                    jsonify({"error": True, "message": "Data deleted successfully"}),
                    200,
                )
            else:
                return jsonify({"error": True, "message": "Data not found"}), 404
        except Exception as e:
            return (
                jsonify(
                    {
                        "error": True,
                        "error_type": str(type(e).__name__),
                        "error_file_details": f"error on line {e.__traceback__.tb_lineno} inside {__file__}",
                    }
                ),
                500,
            )


def get_table_from_card_function():
    data = request.get_json()
    base_data_file_id = data.get("base_data_file_id")
    card_name = data["card_name"]

    user_id = data.get(
        "user_id"
    )  # recieving user_id from frontend. Once JWT is implemented, user_id will be fetched from token

    # retrieve base data files from database if base_data_file_id is received
    if base_data_file_id:
        base_data_file = BaseDataFile.query.filter_by(id=base_data_file_id).first()

    else:
        # base_data_file_id will not be received in landing page. Finding base_data_file with latest closing date for given user_id
        base_data_file = (
            BaseDataFile.query.filter(
                BaseDataFile.user_id == user_id, BaseDataFile.response != None
            )
            .order_by(BaseDataFile.closing_date.desc())
            .first()
        )

    intermediate_calculation = pickle.loads(base_data_file.intermediate_calculation)

    if base_data_file.fund_type == "PCOF":
        df_Availability_Borrower = intermediate_calculation["df_Availability_Borrower"]
        df_principle_obligations = intermediate_calculation["df_principle_obligations"]
        obligator_copy = df_principle_obligations.copy()
        obligator_copy = obligator_copy.fillna(0)
        df_Availability_Borrower = df_Availability_Borrower.copy()
        df_Availability_Borrower = number_formatting_for_availablity(
            df_Availability_Borrower
        )
        card_name_column_mapping = {
            "Total BB": ["Total Borrowing Base"],
            "Leverage BB": [
                "Portfolio > 8 Eligible Issuers?",
                "FMV of Portfolio",
                "Effective Advance Rate on FMV of Portfolio",
                "Portfolio Leverage Borrowing Base (as calculated)",
                "Maximum Advance Rate on PL Borrowing Base",
                "Portfolio Leverage Borrowing Base",
            ],
            "Subscription BB": [
                "Revolving Closing Date",
                "Date of determination:",
                "Months since Revolving Closing Date",
                "Commitment Period (3 years from Final Closing Date, as defined in LPA)",
                "Uncalled Capital Commitments",
                "Subscription Borrowing Base",
                "Effective Advance Rate on Total Uncalled Capital",
                "Months since Revolving Closing Date",
            ],
            "Availability": [
                "Subscription Borrowing Base",
                "Portfolio Leverage Borrowing Base",
                "Total Borrowing Base",
                "(b) Facility Size",
                "Lesser of (a) and (b)",
                "Outstandings",
                "Net Debt Availbility",
                "Gross BB Utilization",
                "Facility Utilization ",
            ],
        }
        # if obligators net capital data
        if card_name == "Obligors net capital":
            obligators_net_capital = obligator_net_capital_data(obligator_copy)
            return jsonify(obligators_net_capital)
        # if any other data
        card_table = remaining_card_data(
            card_name, card_name_column_mapping, df_Availability_Borrower
        )
    elif base_data_file.fund_type == "PFLT":
        if card_name == "Borrowing Base":
            borrowing_base_df = intermediate_calculation["Borrowing Base"]
            borrowing_base_card_rows = [
                "Aggregate Collateral Balance (without duplication) sum of (i)-(vi)",
                "(i) Aggregate Principal Balance of all Collateral Loans (other than Defaulted, Restructured, Haircut Ineligible, and Discount)",
                "(ii) Defaulted Collateral Loan Balance",
                "(iii) The aggregate purchase price of all Discount Loans that are Eligible Collateral Loans and not Defaulted, Haircut or Restructured",
                "(iv) The aggregate Unfunded Commitments of all Delayed Drawdown and Revolvers that are Eligible Loans",
                "(v) The Credit Improved Loan Balance",
                "(vi) The Haircut Collateral Loan Balance",
                "Excess Concentration Amount",
            ]

            borrowing_base_sheet_df = borrowing_base_df[
                borrowing_base_df[borrowing_base_df.columns[0]].isin(
                    borrowing_base_card_rows
                )
            ]

            card_table = {
                column: [
                    {
                        "data": (
                            "$" + numerize.numerize(cell)
                            if type(cell) == int or type(cell) == float
                            else cell
                        )
                    }
                    for cell in borrowing_base_sheet_df[column]
                ]
                for column in borrowing_base_sheet_df.columns.tolist()
            }
            card_table["columns"] = [{"data": borrowing_base_sheet_df.columns.tolist()}]
        if card_name == "Maximum Available Amount":
            borrowing_base_df = intermediate_calculation["Borrowing Base"]
            borrowing_base_card_rows = [
                "Facility Amount, less",
                "(A) Revolving Exposure, plus",
                "(A) Amount on deposit in the Revolving Reserve Account",
                "(A) Total of above 3",
                "(x) Borrowing Base, multipled by",
                "(y) Weighted Average Advance Rate, minus",
                "Foreign Currency Variability Reserve, minus",
                "(B) Revolving Exposure, plus",
                "(B) Cash on deposit in Principal Collection Subaccount",
                "(B) Amount on deposit in the Revolving Reserve Account",
                "(B) Total Of Above 5",
                "Aggregate Collateral Balance, minus",
                "Minimum Equity Amount, plus",
                "(C) Cash on deposit in Principal Collection Subaccount",
                "(C) Total of above 3",
            ]
            borrowing_base_sheet_df = borrowing_base_df[
                borrowing_base_df[borrowing_base_df.columns[0]].isin(
                    borrowing_base_card_rows
                )
            ]

            card_table = {
                column: [
                    {
                        "data": (
                            "$" + numerize.numerize(cell)
                            if type(cell) == int or type(cell) == float
                            else cell
                        )
                    }
                    for cell in borrowing_base_sheet_df[column]
                ]
                for column in borrowing_base_sheet_df.columns.tolist()
            }
            card_table["columns"] = [{"data": borrowing_base_sheet_df.columns.tolist()}]
        if card_name == "Advance Outstandings":
            borrowing_base_df = intermediate_calculation["Borrowing Base"]
            borrowing_base_card_rows = [
                "Advances Outstanding at beginning of the Interest Accrual Period",
                "Advances/(Repayments) during the period through and including & TEXT",
                "Advances Outstanding as of & TEXT",
            ]
            borrowing_base_sheet_df = borrowing_base_df[
                borrowing_base_df[borrowing_base_df.columns[0]].isin(
                    borrowing_base_card_rows
                )
            ]

            card_table = {
                column: [
                    {
                        "data": (
                            "$" + numerize.numerize(cell)
                            if type(cell) == int or type(cell) == float
                            else cell
                        )
                    }
                    for cell in borrowing_base_sheet_df[column]
                ]
                for column in borrowing_base_sheet_df.columns.tolist()
            }
            card_table["columns"] = [{"data": borrowing_base_sheet_df.columns.tolist()}]

        if card_name == "Availability":
            borrowing_base_df = intermediate_calculation["Borrowing Base"]
            borrowing_base_card_rows = [
                "(A) Maximum Available Amount",
                "(B) Advances",
                "AVAILABILITY - (a) minus (b)",
            ]
            borrowing_base_sheet_df = borrowing_base_df[
                borrowing_base_df[borrowing_base_df.columns[0]].isin(
                    borrowing_base_card_rows
                )
            ]

            card_table = {
                column: [
                    {
                        "data": (
                            "$" + numerize.numerize(cell)
                            if type(cell) == int or type(cell) == float
                            else cell
                        )
                    }
                    for cell in borrowing_base_sheet_df[column]
                ]
                for column in borrowing_base_sheet_df.columns.tolist()
            }
            card_table["columns"] = [{"data": borrowing_base_sheet_df.columns.tolist()}]

        if card_name == "Total Credit Facility Balance":
            Credit_Balance_Projection_df = intermediate_calculation[
                "Credit Balance Projection"
            ]
            card_table = {
                column: [
                    {
                        "data": (
                            "$" + numerize.numerize(cell)
                            if type(cell) == int or type(cell) == float
                            else cell
                        )
                    }
                    for cell in Credit_Balance_Projection_df[column]
                ]
                for column in Credit_Balance_Projection_df.columns.tolist()
            }
            card_table["columns"] = [
                {"data": Credit_Balance_Projection_df.columns.tolist()}
            ]

    return jsonify(card_table)


def get_asset_selection_table_function():
    data = request.get_json()
    base_data_file_id = data.get("base_data_file_id")
    if not base_data_file_id:
        return jsonify({"error": True, "message": "base_data_file_id is required"}), 400
    try:
        base_data_file = BaseDataFile.query.filter_by(id=base_data_file_id).first()
        if not base_data_file:
            return jsonify({"error": True, "message": "base_data_file not found"}), 404
        asset_selection_table = {"columns": [], "data": []}

        if base_data_file.fund_type == "PCOF":
            included_assets = json.loads(base_data_file.included_excluded_assets_map)[
                "included_assets"
            ]
            sheet_df_dict = pickle.loads(base_data_file.file_data)
            df_PL_BB_Build = sheet_df_dict["PL BB Build"]
            selected_columns_list = ["Is Eligible Issuer"]
            user_config = UserConfig.query.filter_by(
                user_id=base_data_file.user_id
            ).first()
            if not user_config:
                user_config = UserConfig(user_id=base_data_file.user_id)
                user_config.assets_selection_columns = json.dumps(
                    {
                        base_data_file.fund_type: [
                            "Investment Name",
                            "Investment Investment Type",
                            "Investment Par",
                            "Investment Industry",
                            "Investment Closing Date",
                        ]
                    }
                )
                db.session.add(user_config)
                db.session.commit()
                db.session.refresh(user_config)
            else:
                assets_selection_columns = json.loads(
                    user_config.assets_selection_columns
                )
                if not assets_selection_columns.get(base_data_file.fund_type):
                    assets_selection_columns[base_data_file.fund_type] = [
                        "Investment Name",
                        "Investment Investment Type",
                        "Investment Par",
                        "Investment Industry",
                        "Investment Closing Date",
                    ]
                    user_config.assets_selection_columns = json.dumps(
                        assets_selection_columns
                    )
                    db.session.add(user_config)
                    db.session.commit()
                    db.session.refresh(user_config)

            PCOF_assets_selection_columns = json.loads(
                user_config.assets_selection_columns
            )[base_data_file.fund_type]
            for column in PCOF_assets_selection_columns:
                selected_columns_list.append(column)
            selected_column_df_PL_BB_Build = df_PL_BB_Build[selected_columns_list]
            eligible_assets_mask = (
                selected_column_df_PL_BB_Build["Is Eligible Issuer"] == "Yes"
            )
            eligible_assets_df = selected_column_df_PL_BB_Build[eligible_assets_mask]
            eligible_assets_df.fillna("", inplace=True)

            selected_columns_list.remove("Is Eligible Issuer")
            eligible_assets_df = eligible_assets_df[selected_columns_list]
            # find columns containing null values  (fillna('') does not fills NaT values)
            columns_with_nulls = eligible_assets_df.columns[
                eligible_assets_df.isnull().any()
            ]
            # replace all null values with ''
            for col in columns_with_nulls:
                eligible_assets_df[col] = eligible_assets_df[col].astype(str).fillna("")

            asset_selection_table["columns"] = [
                {"label": column, "key": column.replace(" ", "_")}
                for column in eligible_assets_df.columns
            ]

            for index, row in eligible_assets_df.iterrows():
                row_data = {}
                row_data["isIncluded"] = False
                for col, value in row.items():
                    if col == "Investment Name" and value in included_assets:
                        row_data["isIncluded"] = True
                    if isinstance(value, (int, float)):
                        if col in [
                            "Rates Current LIBOR/Floor",
                            "Rates Fixed Coupon",
                            "Rates Floating Cash Spread",
                            "Leverage LTV Thru PCOF IV",
                        ]:
                            row_data[col.replace(" ", "_")] = "{:,.01f}%".format(
                                value * 100
                            )
                        elif col in [
                            "Financials LTM Revenue ($MMs)",
                            "Financials LTM EBITDA ($MMs)",
                            "Leverage Revolver Commitment",
                            "Leverage Total Enterprise Value",
                            "Leverage Total Leverage",
                            "Leverage PCOF IV Leverage",
                            "Leverage Attachment Point",
                        ]:
                            row_data[col.replace(" ", "_")] = numerize.numerize(
                                value, 2
                            )
                        else:
                            row_data[col.replace(" ", "_")] = "$" + numerize.numerize(
                                value, 2
                            )
                    elif isinstance(value, datetime):
                        row_data[col.replace(" ", "_")] = value.strftime("%Y-%m-%d")
                    else:
                        row_data[col.replace(" ", "_")] = value
                asset_selection_table["data"].append(row_data)

        else:
            a = base_data_file.included_excluded_assets_map
            print(type(a))
            included_assets = json.loads(base_data_file.included_excluded_assets_map)[
                "included_assets"
            ]
            user_config = UserConfig.query.filter_by(
                user_id=base_data_file.user_id
            ).first()
            if not user_config:
                user_config = UserConfig(user_id=base_data_file.user_id)
                user_config.assets_selection_columns = json.dumps(
                    {
                        base_data_file.fund_type: [
                            "Obligor Name",
                            "Loan Type (Term / Delayed Draw / Revolver)",
                            "Purchase Price",
                            "Obligor Industry",
                            "Maturity Date",
                        ]
                    }
                )
                db.session.add(user_config)
                db.session.commit()
                db.session.refresh(user_config)
            else:
                assets_selection_columns = json.loads(
                    user_config.assets_selection_columns
                )
                if not assets_selection_columns.get(base_data_file.fund_type):
                    assets_selection_columns[base_data_file.fund_type] = [
                        "Obligor Name",
                        "Loan Type (Term / Delayed Draw / Revolver)",
                        "Purchase Price",
                        "Obligor Industry",
                        "Maturity Date",
                    ]
                    user_config.assets_selection_columns = json.dumps(
                        assets_selection_columns
                    )
                    db.session.add(user_config)
                    db.session.commit()
                    db.session.refresh(user_config)

            PFLT_assets_selection_columns = json.loads(
                user_config.assets_selection_columns
            )[base_data_file.fund_type]
            selected_columns_list = []
            for column in PFLT_assets_selection_columns:
                selected_columns_list.append(column)

            xl_df_map = pickle.loads(base_data_file.file_data)
            loan_list_df = xl_df_map["Loan List"]

            selected_column_loan_list_df = loan_list_df[selected_columns_list]
            selected_column_loan_list_df.fillna("")
            asset_selection_table["columns"] = [
                {"label": column, "key": column.replace(" ", "_")}
                for column in selected_column_loan_list_df.columns
            ]

            for index, row in selected_column_loan_list_df.iterrows():
                row_data = {}
                row_data["isIncluded"] = False
                for col, value in row.items():
                    if col == "Obligor Name" and value in included_assets:
                        row_data["isIncluded"] = True
                    if selected_column_loan_list_df.dtypes[col] in ["datetime64[ns]"]:
                        if not pd.isna(value):
                            # row_data[col.replace(" ", "_")] = value.strftime("%Y-%m-%d")
                            value = value.strftime("%Y-%m-%d")
                        else:
                            value = ""
                    if col == "Purchase Price":
                        value = str(round(value * 100, 2)) + "%"
                    row_data[col.replace(" ", "_")] = value
                asset_selection_table["data"].append(row_data)

        return jsonify(asset_selection_table)

    except Exception as e:
        return (
            jsonify(
                {
                    "error_status": True,
                    "error": str(e),
                    "error_type": str(type(e).__name__),
                    "error_file_details": f"error on line {e.__traceback__.tb_lineno} inside {__file__}",
                }
            ),
            500,
        )


def retrieve_data_function():
    try:
        data = request.get_json()
        user_id = data["user_id"]
        if not user_id:
            return jsonify({"error": True, "message": "User ID is required"}), 400
        # Query the database for data based on user_id
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
            }
            for file in base_data_files
        ]

        return jsonify({"error": False, "files_list": file_names})

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


def retrieve_borrowing_base_data_datewise_function():
    try:
        # Get user_id and closing_date is required
        data = request.get_json()
        selected_date = data["closing_date"]
        user_id = data["user_id"]
        # Query the database for data used based on selected data
        borrowing_base_results = BaseDataFile.query.filter_by(
            user_id=user_id, closing_date=selected_date
        ).first()
        # If no data found for selected date, return an error response
        # If no data found for selected date
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
                jsonify(
                    {"error": True, "message": f"No data found for {selected_date}"}
                ),
                404,
            )

        # Send complete data from the retrieved data
        pickle_borrowing_base_date_wise_results = borrowing_base_results.response
        borrowing_base_date_wise_results = pickle.loads(
            pickle_borrowing_base_date_wise_results
        )
        borrowing_base_date_wise_results["base_data_file_id"] = (
            borrowing_base_results.id
        )
        borrowing_base_date_wise_results["file_name"] = borrowing_base_results.file_name
        borrowing_base_date_wise_results["fund_name"] = borrowing_base_results.fund_type
        return jsonify(borrowing_base_date_wise_results)

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


def trend_graph_function():
    try:
        if request.method == "POST":
            user_id = int(request.form["user_id"])
            start_date = request.form.get("start_date")
            end_date = request.form.get("end_date")
            fund_type = request.form.get("fund_type")
            if fund_type == "":
                latest_base_data_file = (
                    BaseDataFile.query.filter(
                        BaseDataFile.user_id == user_id, BaseDataFile.response != None
                    )
                    .order_by(BaseDataFile.closing_date.desc())
                    .first()
                )
                fund_type = latest_base_data_file.fund_type
            if (
                start_date and end_date
            ):  # Check if both start_date and end_date are provided
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
            if fund_type == "PCOF":

                calc_df_Availability_Borrower = [
                    aval.intermediate_calculation for aval in base_data_file_sorted
                ]

                # Initialize lists for storing values
                subscription_borrowing_base_values = []
                portfolio_leverage_borrowing_base_values = []
                total_borrowing_base_values = []

                rows_to_extract = [
                    "Subscription Borrowing Base",
                    "Portfolio Leverage Borrowing Base",
                    "Total Borrowing Base",
                ]

                for pickle_file in calc_df_Availability_Borrower:
                    data = pickle.loads(pickle_file)
                    if "df_Availability_Borrower" in data:
                        df = data["df_Availability_Borrower"]
                        row_values = df.loc[df["A"].isin(rows_to_extract), "B"].tolist()
                        subscription_borrowing_base_values.append(row_values[0])
                        portfolio_leverage_borrowing_base_values.append(row_values[1])
                        total_borrowing_base_values.append(row_values[2])

                trend_graph_data = [
                    {
                        "date": closing_date,
                        "Tot BB": total_bb,
                        "Sub BB": subscription_bb,
                        "Lev BB": leverage_bb,
                    }
                    for closing_date, subscription_bb, leverage_bb, total_bb in zip(
                        closing_date,
                        subscription_borrowing_base_values,
                        portfolio_leverage_borrowing_base_values,
                        total_borrowing_base_values,
                    )
                ]
                trend_graph_response = {
                    "trend_graph_data": trend_graph_data,
                    "x_axis": ["Tot BB", "Sub BB", "Lev BB"],
                }
                return jsonify(trend_graph_response)
            else:
                trend_graph_data_response = (
                    PFLTTrendGraphResponseGenerator.generate_pflt_trendgraph(
                        base_data_file_sorted
                    )
                )
                # abc=
                return jsonify(trend_graph_data_response)
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


def download_excel_function():
    try:
        data = request.get_json()
        base_data_file_id = data["base_data_file_id"]
        user_id = data.get("user_id")

        base_data_file = BaseDataFile.query.filter_by(id=base_data_file_id).first()
        if base_data_file.user_id != user_id:
            return (
                jsonify(
                    {
                        "error": True,
                        "message": f"No data found for the user-id {user_id}",
                    }
                ),
                404,
            )

        pickled_intermediate_calculation = base_data_file.intermediate_calculation
        intermediate_calculation_dict = pickle.loads(pickled_intermediate_calculation)

        excel_data = BytesIO()
        with ExcelWriter(excel_data, engine="openpyxl") as writer:
            for dataframe_name, dataframe in intermediate_calculation_dict.items():
                dataframe.to_excel(writer, sheet_name=dataframe_name, index=False)

        # Set the BytesIO stream position to the beginning
        excel_data.seek(0)

        response = make_response(
            send_file(
                excel_data,
                as_attachment=True,
                download_name="output.xlsx",
                mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        )

        response.headers["Content-Disposition"] = "attachment; filename=output.xlsx"

        return response

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


def intermediate_metrics_for_parameters(what_if_analysis):
    what_if_intermediate_calculation = pickle.loads(
        what_if_analysis.intermediate_metrics_data
    )
    what_if_intermediate_metrics_output = what_if_intermediate_calculation[
        "modified_df_PL_BB_Output"
    ]
    simulation_type = what_if_analysis.simulation_type

    base_data_intermediate_metrics_output = what_if_intermediate_calculation[
        "inital_df_PL_BB_Output"
    ]

    # Prepare response data
    intermediate_metrics_data = {
        "columns": [],
        "data": [],
        "simulation_type": simulation_type,
    }

    # Add columns to the preview_table_data dynamically
    columns = [
        {"title": col, "key": col.replace(" ", "_")}
        for col in base_data_intermediate_metrics_output.columns
    ]
    intermediate_metrics_data["columns"] = columns

    # Compare data and prepare rows
    base_data_intermediate_metrics_output = (
        base_data_intermediate_metrics_output.fillna("")
    )
    what_if_intermediate_metrics_output = what_if_intermediate_metrics_output.fillna("")

    common_indices = base_data_intermediate_metrics_output.index.intersection(
        what_if_intermediate_metrics_output.index
    )

    for base_index in common_indices:
        base_row = base_data_intermediate_metrics_output.loc[base_index]
        what_if_row = what_if_intermediate_metrics_output.loc[base_index]
        row_data = {}

        for col, base_value in base_row.items():
            key = col.replace(" ", "_")
            try:
                what_if_value = what_if_row[col]
            except KeyError:
                return (
                    jsonify(
                        {
                            "error": f"Column '{col}' not found in what_if_intermediate_metrics_output"
                        }
                    ),
                    500,
                )

            if isinstance(base_value, (int, float)) and isinstance(
                what_if_value, (int, float)
            ):
                if col != "Adj. Advance Rate":
                    row_data[key] = {
                        "previous_value": "$" + numerize.numerize(base_value, 2),
                        "current_value": "$" + numerize.numerize(what_if_value, 2),
                        "changed": bool(
                            base_value != what_if_value
                        ),  # Convert to native Python bool
                    }
                else:
                    row_data[key] = {
                        "previous_value": "{:,.01f}%".format(base_value * 100),
                        "current_value": "{:,.01f}%".format(what_if_value * 100),
                        "changed": bool(
                            base_value != what_if_value
                        ),  # Convert to native Python bool
                    }
            elif isinstance(base_value, datetime) and isinstance(
                what_if_value, datetime
            ):
                row_data[key] = {
                    "previous_value": base_value.strftime("%Y-%m-%d"),
                    "current_value": what_if_value.strftime("%Y-%m-%d"),
                    "changed": bool(
                        base_value != what_if_value
                    ),  # Convert to native Python bool
                }
            else:
                row_data[key] = {
                    "previous_value": base_value,
                    "current_value": what_if_value,
                    "changed": bool(
                        base_value != what_if_value
                    ),  # Convert to native Python bool
                }

        intermediate_metrics_data["data"].append(row_data)

    return jsonify(intermediate_metrics_data), 200


def intermediate_metrics_for_add_asset(what_if_analysis):
    what_if_intermediate_calculation = pickle.loads(
        what_if_analysis.intermediate_metrics_data
    )
    what_if_intermediate_metrics_output = what_if_intermediate_calculation[
        "modified_df_PL_BB_Output"
    ]
    base_data_intermediate_metrics_output = what_if_intermediate_calculation[
        "inital_df_PL_BB_Output"
    ]
    simulation_type = what_if_analysis.simulation_type

    # Ensure indices are aligned
    base_data_intermediate_metrics_output.reset_index(drop=True, inplace=True)
    what_if_intermediate_metrics_output.reset_index(drop=True, inplace=True)

    # Identify rows that are not in base_data_intermediate_metrics_output
    base_first_col_set = set(base_data_intermediate_metrics_output.iloc[:, 0])
    added_indices = [
        idx
        for idx, row in what_if_intermediate_metrics_output.iterrows()
        if row.iloc[0] not in base_first_col_set
    ]

    intermediate_metrics_data = {
        "columns": [
            {"title": col, "key": col.replace(" ", "_")}
            for col in base_data_intermediate_metrics_output.columns
        ],
        "data": [],
        "simulation_type": simulation_type,
    }

    # Fill NaN values with empty string
    what_if_intermediate_metrics_output = what_if_intermediate_metrics_output.fillna("")

    # Process rows in what-if dataframe
    for index, row in what_if_intermediate_metrics_output.iterrows():
        row_data = {}
        for col, value in row.items():
            key = col.replace(" ", "_")
            if isinstance(value, (int, float)):
                if col != "Adj. Advance Rate":
                    current_value = "$" + numerize.numerize(value, 2)
                else:
                    current_value = "{:,.01f}%".format(value * 100)
            elif isinstance(value, datetime):
                current_value = value.strftime("%Y-%m-%d")
            else:
                current_value = value

            if index in added_indices:
                row_data[key] = {
                    "previous_value": "",
                    "current_value": current_value,
                    "changed": True,
                }
            else:
                row_data[key] = {
                    "previous_value": "",
                    "current_value": current_value,
                    "changed": False,
                }

            intermediate_metrics_data["data"].append(row_data)

    return jsonify(intermediate_metrics_data), 200


def intermediate_metrics_for_basefile(data):
    base_data_file_id = data.get("base_data_file_id")
    if base_data_file_id:
        base_data_file = BaseDataFile.query.filter_by(id=base_data_file_id).first()
    else:
        user_id = data.get("user_id")
        base_data_file = (
            BaseDataFile.query.filter(
                BaseDataFile.user_id == user_id, BaseDataFile.response != None
            )
            .order_by(BaseDataFile.closing_date.desc())
            .first()
        )

    if not base_data_file:
        return jsonify({"error": "BaseDataFile not found"}), 404

    intermediate_calculation = pickle.loads(base_data_file.intermediate_calculation)
    intermediate_metrics_output = intermediate_calculation["df_PL_BB_Output"]

    intermediate_metrics_data = {
        "columns": [],
        "data": [],
        "simulation_type": "base_data_file",
    }

    # Add columns to the preview_table_data dynamically
    intermediate_metrics_data["columns"] = [
        {"title": col, "key": col.replace(" ", "_")}
        for col in intermediate_metrics_output.columns
    ]

    # Add data to the preview_table_data
    intermediate_metrics_output = intermediate_metrics_output.fillna("")
    for _, row in intermediate_metrics_output.iterrows():
        row_data = {}
        for col, value in row.items():
            key = col.replace(" ", "_")
            if isinstance(value, (int, float)):
                if col != "Adj. Advance Rate":
                    row_data[key] = {
                        "previous_value": "",
                        "current_value": "$" + numerize.numerize(value, 2),
                        "changed": False,
                    }
                else:
                    row_data[key] = {
                        "previous_value": "",
                        "current_value": "{:,.01f}%".format(value * 100),
                        "changed": False,
                    }
            elif isinstance(value, datetime):
                row_data[key] = {
                    "previous_value": "",
                    "current_value": value.strftime("%Y-%m-%d"),
                    "changed": False,
                }
            else:
                row_data[key] = {
                    "previous_value": "",
                    "current_value": value,
                    "changed": False,
                }
        intermediate_metrics_data["data"].append(row_data)
    return jsonify(intermediate_metrics_data), 200


def get_intermediate_metrics_function():
    try:
        data = request.get_json()
        what_if_id = data.get("what_if_id")

        if what_if_id:
            # Query WhatIfAnalysis table for intermediate_calculation
            what_if_analysis = WhatIfAnalysis.query.filter_by(id=what_if_id).first()
            if not what_if_analysis:
                return jsonify({"error": "WhatIfAnalysis not found"}), 404

            simulation_type = what_if_analysis.simulation_type
            if simulation_type == "add_asset":
                return intermediate_metrics_for_add_asset(what_if_analysis)
            else:
                return intermediate_metrics_for_parameters(what_if_analysis)

        else:
            return intermediate_metrics_for_basefile(data)

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


def set_user_config_function():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        if not user_id:
            return (
                jsonify({"error_status": True, "message": "user_id is required"}),
                400,
            )

        user_config = UserConfig.query.filter_by(user_id=user_id).first()
        if not user_config:
            user_config = UserConfig(user_id=user_id)

        if data.get("assets_selection_columns"):
            fund_type = data.get("fund_type")
            # assets_selection_columns = ["Investment Name"]
            columns_to_update = data["assets_selection_columns"]
            if not columns_to_update:
                if fund_type == "PCOF":
                    assets_selection_columns = [
                        "Investment Name",
                        "Investment Investment Type",
                        "Investment Par",
                        "Investment Industry",
                        "Investment Closing Date",
                    ]
                if fund_type == "PFLT":
                    assets_selection_columns = [
                        "Obligor Name",
                        "Loan Type",
                        "Purchase Price",
                        "Obligor Industry",
                        "Maturity Date",
                    ]
            else:
                for column in columns_to_update:
                    assets_selection_columns.append(column)

            set_assets_selection_columns = pickle.loads(
                user_config.assets_selection_columns
            )
            if not set_assets_selection_columns.get(fund_type):
                user_config.assets_selection_columns = json.dumps(
                    {fund_type: assets_selection_columns}
                )
            else:
                set_assets_selection_columns[fund_type] = assets_selection_columns
                user_config.assets_selection_columns = json.dumps(
                    set_assets_selection_columns
                )
        if data.get("response_format"):
            user_config.response_format = json.dumps(data["response_format"])

        db.session.add(user_config)
        db.session.commit()

        return (
            jsonify(
                {"error_status": False, "message": "Configuration set successfully"}
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "error_status": True,
                    "error": str(e),
                    "error_type": str(type(e).__name__),
                    "error_file_details": f"error on line {e.__traceback__.tb_lineno} inside {__file__}",
                }
            ),
            500,
        )


def get_columns_list_function():
    # This API returns user_config selected 5 columns
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        fund_type = data.get("fund_type")
        if not user_id:
            return (
                jsonify({"error_status": True, "message": "user_id is required"}),
                400,
            )
        user_config = UserConfig.query.filter_by(user_id=user_id).first()
        if not user_config:
            return (
                jsonify({"error_status": True, "message": "No user config found"}),
                400,
            )
        assets_selection_columns = json.loads(user_config.assets_selection_columns)[
            fund_type
        ]
        return (
            jsonify(
                {
                    "error_status": False,
                    "assets_selection_columns": assets_selection_columns,
                }
            ),
            200,
        )
    except Exception as e:
        return (
            jsonify(
                {
                    "error_status": True,
                    "error": str(e),
                    "error_type": str(type(e).__name__),
                    "error_file_details": f"error on line {e.__traceback__.tb_lineno} inside {__file__}",
                }
            ),
            500,
        )


def get_previous_columns_function():
    try:
        data = request.get_json()
        base_data_file_id = data["base_data_file_id"]
        if not base_data_file_id:
            return (
                jsonify(
                    {"error_status": True, "message": "{base_data_file_id} is required"}
                ),
                400,
            )
        base_data_file = BaseDataFile.query.filter_by(id=base_data_file_id).first()

        included_excluded_assets_map = json.loads(
            base_data_file.included_excluded_assets_map
        )
        included_assets = included_excluded_assets_map["included_assets"]
        excluded_assets = included_excluded_assets_map["excluded_assets"]

        return jsonify(
            {
                "error_status": False,
                "included_assets": included_assets,
                "excluded_assets": excluded_assets,
            }
        )
    except Exception as e:
        return (
            jsonify(
                {
                    "error_status": True,
                    "error": str(e),
                    "error_type": str(type(e).__name__),
                    "error_file_details": f"error on line {e.__traceback__.tb_lineno} inside {__file__}",
                }
            ),
            500,
        )


def get_mathematical_formula_function():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        base_data_file_id = data["base_data_file_id"]
        col_name = data["col_name"]
        row_name = data["row_name"]

        base_data_file = BaseDataFile.query.filter_by(id=base_data_file_id).first()

        intermediate_calculation = pickle.loads(base_data_file.intermediate_calculation)

        df_PL_BB_Build = intermediate_calculation["df_PL_BB_Build"]
        df_PL_BB_Output = intermediate_calculation["df_PL_BB_Output"]

        response_dict = formula_info(
            df_PL_BB_Build, df_PL_BB_Output, row_name, col_name
        )

        return jsonify({"error_status": False, "response_dict": response_dict})
    except Exception as e:
        return (
            jsonify(
                {
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "error_file_details": f"error on line {e.__traceback__.tb_lineno} inside {__file__}",
                }
            ),
            500,
        )


def get_concentration_data_function():
    data = request.get_json()
    try:
        response_dict = get_data_concentration_test(data)
        return jsonify(response_dict), 200

    except Exception as e:
        return (
            jsonify(
                {
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "error_file_details": f"error on line {e.__traceback__.tb_lineno} inside {__file__}",
                }
            ),
            500,
        )


def concentration_data_analysis_function():
    data = request.get_json()
    try:

        concentration_Test_data = change_haircut_number(data)
        return jsonify(concentration_Test_data)

    except Exception as e:
        return (
            jsonify(
                {
                    "error_status": True,
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "error_file_details": f"error on line {e.__traceback__.tb_lineno} inside {__file__}",
                }
            ),
            500,
        )


def lock_concentration_test_function():
    data = request.get_json()
    try:
        response_dict = lock_concentration_test_data(data)
        if response_dict["status_code"] == 403:
            response_data = {
                "error_status": True,
                "message": "This file already exists in the system. Do you want to replace it? You might lose what if analysis data.",
            }, 403
        elif response_dict["status_code"] == 500:
            response_data = {
                "error_status": True,
                "message": response_dict["message"],
            }, 500
        elif response_dict["status_code"] == 200:
            response_data = response_dict["message"]
        return jsonify(response_data), 200

    except Exception as e:
        return (
            jsonify(
                {
                    "error_status": True,
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "error_file_details": f"error on line {e.__traceback__.tb_lineno} inside {__file__}",
                }
            ),
            500,
        )
