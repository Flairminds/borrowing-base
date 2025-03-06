import pickle
import json
import pandas as pd
from datetime import datetime

from source.services.PFLT.calculation.pflt_borrowing_base import PFLTBorrowingBase as PBC
from source.services.PFLT.WIA import responseGenerator
from source.services.WIA import wiaService
from source.services.PFLT.pflt_utility.constants import sheet_uniques
from source.utility.ServiceResponse import ServiceResponse

def get_parameters(base_data_file, type):
    if type == "Ebitda":
        opposite_type = "Leverage"
        type_col = "Current TTM EBITDA"
        opposite_type_col = "Current Total Debt/EBITDA"
    else:
        opposite_type = "Ebitda"
        type_col = "Current Total Debt/EBITDA"
        opposite_type_col = "Current TTM EBITDA"

    included_assets = json.loads(base_data_file.included_excluded_assets_map)["included_assets"]
    loan_list_df = pickle.loads(base_data_file.file_data)["Loan List"]

    wia_loan_list_df = loan_list_df[loan_list_df.copy()["Security Name"].isin(included_assets)]
    wia_loan_list_df = wia_loan_list_df[["Security Name", type_col, opposite_type_col]]
    wia_loan_list_df = wia_loan_list_df.rename(columns={type_col: type, opposite_type_col: opposite_type})

    response = {}

    columns = [{
        "key": column.replace(" ","_"),
        "label": column
    } for column in wia_loan_list_df.columns.tolist()]

    data = []
    for index, row in wia_loan_list_df.iterrows():
        row_data = {}
        for col, value in row.items():
            if wia_loan_list_df[col].dtypes != "object":
                row_data[col.replace(" ", "_")] = round(value, 2)
            else:
                row_data[col.replace(" ", "_")] = value
        data.append(row_data)

    response["columns"] = columns
    response["data"] = data
    response["identifier"] = sheet_uniques["Loan List"].replace(" ", "_")

    return ServiceResponse.success(data=response, message="Parameters to update")

def update_parameters(base_data_file, type, asset_percent_list):
    if type == "Ebitda":
        opposite_type = "Leverage"
        type_col = "Current TTM EBITDA"
        opposite_type_col = "Current Total Debt/EBITDA"
    else:
        opposite_type = "Ebitda"
        type_col = "Current Total Debt/EBITDA"
        opposite_type_col = "Current TTM EBITDA"

    for asset_percent in asset_percent_list:
        if asset_percent.get("percent"):
            percent = float(asset_percent.get("percent"))
        else:
            percent = float("0")
        asset_percent["percent"] = percent

    asset_percent_df = pd.DataFrame.from_records(asset_percent_list)
    
    xl_sheet_df_map = pickle.loads(base_data_file.file_data)

    loan_list_df = xl_sheet_df_map["Loan List"].copy(deep=True)

    included_assets = json.loads(base_data_file.included_excluded_assets_map)["included_assets"]

    loan_list_df = loan_list_df[loan_list_df["Security Name"].isin(included_assets)]
    initial_loan_list_df = loan_list_df.copy(deep=True)

    loan_list_df["debt"] = (loan_list_df["Current TTM EBITDA"] * loan_list_df["Current Total Debt/EBITDA"])
    loan_list_df[type_col] = loan_list_df[type_col] * (1 + asset_percent_df["percent"] / 100)
    
    loan_list_df[opposite_type_col] = (loan_list_df["debt"] / loan_list_df[opposite_type_col])
    loan_list_df = loan_list_df.reset_index()

    loan_list_df = loan_list_df.reset_index(drop=True)

    modified_loan_list_df = loan_list_df.copy(deep=True)

    xl_sheet_df_map["Loan List"] = loan_list_df

    pbc = PBC(file_df=xl_sheet_df_map)
    pbc.calculate()

    initial_xl_df_map = pickle.loads(base_data_file.intermediate_calculation)
    calculated_xl_df_map = pbc.file_df
    response = responseGenerator.generateResponse(initial_xl_df_map, calculated_xl_df_map)

    response["what_if_analysis_type"] = "add_asset"
    response["closing_date"] = base_data_file.closing_date.strftime("%Y-%m-%d")
    response["what_if_analysis_type"] = "add_asset"

    simulation_name = "update_parameter_" + datetime.now().strftime("%Y-%b-%d . %H : %M : %S")
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
        simulation_type="change_"+type,
    )

    if not what_if_analysis_result["error"]:
        response["what_if_analysis_id"] = what_if_analysis_result["what_if_analysis"].id
    return response