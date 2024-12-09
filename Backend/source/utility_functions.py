import sys
import pathlib
source_dir = pathlib.Path().absolute() / "source"
sys.path.append(str(source_dir))
from flask_cors import CORS
import pandas as pd
from functionsCall import *
from WIA_API import *
import pathlib
import json
# from std_file_formater import find_file_format_change, rename_columns#, rename_sheets
from response import *
from session_files import *
from models import *

import pickle

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
    response_data, simulation_name, base_data_file, note, selected_assets_df
):
    try:
        pickled_response_data = pickle.dumps(response_data)

        what_if_analysis = WhatIfAnalysis(
            base_data_file_id=base_data_file.id,
            simulation_name=simulation_name,
            response=pickled_response_data,
            note=note,
            selected_assets=pickle.dumps(selected_assets_df),
        )

        db.session.add(what_if_analysis)
        db.session.commit()
        db.session.refresh(what_if_analysis)
        return {"error": False, "what_if_analysis": what_if_analysis}
    except Exception as e:
        print(str(e))
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

def convert_to_table(selected_assets):
    selected_assets.fillna("", inplace=True)
    selected_WIA_asstes_table_data = {"sheet1": {"columns": [], "data": []}}
    # Add columns to the preview_table_data dynamically
    selected_WIA_asstes_table_data["sheet1"]["columns"] = [
        {"title": col, "key": col.replace(" ", "_")} for col in selected_assets.columns
    ]
    # Add data to the preview_table_data
    for _, row in selected_assets.iterrows():
        row_data = {}
        for col, value in row.items():
            if isinstance(value, (int, float)):
                if col in [
                    "Rates Current LIBOR/Floor",
                    "Rates Fixed Coupon",
                    "Rates Floating Cash Spread",
                    "Leverage LTV Thru PCOF IV",
                ]:
                    row_data[col.replace(" ", "_")] = "{:,.01f}%".format(value * 100)
                elif col in [
                    "Financials LTM Revenue ($MMs)",
                    "Financials LTM EBITDA ($MMs)",
                    "Leverage Revolver Commitment",
                    "Leverage Total Enterprise Value",
                    "Leverage Total Leverage",
                    "Leverage PCOF IV Leverage",
                    "Leverage Attachment Point",
                ]:
                    row_data[col.replace(" ", "_")] = numerize.numerize(value, 2)
                else:
                    row_data[col.replace(" ", "_")] = numerize.numerize(value, 2)
            elif isinstance(value, datetime):
                row_data[col.replace(" ", "_")] = value.strftime("%Y-%m-%d")
            else:
                row_data[col.replace(" ", "_")] = value
        selected_WIA_asstes_table_data["sheet1"]["data"].append(row_data)
    return selected_WIA_asstes_table_data

