import pickle


from functionsCall import functions_call_calculation, read_excels
import response
import app
from models import ModifiedBaseDataFile, BaseDataFile


def calculate_base_data(data):
    modified_base_data_file_id = data.get("modified_base_data_file_id")
    if not modified_base_data_file_id:
        return {"error_status": True, "message": "base_data_file_id is required"}

    modified_base_data_file = ModifiedBaseDataFile.query.filter_by(
        id=modified_base_data_file_id
    ).first()

    base_data_file = BaseDataFile.query.filter_by(
        id=modified_base_data_file.base_data_file_id
    ).first()

    base_data_file_data = pickle.loads(base_data_file.file_data)
    intermediate_calculation = pickle.loads(base_data_file.intermediate_calculation)

    modified_xl_df_map = pickle.loads(modified_base_data_file.modified_data)

    new_modified_xl_df_map = base_data_file_data
    for sheet_name in modified_xl_df_map.keys():
        new_modified_xl_df_map[sheet_name] = modified_xl_df_map[sheet_name]

    df_segmentation_overview = intermediate_calculation["df_segmentation_overview"]
    previous_security = intermediate_calculation["df_security"]
    calc_df_Availability_Borrower = intermediate_calculation["df_Availability_Borrower"]

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
    ) = calculate_borrowing_base(new_modified_xl_df_map)

    merged_segmentation_overview, merged_df_security = (
        response.sheets_for_whatif_analysis(
            df_segmentation_overview,
            previous_security,
            Updated_df_segmentation_overview,
            Updated_df_security,
        )
    )

    (
        card_data,
        segmentation_overview_data,
        security_data,
        concentration_Test_data,
        principal_obligation_data,
        segmentation_chart_data,
        security_chart_data,
    ) = response.formated_response_whatif_analysis(
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

    return response_data, df_PL_BB_Output


def calculate_borrowing_base(xl_sheet_df_map):
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

    return (
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
    )


def save_response_data(data, response_data, updated_df_PL_BB_Output):
    try:
        db = app.db
        modified_base_data_file_id = data.get("modified_base_data_file_id")
        if not modified_base_data_file_id:
            return {"error_status": True, "message": "base_data_file_id is required"}

        modified_base_data_file = ModifiedBaseDataFile.query.filter_by(
            id=modified_base_data_file_id
        ).first()

        base_data_file = BaseDataFile.query.filter_by(
            id=modified_base_data_file.base_data_file_id
        ).first()
        intermediate_calculation = pickle.loads(base_data_file.intermediate_calculation)
        initial_df_PL_BB_Output = intermediate_calculation["df_PL_BB_Output"]

        intermediate_metrics_data = {
            "inital_df_PL_BB_Output": initial_df_PL_BB_Output,
            "modified_df_PL_BB_Output": updated_df_PL_BB_Output,
        }

        modified_base_data_file.response = response_data
        modified_base_data_file.intermediate_metrics_data = intermediate_metrics_data

        db.session.add(modified_base_data_file)
        db.session.commit()

        return True
    except Exception as e:
        return False
