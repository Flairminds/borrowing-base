from flask_session import Session
from flask import Flask, request, jsonify, render_template, send_from_directory, session
from flask_cors import CORS


# save to session base files
def save_base_data_files(
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
):
    dataframe_lis = [
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
    ]
    session["base_data_files"] = {}
    for dataframe in dataframe_lis:
        variable_name = [
            name for name, value in locals().items() if value is dataframe
        ][0]
        session["base_data_files"][f"{variable_name}"] = dataframe


# save to session calculated files
def save_calculated_files(
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
):
    session["df_PL_BB_Build"] = df_PL_BB_Build
    session["df_Inputs_Other_Metrics"] = df_Inputs_Other_Metrics
    session["df_Availability_Borrower"] = df_Availability_Borrower
    session["df_PL_BB_Results"] = df_PL_BB_Results
    session["df_subscriptionBB"] = df_subscriptionBB
    session["df_security"] = df_security
    session["df_industry"] = df_industry
    session["df_Input_pricing"] = df_Input_pricing
    session[
        "df_Inputs_Portfolio_LeverageBorrowingBase"
    ] = df_Inputs_Portfolio_LeverageBorrowingBase
    session["df_Obligors_Net_Capital"] = df_Obligors_Net_Capital
    session["df_Inputs_Advance_Rates"] = df_Inputs_Advance_Rates
    session["df_Inputs_Concentration_limit"] = df_Inputs_Concentration_limit
    session["df_principle_obligations"] = df_principle_obligations
    session["df_segmentation_overview"] = df_segmentation_overview


# retrive base data files
def retrive_base_data_files():
    df_PL_BB_Build = session["base_data_files"]["df_PL_BB_Build"]
    df_Inputs_Other_Metrics = session["base_data_files"]["df_Inputs_Other_Metrics"]
    df_Availability_Borrower = session["base_data_files"][
        "df_Availability_Borrower"
    ].copy()
    df_PL_BB_Results = session["base_data_files"]["df_PL_BB_Results"]
    df_subscriptionBB = session["base_data_files"]["df_subscriptionBB"]
    df_security = session["base_data_files"]["df_security"]
    df_industry = session["base_data_files"]["df_industry"]
    df_Input_pricing = session["base_data_files"]["df_Input_pricing"]
    df_Inputs_Portfolio_LeverageBorrowingBase = session["base_data_files"][
        "df_Inputs_Portfolio_LeverageBorrowingBase"
    ]
    df_Obligors_Net_Capital = session["base_data_files"]["df_Obligors_Net_Capital"]
    df_Inputs_Advance_Rates = session["base_data_files"]["df_Inputs_Advance_Rates"]
    df_Inputs_Concentration_limit = session["base_data_files"][
        "df_Inputs_Concentration_limit"
    ]
    df_principle_obligations = session["base_data_files"]["df_principle_obligations"]
    return (
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
