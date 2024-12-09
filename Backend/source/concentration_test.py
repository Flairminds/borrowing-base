from datetime import datetime, timezone
import json
import pickle
import pandas as pd

from models import BaseDataFile, WhatIfAnalysis
from response import number_formatting_for_concentration
from functionsCall import read_excels, functions_call_calculation


def get_data_concentration_test(data):
    import app

    db = app.db
    user_id = data.get("user_id")
    base_data_file_id = data["base_data_file_id"]

    previous_haircut_column = data.get("previous_haircut_column")

    base_data_file = BaseDataFile.query.filter_by(id=base_data_file_id).first()

    intermediate_calculation = pickle.loads(base_data_file.intermediate_calculation)

    df_PL_BB_Build = intermediate_calculation["df_PL_BB_Build"]
    selectd_columns = [
        "Investment Name",
        "Issuer",
        "Investment Industry",
        "Concentration Adjustment",
        "Concentration Adj. Elig. Amount",
    ]
    concentration_data = df_PL_BB_Build[selectd_columns]
    concentration_data.rename(
        columns={
            "Concentration Adjustment": "Adjustment",
            "Concentration Adj. Elig. Amount": "Concentration Limit Adj. Elig. Amount",
        },
        inplace=True,
    )

    preview_table_data = {"table": {"columns": [], "data": []}}
    # Add columns to the preview_table_data dynamically
    for col in concentration_data.columns:
        if col == "Adjustment":
            preview_table_data["table"]["columns"].append(
                {"title": "Adjustment", "key": "Haircut_number"}
            )
        else:
            preview_table_data["table"]["columns"].append(
                {"title": col, "key": col.replace(" ", "_")}
            )
    # Add data to the preview_table_data
    haircut_number_counter = 0
    for _, row in concentration_data.iterrows():
        row_data = {}
        for col, value in row.items():
            if isinstance(value, datetime):  # Convert datetime to string
                value = value.strftime("%Y-%m-%d")
            key = col.replace(" ", "_")
            if col == "Adjustment":
                key = "Haircut_number"
                if previous_haircut_column:
                    value = previous_haircut_column[haircut_number_counter]
                    haircut_number_counter += 1
            if isinstance(value, (int, float)):
                row_data[key] = f"{value:,.0f}"
            else:
                row_data[key] = value
        preview_table_data["table"]["data"].append(row_data)
    # Convert preview_table_data to JSON string and then parse it to a dictionary
    response_dict = json.loads(json.dumps(preview_table_data))

    return response_dict


def change_haircut_number(data):
    import WIA_API

    base_data_file_id = int(data["base_data_file_id"])

    updated_column_list = data["updated_column_list"]
    updated_column_list = [
        int(s.replace(",", "")) if isinstance(s, str) else s
        for s in updated_column_list
    ]

    previous_actual_column = data.get("previous_actual_column")
    if previous_actual_column:
        previous_actual_column = [
            previous_actual_value["data"]
            for previous_actual_value in previous_actual_column
        ]

    previous_result_column = data.get("previous_result_column")
    if previous_result_column:
        previous_result_column = [
            previous_result_value["data"]
            for previous_result_value in previous_result_column
        ]

    previous_haircut_column = data.get("previous_haircut_column")
    if previous_haircut_column:
        previous_haircut_column = [
            previous_haircut_value["data"]
            for previous_haircut_value in previous_haircut_column
        ]

    asset_percent = pd.Series(updated_column_list)

    # retrieve base data files from database

    base_data_file = BaseDataFile.query.filter_by(id=base_data_file_id).first()
    xl_sheet_df_map = pickle.loads(base_data_file.file_data)

    included_excluded_assets_map = json.loads(
        base_data_file.included_excluded_assets_map
    )
    included_assets = included_excluded_assets_map["included_assets"]

    intermediate_calculation = pickle.loads(base_data_file.intermediate_calculation)
    df_PL_BB_Results = intermediate_calculation["df_PL_BB_Results"]

    formatted_df_PL_BB_Results = number_formatting_for_concentration(df_PL_BB_Results)
    if not previous_actual_column:
        previous_actual_column = formatted_df_PL_BB_Results["Actual"].fillna(0).tolist()

    if not previous_result_column:
        previous_result_column = df_PL_BB_Results["Result"].tolist()

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

    updated_df_PL_BB_Build = df_PL_BB_Build.copy(deep=True)
    original_PL_BB_Build = df_PL_BB_Build.copy(deep=True)
    final_df_PL_BB_Build = WIA_API.updating_selected_assets(
        included_assets, updated_df_PL_BB_Build, original_PL_BB_Build
    )

    final_df_PL_BB_Build["debt"] = (
        final_df_PL_BB_Build["Financials LTM EBITDA ($MMs)"]
        * final_df_PL_BB_Build["Leverage Total Leverage"]
    )

    final_df_PL_BB_Build["Concentration Adjustment"] = asset_percent
    # updated_df_PL_BB_Build[wia_col_name] = asset_percent_df[f"change_{type}"]

    # calculate change after whatif analysis
    (
        final_df_PL_BB_Build,
        df_Inputs_Other_Metrics,
        Updated_df_Availability_Borrower,
        Updated_df_PL_BB_Results,
        df_subscriptionBB,
        Updated_df_security,
        df_industry,
        df_Input_pricing,
        df_Inputs_Portfolio_LeverageBorrowingBase,
        df_Obligors_Net_Capital,
        df_Inputs_Advance_Rates,
        df_Inputs_Concentration_limit,
        df_principle_obligations,
        Updated_df_segmentation_overview,
        df_PL_BB_Output,
    ) = functions_call_calculation(
        final_df_PL_BB_Build,
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

    selectd_columns = ["Concentration Tests", "Concentration Limit", "Actual", "Result"]
    concentration_data = Updated_df_PL_BB_Results[selectd_columns]
    # ---------------------
    Updated_df_PL_BB_Results.fillna({"Concentration Limit": 0}, inplace=True)
    Updated_df_PL_BB_Results = number_formatting_for_concentration(
        Updated_df_PL_BB_Results
    )
    concentration_tests = Updated_df_PL_BB_Results["Concentration Tests"].tolist()
    concentration_limits = Updated_df_PL_BB_Results["Concentration Limit"].tolist()
    actual_values = Updated_df_PL_BB_Results["Actual"].tolist()
    pass_list = Updated_df_PL_BB_Results["Result"].tolist()

    # Create required format for concentration test data
    concentration_Test_data = {
        "columns": [
            {"data": ["Concentration Test", "Concentration Limit", "Actual", "Result"]}
        ],
        "Concentration Test": [{"data": val} for val in concentration_tests[:-1]],
        "Concentration Limit": [
            {
                "data": (
                    ""
                    if val != val
                    else (
                        "$" + "{:,}".format(val)
                        if isinstance(val, (int, float))
                        else val
                    )
                )
            }
            for val in concentration_limits[:-1]
        ],
        "Actual": [
            {
                "data": (
                    ""
                    if val != val
                    else "{:,}".format(val) if isinstance(val, (int, float)) else val
                )
            }
            for val in actual_values[:-1]
        ],
        "Result": [{"data": (val)} for val in pass_list[:-1]],
    }

    if previous_actual_column and all(x is not None for x in previous_actual_column):
        # concentration_Test_data["columns"][0]['data'].append("Previous Actual")
        concentration_Test_data["Previous Actual"] = [
            {"data": val} for val in previous_actual_column[:-1]
        ]

    # Check if `previous_result_column` has no `None` values
    if previous_result_column and all(x is not None for x in previous_result_column):
        concentration_Test_data["columns"][0]["data"].append("Previous Result")
        concentration_Test_data["Previous Result"] = [
            {"data": val} for val in previous_result_column[:-1]
        ]

    if previous_haircut_column and all(x is not None for x in previous_haircut_column):
        concentration_Test_data["columns"][0]["data"].append("Previous Haircut Number")
        concentration_Test_data["Previous Haircut Number "] = [
            {"data": val} for val in previous_haircut_column[:]
        ]
    return concentration_Test_data


def delete_what_if_analysis(base_data_file_id):
    import app

    db = app.db
    try:
        WhatIfAnalysis.query.filter_by(base_data_file_id=base_data_file_id).delete()
        db.session.commit()
        return {
            "delete_status": False,
            "message": "What if analysis deleted successfully.",
        }
    except Exception as e:
        print(str(e))
        return (
            {
                "delete_status": True,
                "message": f"An error occurred while deleting what if analysis: ",
            },
        )


def lock_concentration_test_data(data):
    from response import formatted_data
    import app
    import WIA_API

    db = app.db

    base_data_file_id = int(data["base_data_file_id"])
    asset_haircut_number_mapping = data["asset_haircut_number_mapping"]
    asset_haircut_number_map = {}
    # asset_haircut_number_mapping = [int(s.replace(',', '')) if isinstance(s, str) else s for s in asset_haircut_number_mapping]
    for asset_haircut_number in asset_haircut_number_mapping:
        num = asset_haircut_number[list(asset_haircut_number.keys())[0]]
        if isinstance(num, str):
            num = float(num.replace(",", ""))
        asset_haircut_number_map[list(asset_haircut_number.keys())[0]] = num

        over_write = data.get("over_write")
    if not over_write:
        return {
            "error_status": True,
            "status_code": 403,
            "message": "This file already exists in the system. Do you want to replace it? You might lose what if analysis data.",
        }
    else:

        # retrieve base data files from database
        base_data_file = BaseDataFile.query.filter_by(id=base_data_file_id).first()

        delete_response = delete_what_if_analysis(base_data_file.id)
        if not delete_response["delete_status"]:

            xl_sheet_df_map = pickle.loads(base_data_file.file_data)

            included_excluded_assets_map = json.loads(
                base_data_file.included_excluded_assets_map
            )
            included_assets = included_excluded_assets_map["included_assets"]

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

            updated_df_PL_BB_Build = df_PL_BB_Build.copy(deep=True)
            original_PL_BB_Build = df_PL_BB_Build.copy(deep=True)

            final_df_PL_BB_Build = WIA_API.updating_selected_assets(
                included_assets, updated_df_PL_BB_Build, original_PL_BB_Build
            )

            # final_df_PL_BB_Build['Concentration Adjustment'] = final_df_PL_BB_Build['Investment Name'].map(asset_haircut_number_map)
            for assset_name in asset_haircut_number_map.keys():
                condition = final_df_PL_BB_Build["Investment Name"] == assset_name
                final_df_PL_BB_Build.loc[condition, "Concentration Adjustment"] = (
                    asset_haircut_number_map[assset_name]
                )
            xl_sheet_df_map["PL BB Build"] = final_df_PL_BB_Build

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
                final_df_PL_BB_Build,
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
            )
            # Construct response dictionary
            response_data = {
                "card_data": card_data,
                "segmentation_overview_data": segmentation_Overview_data,
                "security_data": security_data,
                "concentration_test_data": concentration_Test_data,
                "principal_obligation_data": principal_obligation_data,
                "segmentation_chart_data": segmentation_chart_data,
                "security_chart_data": security_chart_data,
            }

            base_data_file.file_data = pickle.dumps(xl_sheet_df_map)
            base_data_file.response = pickle.dumps(response_data)
            base_data_file.intermediate_calculation = pickle.dumps(
                intermediate_calculation
            )
            base_data_file.updated_at = datetime.now(timezone.utc)

            db.session.add(base_data_file)
            db.session.commit()

            return {"error_status": False, "status_code": 200, "message": response_data}
        else:
            return {
                "error_status": False,
                "status_code": 500,
                "message": delete_response["message"],
            }
