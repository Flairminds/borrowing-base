import json
import pickle
import pandas as pd
from datetime import datetime
from flask import jsonify

from source.services.PFLT.calculation.pflt_borrowing_base import (
    PFLTBorrowingBase as PBC,
)
from source.services.PFLT.WIA import responseGenerator
from source.services.WIA import wiaService


def add_asset(base_data_file, selected_assets):
    xl_sheet_df_map = pickle.loads(base_data_file.file_data)

    loan_list_df = xl_sheet_df_map["Loan List"].copy(deep=True)

    included_assets = json.loads(base_data_file.included_excluded_assets_map)[
        "included_assets"
    ]

    loan_list_df = loan_list_df[loan_list_df["Security Name"].isin(included_assets)]
    initial_loan_list_df = loan_list_df.copy(deep=True)

    uploaded_df = pd.DataFrame(selected_assets)
    uploaded_df.columns = uploaded_df.columns.str.replace("_", " ")
    uploaded_df = uploaded_df.reindex(columns=loan_list_df.columns)

    loan_list_df = pd.concat([loan_list_df, uploaded_df], ignore_index=True)
    loan_list_df = loan_list_df.reset_index(drop=True)

    modified_loan_list_df = loan_list_df.copy(deep=True)

    xl_sheet_df_map["Loan List"] = loan_list_df

    pbc = PBC(file_df=xl_sheet_df_map)
    pbc.calculate()

    initial_xl_df_map = pickle.loads(base_data_file.intermediate_calculation)
    calculated_xl_df_map = pbc.file_df
    response = responseGenerator.generateResponse(
        initial_xl_df_map, calculated_xl_df_map
    )
    response["what_if_analysis_type"] = "add_asset"
    response["closing_date"] = base_data_file.closing_date.strftime("%Y-%m-%d")
    response["what_if_analysis_type"] = "add_asset"

    simulation_name = "add_asset_" + datetime.now().strftime("%Y-%b-%d . %H : %M : %S")
    note = None
    initial_data = {"Loan List": initial_loan_list_df}
    updated_data = {"Loan List": modified_loan_list_df}
    intermediate_metrics_data = {}

    what_if_analysis_result = wiaService.save_what_if_analysis(
        base_data_file_id=base_data_file.id,
        simulation_name=simulation_name,
        initial_data=initial_data,
        updated_data=updated_data,
        intermediate_metrics_data=intermediate_metrics_data,
        response=response,
        note=note,
        is_saved=False,
        simulation_type="add_asset",
        intermediate_calculation=calculated_xl_df_map
    )

    if not what_if_analysis_result["error"]:
        response["what_if_analysis_id"] = what_if_analysis_result["what_if_analysis"].id
    return jsonify(response), 200
