from functionsCall import functions_call_calculation, read_excels
from response import formatted_data


def calculate_borrowing_base(xl_sheet_df_map):
    df_PL_BB_Build, df_Inputs_Other_Metrics, df_Availability_Borrower, df_PL_BB_Results, df_subscriptionBB, df_security, df_industry, df_Input_pricing, df_Inputs_Portfolio_LeverageBorrowingBase, df_Obligors_Net_Capital,  df_Inputs_Advance_Rates, df_Inputs_Concentration_limit, df_principle_obligations = read_excels(xl_sheet_df_map)

    df_PL_BB_Build, df_Inputs_Other_Metrics, df_Availability_Borrower, df_PL_BB_Results,df_subscriptionBB,df_security,df_industry,df_Input_pricing,df_Inputs_Portfolio_LeverageBorrowingBase,df_Obligors_Net_Capital,df_Inputs_Advance_Rates,df_Inputs_Concentration_limit,df_principle_obligations,df_segmentation_overview, df_PL_BB_Output = functions_call_calculation(df_PL_BB_Build, df_Inputs_Other_Metrics, df_Availability_Borrower, df_PL_BB_Results,df_subscriptionBB,df_security,df_industry,df_Input_pricing,df_Inputs_Portfolio_LeverageBorrowingBase,df_Obligors_Net_Capital,df_Inputs_Advance_Rates,df_Inputs_Concentration_limit,df_principle_obligations)

    card_data, segmentation_Overview_data, security_data, concentration_Test_data, principal_obligation_data , segmentation_chart_data, security_chart_data = formatted_data(df_PL_BB_Results, df_security, df_segmentation_overview, df_principle_obligations,df_Availability_Borrower)

    response_data = {
                "card_data": card_data,
                "segmentation_overview_data": segmentation_Overview_data,
                "security_data": security_data,
                "concentration_test_data": concentration_Test_data,
                "principal_obligation_data": principal_obligation_data,
                "segmentation_chart_data" : segmentation_chart_data,
                "security_chart_data" : security_chart_data
            }
    return response_data