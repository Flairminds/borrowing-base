import json


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


def read_excels(tables_dict):
    df_PL_BB_Build = tables_dict["PL BB Build"]
    df_Inputs_Other_Metrics = tables_dict["Other Metrics"]
    df_Availability_Borrower = tables_dict["Availability Borrower"]
    df_PL_BB_Results = tables_dict["PL BB Results"]
    df_subscriptionBB = tables_dict["Subscription BB"]
    df_security = tables_dict["PL_BB_Results_Security"]
    df_industry = tables_dict["Inputs Industries"]
    df_Input_pricing = tables_dict["Pricing"]
    df_Inputs_Portfolio_LeverageBorrowingBase = tables_dict[
        "Portfolio LeverageBorrowingBase"
    ]
    df_Obligors_Net_Capital = tables_dict["Obligors' Net Capital"]
    df_Inputs_Advance_Rates = tables_dict["Advance Rates"]
    df_Inputs_Concentration_limit = tables_dict["Concentration Limits"]
    df_principle_obligations = tables_dict["Principle Obligations"]

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


def get_eligible_funds(df_PL_BB_Build):
    eligible_assets_mask = df_PL_BB_Build["Is Eligible Issuer"] == "Yes"
    return df_PL_BB_Build[eligible_assets_mask]["Investment Name"].tolist()
