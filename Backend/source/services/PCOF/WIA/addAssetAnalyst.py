import pickle
import json
import pandas as pd
from datetime import datetime
from flask import jsonify

from source.services.PCOF import utility as pcofUtility
from source.services.PCOF.calculation.functionsCall import calculate_bb
from source.services.PCOF.WIA import responseGenerator
from source.services.PCOF.WIA import responseGenerator2
from source.services.WIA import wiaService


def add_asset(base_data_file, selected_assets):
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

    intermediate_calculation = pickle.loads(base_data_file.intermediate_calculation)

    initial_segmentation_overview_df = intermediate_calculation[
        "df_segmentation_overview"
    ]
    initial_security_df = intermediate_calculation["df_security"]

    df_PL_BB_Build = df_PL_BB_Build[
        df_PL_BB_Build["Investment Name"].isin(
            pcofUtility.get_eligible_funds(df_PL_BB_Build)
        )
    ]

    included_assets = json.loads(base_data_file.included_excluded_assets_map)[
        "included_assets"
    ]

    df_PL_BB_Build = df_PL_BB_Build[df_PL_BB_Build["Investment Name"].isin(included_assets)].reset_index(drop=True)
    initial_pl_bb_build = df_PL_BB_Build.copy(deep=True)

    uploaded_df = pd.DataFrame(selected_assets)
    uploaded_df.columns = uploaded_df.columns.str.replace("_", " ").str.title()
    uploaded_df = uploaded_df.reindex(columns=df_PL_BB_Build.columns)
    # Concatenate df_PL_BB_Build and uploaded_df
    df_PL_BB_Build = pd.concat([df_PL_BB_Build, uploaded_df], ignore_index=True)
    modified_pl_bb_build = df_PL_BB_Build.copy(deep=True)

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
    )= responseGenerator2.generate_response(initial_xl_df_map=initial_xl_df_map, calculated_xl_df_map=calculated_xl_df_map)
    # merged_segmentation_overview, merged_df_security = (
    #     responseGenerator.sheets_for_whatif_analysis(
    #         initial_segmentation_overview_df,
    #         initial_security_df,
    #         Updated_df_segmentation_overview,
    #         Updated_df_security,
    #     )
    # )

    # calculated_df_Availability_Borrower = intermediate_calculation[
    #     "df_Availability_Borrower"
    # ]

    # (
    #     card_data,
    #     segmentation_overview_data,
    #     security_data,
    #     concentration_Test_data,
    #     principal_obligation_data,
    #     segmentation_chart_data,
    #     security_chart_data,
    # ) = responseGenerator.generate_response(
    #     merged_segmentation_overview,
    #     merged_df_security,
    #     Updated_df_PL_BB_Results,
    #     df_principle_obligations,
    #     calculated_df_Availability_Borrower,
    #     Updated_df_Availability_Borrower,
    # )
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
    simulation_name = "add_asset_" + datetime.now().strftime("%Y-%b-%d . %H : %M : %S")
    note = None
    intermediate_metrics_data["modified_df_PL_BB_Output"] = df_PL_BB_Output
    initial_data = {"PL BB Build": initial_pl_bb_build}
    updated_data = {"PL BB Build": modified_pl_bb_build}
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
        simulation_type="add_asset",
        intermediate_calculation = calculated_xl_df_map
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
