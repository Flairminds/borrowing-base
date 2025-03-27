import pickle
import json
import pandas as pd
from datetime import datetime

from source.services.PCOF import utility as pcofUtility
from source.services.PCOF.calculation.functionsCall import calculate_bb
from source.services.PCOF.WIA import responseGenerator2
from source.services.WIA import wiaService
from source.utility.ServiceResponse import ServiceResponse

def get_parameters(base_data_file, type):
    intermediate_calculation = pickle.loads(base_data_file.intermediate_calculation)
    df_PL_BB_Build = intermediate_calculation["df_PL_BB_Build"].copy(deep=True)

    if type == "Ebitda":
        opposite_type = "Leverage"
        type_col = "Financials LTM EBITDA ($MMs)"
        opposite_type_col = "Leverage Total Leverage"
    else:
        opposite_type = "Ebitda"
        type_col = "Leverage Total Leverage"
        opposite_type_col = "Financials LTM EBITDA ($MMs)"

    included_assets = json.loads(base_data_file.included_excluded_assets_map)["included_assets"]
    selected_assets_mask = df_PL_BB_Build["Investment Name"].isin(included_assets)
    wia_df_PL_BB_Build = df_PL_BB_Build[selected_assets_mask]

    wia_df_PL_BB_Build = wia_df_PL_BB_Build.rename(columns={type_col: type, opposite_type_col: opposite_type})

    wia_df_PL_BB_Build = wia_df_PL_BB_Build[["Investment Name", type, opposite_type]]

    wia_df_PL_BB_Build[[type, opposite_type]] = wia_df_PL_BB_Build[[type, opposite_type]].fillna(0)

    response = {}

    columns = [{
        "key": column.replace(" ","_"),
        "label": "Ebitda ($MMs)" if column == "Ebitda" else column
    } for column in wia_df_PL_BB_Build.columns.tolist()]

    data = []
    for index, row in wia_df_PL_BB_Build.iterrows():
        row_data = {}
        for col, value in row.items():
            if wia_df_PL_BB_Build[col].dtypes != "object":
                row_data[col.replace(" ", "_")] = round(value, 2)
            else:
                row_data[col.replace(" ", "_")] = value
        data.append(row_data)

    response["columns"] = columns
    response["data"] = data
    response["identifier"] = "Investment_Name"

    return ServiceResponse.success(data=response, message="Parameters to update")

def update_parameters(base_data_file, type, asset_percent_list):
    if type == "Ebitda":
        opposite_type = "Leverage"
        type_col = "Financials LTM EBITDA ($MMs)"
        opposite_type_col = "Leverage Total Leverage"
    else:
        opposite_type = "Ebitda"
        type_col = "Leverage Total Leverage"
        opposite_type_col = "Financials LTM EBITDA ($MMs)"
    
    for asset_percent in asset_percent_list:
        if asset_percent.get("percent"):
            percent = float(asset_percent.get("percent"))
        else:
            percent = float("0")
        asset_percent["percent"] = percent

    asset_percent_df = pd.DataFrame.from_records(asset_percent_list)
    asset_percent_df['Ebitda'] = pd.to_numeric(asset_percent_df['Ebitda'], errors='coerce')
    asset_percent_df['Leverage'] = pd.to_numeric(asset_percent_df['Leverage'], errors='coerce')

    xl_sheet_df_map = pickle.loads(base_data_file.file_data)
    
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
    ) = pcofUtility.read_excels(xl_sheet_df_map)
    selected_assets = json.loads(base_data_file.included_excluded_assets_map)["included_assets"]

    df_PL_BB_Build = df_PL_BB_Build.copy()
    
    # get eligible and included assets
    original_pl_bb_build = df_PL_BB_Build.copy()
    df_PL_BB_Build = df_PL_BB_Build[df_PL_BB_Build["Is Eligible Issuer"] == "Yes"]
    selected_assets_mask = df_PL_BB_Build["Investment Name"].isin(selected_assets)
    df_PL_BB_Build = df_PL_BB_Build[selected_assets_mask].reset_index(drop=True)
    if "Cash" in df_PL_BB_Build["Investment Name"].tolist():
        df_PL_BB_Build = df_PL_BB_Build.append(original_pl_bb_build[original_pl_bb_build['Investment Name'] == 'Cash'])
    
    initial_pl_bb_build = df_PL_BB_Build.copy(deep=True)

    df_PL_BB_Build[['Financials LTM EBITDA ($MMs)', 'Leverage Total Leverage']] = df_PL_BB_Build[['Financials LTM EBITDA ($MMs)', 'Leverage Total Leverage']].fillna(0)

    df_PL_BB_Build['Financials LTM EBITDA ($MMs)'] = pd.to_numeric(df_PL_BB_Build['Financials LTM EBITDA ($MMs)'], errors='coerce')
    df_PL_BB_Build['Leverage Total Leverage'] = pd.to_numeric(df_PL_BB_Build['Leverage Total Leverage'], errors='coerce')

    df_PL_BB_Build["debt"] = (df_PL_BB_Build["Financials LTM EBITDA ($MMs)"] * df_PL_BB_Build["Leverage Total Leverage"])
    df_PL_BB_Build[type_col] = asset_percent_df[type] * (1 + asset_percent_df["percent"] / 100)
    
    df_PL_BB_Build[opposite_type_col] = (df_PL_BB_Build["debt"] / df_PL_BB_Build[opposite_type_col])
    df_PL_BB_Build = df_PL_BB_Build.reset_index()
    midified_df_PL_BB_Build = df_PL_BB_Build.copy(deep=True)

    intermediate_calculation = pickle.loads(base_data_file.intermediate_calculation)
    intermediate_metrics_data = {
        "inital_df_PL_BB_Output": intermediate_calculation["df_PL_BB_Output"]
    }

    (
        df_PL_BB_Build,
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
    ) = calculate_bb(
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

    initial_xl_df_map = pickle.loads(base_data_file.intermediate_calculation)
    calculated_xl_df_map = {
        "df_PL_BB_Build": df_PL_BB_Build,
        "df_Inputs_Other_Metrics": df_Inputs_Other_Metrics,
        "Updated_df_Availability_Borrower": Updated_df_Availability_Borrower,
        "Updated_df_PL_BB_Results": Updated_df_PL_BB_Results,
        "df_subscriptionBB": df_subscriptionBB,
        "Updated_df_security": Updated_df_security,
        "df_industry": df_industry,
        "df_Input_pricing": df_Input_pricing,
        "df_Inputs_Portfolio_LeverageBorrowingBase": df_Inputs_Portfolio_LeverageBorrowingBase,
        "df_Obligors_Net_Capital": df_Obligors_Net_Capital,
        "df_Inputs_Advance_Rates": df_Inputs_Advance_Rates,
        "df_Inputs_Concentration_limit": df_Inputs_Concentration_limit,
        "df_principle_obligations": df_principle_obligations,
        "Updated_df_segmentation_overview": Updated_df_segmentation_overview,
        "df_PL_BB_Output": df_PL_BB_Output
    }

    (
        card_data,
        segmentation_overview_data,
        security_data,
        concentration_Test_data,
        principal_obligation_data,
        segmentation_chart_data,
        security_chart_data 
    ) = responseGenerator2.generate_response(initial_xl_df_map=initial_xl_df_map, calculated_xl_df_map=calculated_xl_df_map)

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
    simulation_name = "update_parameter_" + datetime.now().strftime("%Y-%b-%d . %H : %M : %S")
    note = None
    
    intermediate_metrics_data["modified_df_PL_BB_Output"] = df_PL_BB_Output
    initial_data = {"PL BB Build": initial_pl_bb_build}
    updated_data = {"PL BB Build": midified_df_PL_BB_Build}
    base_data_file_id = base_data_file.id

    what_if_analysis_result = wiaService.save_what_if_analysis(
        base_data_file_id=base_data_file_id,
        simulation_name=simulation_name,
        initial_data=initial_data,
        updated_data=updated_data,
        intermediate_metrics_data=intermediate_metrics_data,
        response=response_data,
        note=note,
        is_saved=False,
        simulation_type="change_" + type,
        intermediate_calculation=calculated_xl_df_map
    )

    if not what_if_analysis_result["error"]:
        response_data["what_if_analysis_id"] = what_if_analysis_result[
            "what_if_analysis"
        ].id
        response_data["what_if_analysis_type"] = what_if_analysis_result[
            "what_if_analysis"
        ].simulation_type
        return response_data
    else:
        raise Exception("Could not add assets")