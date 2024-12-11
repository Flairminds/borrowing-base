from flask import (
    request,
    jsonify,
    send_file,
    make_response,
)
import pandas as pd
from pandas import ExcelWriter
from functionsCall import *

# from utility_functions import *
import json
from response import *
from session_files import *
from models import *
import pickle
from dotenv import load_dotenv
from io import BytesIO
from numerize import numerize

import modified_dfs_calculation

from source.services import wiaService
from source.utility.HTTPResponse import HTTPResponse


def updating_selected_assets(selected_assets, df_PL_BB_Build, original_PL_BB_Build):
    selected_assets_mask = df_PL_BB_Build["Investment Name"].isin(selected_assets)

    df_PL_BB_Build = df_PL_BB_Build[selected_assets_mask].reset_index(drop=True)
    df_PL_BB_Build = df_PL_BB_Build[df_PL_BB_Build["Is Eligible Issuer"] == "Yes"]
    if "Cash" not in selected_assets:
        cash_row = original_PL_BB_Build[
            original_PL_BB_Build["Investment Name"] == "Cash"
        ]
        # df_PL_BB_Build = pd.concat([df_PL_BB_Build, cash_row], ignore_index=True)
        df_PL_BB_Build = pd.concat([df_PL_BB_Build, cash_row], ignore_index=True)
    else:
        cash_row = original_PL_BB_Build[
            original_PL_BB_Build["Investment Name"] == "Cash"
        ]
        if cash_row["Is Eligible Issuer"].tolist()[0] == "No":
            df_PL_BB_Build = pd.concat([df_PL_BB_Build, cash_row], ignore_index=True)
    return df_PL_BB_Build


def get_included_excluded_assets_map_json(df_PL_BB_Build):
    eligible_assets_mask = df_PL_BB_Build["Is Eligible Issuer"] == "Yes"
    all_assets_list = df_PL_BB_Build[eligible_assets_mask]["Investment Name"].tolist()

    selected_assets = all_assets_list.copy()
    excluded_assets = all_assets_list.copy()

    for included_asset in selected_assets:
        if included_asset in all_assets_list:
            excluded_assets.remove(included_asset)

    included_excluded_assets_map = {
        "included_assets": selected_assets,
        "excluded_assets": excluded_assets,
    }

    return json.dumps(included_excluded_assets_map)


def add_what_if_analysis_to_db(
    response_data,
    simulation_name,
    base_data_file,
    note,
    initial_data,
    updated_data,
    intermediate_metrics_data,
    simulation_type,
):
    try:
        what_if_analysis = WhatIfAnalysis.query.filter_by(
            base_data_file_id=base_data_file.id, is_saved=False
        ).first()
        if not what_if_analysis:
            what_if_analysis = WhatIfAnalysis(
                base_data_file_id=base_data_file.id,
                simulation_name=simulation_name,
                response=pickle.dumps(response_data),
                note=note,
                initial_data=pickle.dumps(initial_data),
                updated_data=pickle.dumps(updated_data),
                intermediate_metrics_data=pickle.dumps(intermediate_metrics_data),
                simulation_type=simulation_type,
            )
        else:
            what_if_analysis.initial_data = pickle.dumps(initial_data)
            what_if_analysis.updated_data = pickle.dumps(updated_data)
            what_if_analysis.intermediate_metrics_data = pickle.dumps(
                intermediate_metrics_data
            )
            what_if_analysis.response = pickle.dumps(response_data)
            what_if_analysis.simulation_name = simulation_name
            what_if_analysis.simulation_type = simulation_type
            what_if_analysis.created_at = datetime.now(timezone.utc)
            what_if_analysis.updated_at = datetime.now(timezone.utc)
            what_if_analysis.note = note

        db.session.add(what_if_analysis)
        db.session.commit()
        db.session.refresh(what_if_analysis)
        return {"error": False, "what_if_analysis": what_if_analysis}
    except Exception as e:
        print(str(e))
        db.session.rollback()
        return {"error": True, "what_if_analysis": None}


def generate_simulation_name(previous_unnamed_simulations, simulation_type):
    if previous_unnamed_simulations:
        previous_unnamed_simulations = sorted(
            previous_unnamed_simulations, key=lambda x: x.created_at
        )

        previous_unnamed_simulation = previous_unnamed_simulations[-1]
        simulation_name = simulation_type + str(
            (int(previous_unnamed_simulation.simulation_name[-1]) + 1)
        )
    else:
        simulation_name = simulation_type + str("1")

    return simulation_name


def get_WIA_assets_function():
    try:
        data = request.get_json()
        base_data_file_id = data.get("base_data_file_id")
        type = data.get("type")

        if not base_data_file_id:
            return jsonify(
                {"error_status": True, "error": "base_data_file_id is required"}
            )

        base_data_file = BaseDataFile.query.filter_by(id=base_data_file_id).first()
        if not base_data_file:
            return jsonify({"error_status": True, "error": "base_data_file not found"})

        intermediate_calculation = pickle.loads(base_data_file.intermediate_calculation)
        df_PL_BB_Build = intermediate_calculation["df_PL_BB_Build"]

        if type == "Ebitda":
            opposite_type = "Leverage"
            wia_col_name = "Financials LTM EBITDA ($MMs)"
            opposite_wia_col_name = "Leverage Total Leverage"
        else:
            opposite_type = "Ebitda"
            wia_col_name = "Leverage Total Leverage"
            opposite_wia_col_name = "Financials LTM EBITDA ($MMs)"

        wia_df_PL_BB_Build = df_PL_BB_Build[
            ["Investment Name", f"{wia_col_name}", opposite_wia_col_name]
        ]

        included_assets = json.loads(base_data_file.included_excluded_assets_map)[
            "included_assets"
        ]
        selected_assets_mask = wia_df_PL_BB_Build["Investment Name"].isin(
            included_assets
        )
        wia_df_PL_BB_Build = wia_df_PL_BB_Build[selected_assets_mask]

        asset_whatIf_map_list = []
        for index, row in wia_df_PL_BB_Build.iterrows():
            row_data = {
                "InvestmentName": row["Investment Name"],
                "previousValue": round(row[f"{wia_col_name}"], 2),
                f"previous{opposite_type}": round(row[f"{opposite_wia_col_name}"], 2),
            }
            asset_whatIf_map_list.append(row_data)
        return jsonify({"asset_whatIf_map_list": asset_whatIf_map_list})
    except Exception as e:
        return jsonify(
            {
                "error_status": True,
                "error": str(e),
                "error_type": str(type(e).__name__),
                "error_file_details": f"error on line {e.__traceback__.tb_lineno} inside {__file__}",
            }
        )


def change_ebitda_function():
    try:
        data = request.get_json()
        base_data_file_id = int(data["base_data_file_id"])
        to_save = data["to_save"]
        type = data["type"]
        asset_percent_map_list = data["asset_percent_map_list"]

        # converting asset_percent_map_list dictionary required for df format
        asset_percent_dict = {
            "Investment Name": [],
            "previous value": [],
            "percentage": [],
        }

        for asset_data in asset_percent_map_list:
            asset_percent_dict["Investment Name"].append(asset_data["InvestmentName"])
            asset_percent_dict["previous value"].append(asset_data["previousValue"])
            asset_percent_dict["percentage"].append(
                int("0")
                if asset_data["updatedValue"] == ""
                else float(asset_data["updatedValue"])
            )

        asset_percent_df = pd.DataFrame(asset_percent_dict)

        if type == "Ebitda":
            wia_col_name = "Financials LTM EBITDA ($MMs)"
            opposite_wia_col = "Leverage Total Leverage"
        else:
            wia_col_name = "Leverage Total Leverage"
            opposite_wia_col = "Financials LTM EBITDA ($MMs)"
        # retrieve base data files from database
        base_data_file = BaseDataFile.query.filter_by(id=base_data_file_id).first()
        xl_sheet_df_map = pickle.loads(base_data_file.file_data)

        included_excluded_assets_map = json.loads(
            base_data_file.included_excluded_assets_map
        )
        included_assets = included_excluded_assets_map["included_assets"]
        initial_data_asset_inventory = pickle.loads(
            base_data_file.intermediate_calculation
        )["df_PL_BB_Build"]
        intermediate_metrics_data = {
            "inital_df_PL_BB_Output": pickle.loads(
                base_data_file.intermediate_calculation
            )["df_PL_BB_Output"]
        }

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

        # retrieve required calculated files from DB
        intermediate_calculation = pickle.loads(base_data_file.intermediate_calculation)
        calc_df_Availability_Borrower = intermediate_calculation[
            "df_Availability_Borrower"
        ]
        df_segmentation_overview = intermediate_calculation["df_segmentation_overview"]
        previous_security = intermediate_calculation["df_security"]
        updated_df_PL_BB_Build = df_PL_BB_Build.copy(deep=True)
        original_PL_BB_Build = df_PL_BB_Build.copy(deep=True)
        final_df_PL_BB_Build = updating_selected_assets(
            included_assets, updated_df_PL_BB_Build, original_PL_BB_Build
        )
        final_df_PL_BB_Build["debt"] = (
            final_df_PL_BB_Build["Financials LTM EBITDA ($MMs)"]
            * final_df_PL_BB_Build["Leverage Total Leverage"]
        )
        final_df_PL_BB_Build[wia_col_name] = asset_percent_df["previous value"] * (
            1 + asset_percent_df["percentage"] / 100
        )
        # updated_df_PL_BB_Build[wia_col_name] = asset_percent_df[f"change_{type}"]
        final_df_PL_BB_Build[opposite_wia_col] = (
            final_df_PL_BB_Build["debt"] / final_df_PL_BB_Build[wia_col_name]
        )

        pl_bb_build_to_save = final_df_PL_BB_Build.copy(deep=True)
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
        # sheets for whatif analysis
        merged_segmentation_overview, merged_df_security = sheets_for_whatif_analysis(
            df_segmentation_overview,
            previous_security,
            Updated_df_segmentation_overview,
            Updated_df_security,
        )
        # response for whatif analysis
        (
            card_data,
            segmentation_overview_data,
            security_data,
            concentration_Test_data,
            principal_obligation_data,
            segmentation_chart_data,
            security_chart_data,
        ) = formated_response_whatif_analysis(
            merged_segmentation_overview,
            merged_df_security,
            Updated_df_PL_BB_Results,
            df_principle_obligations,
            calc_df_Availability_Borrower,
            Updated_df_Availability_Borrower,
        )
        response_data = {
            "card_data": card_data,
            "segmentation_overview_data": segmentation_overview_data,
            "security_data": security_data,
            "concentration_test_data": concentration_Test_data,
            "principal_obligation_data": principal_obligation_data,
            "segmentation_chart_data": segmentation_chart_data,
            "security_chart_data": security_chart_data,
            "closing_date": base_data_file.closing_date.strftime("%Y-%m-%d"),
        }

        # add what if analysis to database
        simulation_type1 = f"change_{type}_"

        previous_unnamed_simulations = WhatIfAnalysis.query.filter(
            WhatIfAnalysis.base_data_file_id == base_data_file.id,
            WhatIfAnalysis.simulation_name.startswith(simulation_type1),
        ).all()

        simulation_name = generate_simulation_name(
            previous_unnamed_simulations, simulation_type1
        )
        if data.get("simulation_name"):
            simulation_name = data.get("simulation_name")
        note = data.get("note") or None

        intermediate_metrics_data["modified_df_PL_BB_Output"] = df_PL_BB_Output
        intermediate_metrics_data["modified_df_PL_BB_Build"] = final_df_PL_BB_Build
        intermediate_metrics_data["initial_df_PL_BB_Build"] = pl_bb_build_to_save

        # add_what_if_analysis_to_db(    response_data, simulation_name, base_data_file, note, initial_data, updated_data, intermediate_metrics_data, simulation_type

        what_if_analysis_result = add_what_if_analysis_to_db(
            response_data,
            simulation_name,
            base_data_file,
            note,
            initial_data=initial_data_asset_inventory,
            updated_data={"modified_assets_df": final_df_PL_BB_Build},
            intermediate_metrics_data=intermediate_metrics_data,
            simulation_type="change_" + type,
        )

        # what_if_analysis_result = add_what_if_analysis_to_db(
        #     response_data, simulation_name, base_data_file, note, asset_percent_df
        # )
        if not what_if_analysis_result["error"]:
            response_data["what_if_analysis_id"] = what_if_analysis_result[
                "what_if_analysis"
            ].id
            response_data["what_if_analysis_type"] = what_if_analysis_result[
                "what_if_analysis"
            ].simulation_type
            return jsonify(response_data)
        else:
            raise Exception("could not save ebitda change")

        # return jsonify(response_data)
    except Exception as e:
        return jsonify(
            {
                "error": str(e),
                "error_type": str(type(e).__name__),
                "error_file_details": f"error on line {e.__traceback__.tb_lineno} inside {__file__}",
            }
        )


def change_asset_function():
    try:
        data = request.get_json()
        base_data_file_id = int(data["base_data_file_id"])
        to_save = bool(int(data["to_save"]))
        # retrieve base data files from database
        base_data_file = BaseDataFile.query.filter_by(id=base_data_file_id).first()
        xl_sheet_df_map = pickle.loads(base_data_file.file_data)

        included_excluded_assets_map = json.loads(
            base_data_file.included_excluded_assets_map
        )
        included_assets = included_excluded_assets_map["included_assets"]
        # get dataframes from database
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

        # retrieve required calculated files from DB
        intermediate_calculation = pickle.loads(base_data_file.intermediate_calculation)
        calc_df_Availability_Borrower = intermediate_calculation[
            "df_Availability_Borrower"
        ]
        df_segmentation_overview = intermediate_calculation["df_segmentation_overview"]
        previous_security = intermediate_calculation["df_security"]
        original_PL_BB_Build = df_PL_BB_Build.copy(deep=True)
        updated_df_PL_BB_Build = df_PL_BB_Build.copy(deep=True)
        final_df_PL_BB_Build = updating_selected_assets(
            included_assets, updated_df_PL_BB_Build, original_PL_BB_Build
        )

        intermediate_metrics_data = {
            "inital_df_PL_BB_Output": pickle.loads(
                base_data_file.intermediate_calculation
            )["df_PL_BB_Output"]
        }

        pl_bb_build_to_save = final_df_PL_BB_Build.copy(deep=True)
        # Create uploaded_df with columns from selected_assets
        uploaded_df = pd.DataFrame(data["selected_assets"])
        uploaded_df.columns = uploaded_df.columns.str.replace("_", " ").str.title()
        uploaded_df = uploaded_df.reindex(columns=updated_df_PL_BB_Build.columns)
        # Concatenate df_PL_BB_Build and uploaded_df
        uploaded_df_PL_BB_Build = pd.concat(
            [final_df_PL_BB_Build, uploaded_df], ignore_index=True
        )
        uploaded_df_PL_BB_Build_to_save = uploaded_df_PL_BB_Build.copy(deep=True)
        # calculate change after whatif analysis
        (
            uploaded_df_PL_BB_Build,
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
            uploaded_df_PL_BB_Build,
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
        # sheets for whatif analysis
        merged_segmentation_overview, merged_df_security = sheets_for_whatif_analysis(
            df_segmentation_overview,
            previous_security,
            Updated_df_segmentation_overview,
            Updated_df_security,
        )
        # response for whatif analysis
        (
            card_data,
            segmentation_overview_data,
            security_data,
            concentration_Test_data,
            principal_obligation_data,
            segmentation_chart_data,
            security_chart_data,
        ) = formated_response_whatif_analysis(
            merged_segmentation_overview,
            merged_df_security,
            Updated_df_PL_BB_Results,
            df_principle_obligations,
            calc_df_Availability_Borrower,
            Updated_df_Availability_Borrower,
        )
        response_data = {
            "card_data": card_data,
            "segmentation_overview_data": segmentation_overview_data,
            "security_data": security_data,
            "concentration_test_data": concentration_Test_data,
            "principal_obligation_data": principal_obligation_data,
            "segmentation_chart_data": segmentation_chart_data,
            "security_chart_data": security_chart_data,
            "closing_date": base_data_file.closing_date.strftime("%Y-%m-%d"),
        }

        # add what if analysis to database
        simulation_type1 = "change_asset_"

        previous_unnamed_simulations = WhatIfAnalysis.query.filter(
            WhatIfAnalysis.base_data_file_id == base_data_file.id,
            WhatIfAnalysis.simulation_name.startswith(simulation_type1),
        ).all()

        simulation_name = generate_simulation_name(
            previous_unnamed_simulations, simulation_type1
        )
        if data.get("simulation_name"):
            simulation_name = data.get("simulation_name")
        note = data.get("note") or None

        intermediate_metrics_data["modified_df_PL_BB_Output"] = df_PL_BB_Output
        # intermediate_metrics_data["modified_df_PL_BB_Build"] = uploaded_df_PL_BB_Build
        # intermediate_metrics_data["initial_df_PL_BB_Build"] = pl_bb_build_to_save
        what_if_analysis_result = add_what_if_analysis_to_db(
            response_data,
            simulation_name,
            base_data_file,
            note,
            initial_data={"PL BB Build": pl_bb_build_to_save},
            updated_data={"modified_assets_df": uploaded_df_PL_BB_Build_to_save},
            intermediate_metrics_data=intermediate_metrics_data,
            simulation_type="add_asset",
        )

        if not what_if_analysis_result["error"]:
            response_data["what_if_analysis_id"] = what_if_analysis_result[
                "what_if_analysis"
            ].id
            response_data["what_if_analysis_type"] = what_if_analysis_result[
                "what_if_analysis"
            ].simulation_type
            return jsonify(response_data)
        else:
            raise Exception("Could not add assets")
        # else:
        #     return jsonify(response_data)
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


class AssetProcessor:
    def __init__(self, what_if_analysis):
        self.simulation_type = what_if_analysis.simulation_type
        # self.sheet_name = f"{self.simulation_type}_sheet"

        if self.simulation_type == "add_asset":
            self.init_add_asset(what_if_analysis)
        elif (
            self.simulation_type == "change_Ebitda"
            or self.simulation_type == "change_Leverage"
        ):
            self.init_asset_inventory(what_if_analysis)
        else:
            self.init_update_asset_inventory(what_if_analysis)

    def init_add_asset(self, what_if_analysis):
        initial_pl_bb_build = pickle.loads(what_if_analysis.initial_data)["PL BB Build"]
        updated_pl_bb_build = pickle.loads(what_if_analysis.updated_data)[
            "modified_assets_df"
        ]
        self.what_if_intermediate_metrics_output = updated_pl_bb_build
        self.base_data_intermediate_metrics_output = initial_pl_bb_build
        self.sheet_name = "PL BB Build"
        # Ensure indices are aligned
        self.base_data_intermediate_metrics_output.reset_index(drop=True, inplace=True)
        self.what_if_intermediate_metrics_output.reset_index(drop=True, inplace=True)

        self.data = {
            self.sheet_name: {
                "columns": [],
                "data": [],
                "new_data": [],
                "simulation_type": self.simulation_type,
            }
        }

        self.prepare_columns()
        self.fill_missing_values()
        self.added_indices = self.identify_added_rows()
        self.process_rows()

    def init_asset_inventory(self, what_if_analysis):
        self.asset_inventory_initial_pl_bb_build = pickle.loads(
            what_if_analysis.initial_data
        )
        self.asset_inventory_updated_data = pickle.loads(what_if_analysis.updated_data)
        self.asset_inventory_updated_pl_bb_build = self.asset_inventory_updated_data[
            "modified_assets_df"
        ]
        self.sheet_name = "PL BB Build"
        self.data = {
            self.sheet_name: {
                "columns": [],
                "data": [],
                "new_data": [],
                "simulation_type": self.simulation_type,
            }
        }

        self.specific_columns = [
            "Investment Name",
            "Issuer",
            "Financials LTM EBITDA ($MMs)",
            "Leverage Total Leverage",
            "Borrowing Base",
        ]
        self.renamed_columns = {
            "Investment Name": "Investor Name",
            "Financials LTM EBITDA ($MMs)": "EBITDA",
            "Leverage Total Leverage": "Leverage",
        }

        self.prepare_columns()
        self.fill_missing_values()
        self.process_rows()

    def init_update_asset_inventory(self, modified_base_data_file):
        modified_data = pickle.loads(modified_base_data_file.modified_data)
        initial_data = pickle.loads(modified_base_data_file.initial_data)

        self.data = {}
        for sheet in modified_data:
            self.sheet_name = sheet
            self.initial_df = initial_data[sheet]
            self.modified_df = modified_data[sheet]

            # self.data = {
            self.data[self.sheet_name] = {
                "columns": [],
                "data": [],
                "new_data": [],
                "simulation_type": self.simulation_type,
            }
            # }

            self.process_update_sheet_rows(sheet)

    def get_native_value(self, value, dtype):
        if isinstance(value, (np.integer, int)):
            if value != value:
                return ""
            if value == "":
                return value
            return numerize.numerize(int(value), 2)
        if isinstance(value, (np.floating, float)):
            if value != value:
                return ""
            if value == "":
                return "{:,.02}".format(value)
            return float(value)
        if dtype == "datetime64[ns]":
            if pd.isna(value):
                return ""
            if value == "":
                return ""
            return pd.to_datetime(value).strftime("%Y-%m-%d")
        if dtype == "object":
            if value != value:
                return ""
            return str(value)

    def process_update_sheet_rows(self, sheet_name):
        new_data = []
        for idx, row in self.modified_df.iterrows():
            row_data = {}
            unique_id = row[self.modified_df.columns[0]]
            if unique_id not in self.initial_df[self.initial_df.columns[0]].tolist():
                for col, current_value in row.items():
                    key = col.replace(" ", "_")
                    if col == self.modified_df.columns[0]:
                        self.data[sheet_name]["new_data"].append(current_value)

                    row_data[key] = {
                        "previous_value": "",
                        "current_value": self.get_native_value(
                            current_value, self.initial_df[col].dtype
                        ),  # format it accordingly
                        "changed": True,
                    }
            else:
                for col, current_value in row.items():
                    key = col.replace(" ", "_")
                    # previous_value = self.initial_df[col].values[0]
                    previous_value = self.initial_df[
                        self.initial_df[self.initial_df.columns[0]] == unique_id
                    ][col].values[0]

                    # Format the values accordingly as per the data type of the column
                    previous_value = self.get_native_value(
                        previous_value, self.initial_df[col].dtype
                    )
                    current_value = self.get_native_value(
                        current_value, self.initial_df[col].dtype
                    )

                    row_data[key] = {
                        "previous_value": previous_value,
                        "current_value": current_value,
                        "changed": bool(current_value != previous_value),
                    }
                    # previous_value = self.get_native_value(previous_value, self.initial_df[col].dtype)
                    # current_value = self.get_native_value(previous_value, self.initial_df[col].dtype)

                    # row_data[key] = {
                    #     "previous_value": previous_value,
                    #     "current_value": current_value,
                    #     "changed": bool(current_value != previous_value),
                    # }

            self.data[sheet_name]["data"].append(row_data)

        self.data[sheet_name]["columns"] = [
            {"key": column_name.replace(" ", "_"), "title": column_name}
            for column_name in self.modified_df.columns.tolist()
        ]

    def prepare_columns(self):
        if self.simulation_type == "add_asset":
            self.data[self.sheet_name]["columns"] = [
                {"title": col, "key": col.replace(" ", "_")}
                for col in self.base_data_intermediate_metrics_output.columns
            ]
        elif (
            self.simulation_type == "change_Ebitda"
            or self.simulation_type == "change_Leverage"
        ):
            columns = [
                {
                    "title": self.renamed_columns.get(col, col),
                    "key": self.renamed_columns.get(col, col).replace(" ", "_"),
                }
                for col in self.specific_columns
            ]
            self.data[self.sheet_name]["columns"] = columns
        else:
            self.data[self.sheet_name]["columns"] = [
                {"title": col, "key": col.replace(" ", "_")}
                for col in self.modified_df.columns
            ]

    def fill_missing_values(self):
        if self.simulation_type == "add_asset":
            self.what_if_intermediate_metrics_output.fillna("", inplace=True)
            self.base_data_intermediate_metrics_output.fillna("", inplace=True)
        else:
            self.asset_inventory_initial_pl_bb_build = (
                self.asset_inventory_initial_pl_bb_build[self.specific_columns]
                .rename(columns=self.renamed_columns)
                .fillna("")
            )
            self.asset_inventory_updated_pl_bb_build = (
                self.asset_inventory_updated_pl_bb_build[self.specific_columns]
                .rename(columns=self.renamed_columns)
                .fillna("")
            )

    def identify_added_rows(self):
        base_first_col_set = set(self.base_data_intermediate_metrics_output.iloc[:, 0])
        added_indices = [
            idx
            for idx, row in self.what_if_intermediate_metrics_output.iterrows()
            if row.iloc[0] not in base_first_col_set
        ]
        return added_indices

    def format_value(self, value, col):
        if pd.isna(value):
            return ""
        if isinstance(value, (int, float)):
            if col != "Adj. Advance Rate":
                return numerize.numerize(float(value), 2)
            else:
                return "{:,.01f}%".format(value * 100)
        elif isinstance(value, (datetime, pd.Timestamp)):
            return value.strftime("%Y-%m-%d")
        else:
            return str(value)

    def process_rows(self):
        if self.simulation_type == "add_asset":
            self.process_add_asset_rows()
        elif (
            self.simulation_type == "change_Ebitda"
            or self.simulation_type == "change_Leverage"
        ):
            self.process_asset_inventory_rows()
        # else:
        #     self.process_update_asset_inventory_rows()

    def process_add_asset_rows(self):
        for idx, row in self.what_if_intermediate_metrics_output.iterrows():
            row_data = {}
            for col, current_value in row.items():
                key = col.replace(" ", "_")
                formatted_current_value = self.format_value(current_value, col)
                if idx in self.added_indices:
                    row_data[key] = {
                        "previous_value": "",
                        "current_value": formatted_current_value,
                        "changed": True,
                    }
                else:
                    row_data[key] = {
                        "previous_value": "",
                        "current_value": formatted_current_value,
                        "changed": False,
                    }

            self.data[self.sheet_name]["data"].append(row_data)

    def process_asset_inventory_rows(self):
        for index, row in self.asset_inventory_updated_pl_bb_build.iterrows():
            row_data = {}
            base_row = self.asset_inventory_initial_pl_bb_build[
                self.asset_inventory_initial_pl_bb_build["Investor Name"]
                == row["Investor Name"]
            ]

            if not base_row.empty:
                base_row = base_row.squeeze()
            else:
                base_row = None

            for col, value in row.items():
                key = col.replace(" ", "_")

                if base_row is not None:
                    base_value = base_row[col]
                    changed = bool(base_value != value)
                    percent_change = (
                        self.calculate_percent_change(base_value, value)
                        if changed
                        else ""
                    )
                    formatted_previous_value = self.format_value(base_value, col)
                else:
                    base_value = None
                    changed = False
                    percent_change = ""
                    formatted_previous_value = ""

                formatted_current_value = self.format_value(value, col)

                row_data[key] = {
                    "previous_value": formatted_previous_value,
                    "current_value": formatted_current_value,
                    "changed": changed,
                    "percent_change": percent_change,
                }

            self.data[self.sheet_name]["data"].append(row_data)

    def calculate_percent_change(self, old_value, new_value):
        if isinstance(old_value, (int, float)) and isinstance(new_value, (int, float)):
            if old_value == 0:
                return f"{new_value:.2f}%"
            percent_change = ((new_value - old_value) / abs(old_value)) * 100
            return f"{percent_change:.2f}%"
        else:
            return ""

    def get_response(self):
        return self.data


def get_selected_WIA_asstes_function():
    try:
        data = request.get_json()
        what_if_analysis_id = data["what_if_analysis_id"]
        what_if_analysis_type = data["what_if_analysis_type"]

        if what_if_analysis_type == "Update asset":
            what_if_analysis = ModifiedBaseDataFile.query.filter_by(
                id=what_if_analysis_id
            ).first()
        else:
            what_if_analysis = WhatIfAnalysis.query.filter_by(
                id=what_if_analysis_id
            ).first()
        if not what_if_analysis:
            return (
                jsonify(
                    {"error_status": True, "message": "what_if_analysis not found"}
                ),
                404,
            )

        processor = AssetProcessor(what_if_analysis)
        selected_WIA_asstes_table_data = processor.get_response()
        return jsonify(selected_WIA_asstes_table_data), 200

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


def select_what_if_analysis_function():
    data = request.get_json()
    what_if_analysis_id = data["what_if_analysis_id"]
    try:
        what_if_analysis = WhatIfAnalysis.query.filter_by(
            id=what_if_analysis_id
        ).first()
        if not what_if_analysis:
            return (
                jsonify({"error": True, "message": "WHat if analysis not found"}),
                404,
            )
        else:
            pickled_response = what_if_analysis.response
            what_if_analysis_response = pickle.loads(pickled_response)
            return jsonify(
                {"error": False, "what_if_analysis": what_if_analysis_response}
            )
    except Exception as e:
        print(e)
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


def get_analysis_list_function():
    try:
        data = request.get_json()
        user_id = data["user_id"]

        if not user_id:
            return jsonify({"error": True, "message": "User ID is required"}), 400

        what_if_data = (
            db.session.query(BaseDataFile, WhatIfAnalysis)
            .join(WhatIfAnalysis, WhatIfAnalysis.base_data_file_id == BaseDataFile.id)
            .filter(BaseDataFile.user_id == user_id, WhatIfAnalysis.is_saved == True)
            .all()
        )
        update_Asset_what_if_data = (
            db.session.query(BaseDataFile, ModifiedBaseDataFile)
            .join(
                ModifiedBaseDataFile,
                ModifiedBaseDataFile.base_data_file_id == BaseDataFile.id,
            )
            .filter(
                BaseDataFile.user_id == user_id, ModifiedBaseDataFile.is_saved == True
            )
            .all()
        )

        # Construct the response in the desired format
        response = []
        for base_data_file, what_if_entry in what_if_data:
            result_entry = {
                "base_file_name": base_data_file.file_name,  # Assuming file_name is the column name for the file name
                "name": what_if_entry.simulation_name,
                "note": what_if_entry.note if what_if_entry.note else "",
                "what_if_analysis_id": what_if_entry.id,
                "simulation_type": what_if_entry.simulation_type,
                "last_updated": (
                    what_if_entry.updated_at.strftime("%m/%d/%Y")
                    if what_if_entry.updated_at
                    else ""
                ),  # Assuming updated_at is a datetime object
                "created_date": (
                    what_if_entry.created_at.strftime("%m/%d/%Y %H:%M")
                    if what_if_entry.created_at
                    else ""
                ),  # Assuming created_at is a datetime object
            }
            response.append(result_entry)

        for base_data_file, what_if_entry in update_Asset_what_if_data:
            result_entry = {
                "base_file_name": base_data_file.file_name,  # Assuming file_name is the column name for the file name
                "name": what_if_entry.simulation_name,
                "note": what_if_entry.note if what_if_entry.note else "",
                "what_if_analysis_id": what_if_entry.id,
                "simulation_type": what_if_entry.simulation_type,
                "last_updated": (
                    what_if_entry.updated_at.strftime("%m/%d/%Y")
                    if what_if_entry.updated_at
                    else ""
                ),  # Assuming updated_at is a datetime object
                "created_date": (
                    what_if_entry.created_at.strftime("%m/%d/%Y %H:%M")
                    if what_if_entry.created_at
                    else ""
                ),  # Assuming created_at is a datetime object
            }
            response.append(result_entry)

        return jsonify(Whatif_data=response)

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


def add_asset_overview_function():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file part"})
        excelfile = request.files["file"]
        wia_ref_sheets_dict = pd.read_excel(excelfile, sheet_name=None)
        data = wia_ref_sheets_dict["Sheet1"]
        preview_table_data = {"sheet1": {"columns": [], "data": []}}
        # Add columns to the preview_table_data dynamically
        preview_table_data["sheet1"]["columns"] = [
            {"title": col, "key": col.replace(" ", "_")} for col in data.columns
        ]
        # Add data to the preview_table_data
        for _, row in data.iterrows():
            row_data = {}
            for col, value in row.items():
                if isinstance(value, datetime):  # Convert datetime to string
                    value = value.strftime("%Y-%m-%d")
                row_data[col.replace(" ", "_")] = value
            preview_table_data["sheet1"]["data"].append(row_data)
        # Convert preview_table_data to JSON string and then parse it to a dictionary
        response_dict = json.loads(json.dumps(preview_table_data))
        return jsonify(response_dict), 200

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


def save_assets_for_wia_function():
    try:
        data = request.get_json()
        assets_to_save_df = pd.DataFrame(data["selected_assets"])
        save_df = pickle.dumps(assets_to_save_df)
        user_id = 1  # for now basic user_id is 1 will be implemented later
        ref_file_name = "test BB 1"  # basic for now

        wia_ref_sheets = WiaRefSheets(
            user_id=user_id, ref_file_name=ref_file_name, sheet_data=save_df
        )
        db.session.add(wia_ref_sheets)
        db.session.commit()
        db.session.refresh(wia_ref_sheets)
        response = "Assets Saved Sucessfully"
        return jsonify(response)
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


def download_excel_for_assets_function():
    try:
        data = request.get_json()
        uploaded_df = pd.DataFrame(data["assets_to_download"])
        excel_data = BytesIO()
        with ExcelWriter(excel_data, engine="openpyxl") as writer:
            uploaded_df.to_excel(writer, sheet_name="sheet1", index=False)
        # Set the BytesIO stream position to the beginning
        excel_data.seek(0)

        response = make_response(
            send_file(
                excel_data,
                as_attachment=True,
                download_name="assets.xlsx",
                mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        )
        return response
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
def calculate_bb_modified_sheets_function():
    data = request.get_json()
    try:
        request_validation_status = modified_dfs_calculation.validate_request_data(data)
        if request_validation_status:
            return jsonify(request_validation_status), 400

        response_data, updated_df_PL_BB_Output = (
            modified_dfs_calculation.calculate_base_data(data)
        )

        if modified_dfs_calculation.save_response_data(
            data, response_data, updated_df_PL_BB_Output
        ):
            return jsonify({"error_status": False, "message": response_data}), 200
        else:
            return (
                jsonify(
                    {
                        "error_status": False,
                        "message": "Could not calculate borrowing base on modified sheets",
                    }
                ),
                500,
            )

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


def save_what_if_analysis_function():
    try:
        data = request.get_json()
        temporary_what_if_analysis_id = data["temporary_what_if_analysis_id"]
        if not temporary_what_if_analysis_id:
            return jsonify({"error": "Temporary What-if Analysis ID is required"}), 400

        what_if_analysis_type = data["what_if_analysis_type"]
        if not what_if_analysis_type:
            return jsonify({"error": "what_if_analysis_type is required"}), 400

        if what_if_analysis_type == "Update asset":
            modified_base_data_file = ModifiedBaseDataFile.query.filter_by(
                id=temporary_what_if_analysis_id
            ).first()

            note = data.get("note") or None
            simulation_name = (
                data.get("simulation_name") or modified_base_data_file.simulation_name
            )

            modified_base_data_file.note = note
            modified_base_data_file.simulation_name = simulation_name
            modified_base_data_file.is_saved = True

            db.session.add(modified_base_data_file)
            db.session.commit()
            return jsonify({"message": "What-if Analysis updated successfully"}), 200
        else:
            what_if_analysis = WhatIfAnalysis.query.filter_by(
                id=temporary_what_if_analysis_id
            ).first()

            note = data.get("note") or None
            simulation_name = (
                data.get("simulation_name") or what_if_analysis.simulation_name
            )

            what_if_analysis.is_saved = True
            db.session.add(what_if_analysis)
            db.session.commit()

            return jsonify({"message": "What-if Analysis updated successfully"}), 200
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
