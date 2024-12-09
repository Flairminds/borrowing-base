import pandas as pd
from numerize import numerize

from concentration_test_application import ConcentraionTestFormatter


def number_formatting_for_availablity(df_Availability_Borrower):
    df_Availability_Borrower.fillna(0, inplace=True)

    def convert_to_numeric(value):
        if isinstance(value, str):
            # Remove any non-numeric characters before converting to float
            value = float(value.replace(",", "").replace("$", "").replace("%", ""))
        return value

    df_Availability_Borrower.at[1, "B"] = str(
        pd.to_datetime(df_Availability_Borrower.at[1, "B"]).date()
    )
    df_Availability_Borrower.at[2, "B"] = str(
        pd.to_datetime(df_Availability_Borrower.at[2, "B"]).date()
    )

    for index in [4, 5, 6, 7, 8, 9, 12, 13, 16, 17, 18, 19, 22]:
        df_Availability_Borrower.at[index, "B"] = "$" + numerize.numerize(
            convert_to_numeric(df_Availability_Borrower.at[index, "B"])
        )

    for index in [10, 14, 15, 20, 21]:
        df_Availability_Borrower.at[index, "B"] = "{:,.01f}%".format(
            convert_to_numeric(df_Availability_Borrower.at[index, "B"]) * 100
        )

    return df_Availability_Borrower


def number_formatting_for_concentration(df):
    rows_to_keep = [
        "Min. Eligible Issuers (#)",
        "8 or 9 Issuers?",
        "Max. Weighted Average Maturity (Years)",
        "Max. Weighted Average Leverage thru Borrower",
    ]
    # Create a mask to identify rows to convert
    mask = ~df["Concentration Tests"].isin(rows_to_keep)
    # Convert values to percentages for relevant rows
    # df.loc[mask, "Concentration Limit"] = (
    #     df.loc[mask, "Concentration Limit"] * 100
    # ).map("{:.0f}%".format)
    df["Actual"].fillna(0, inplace=True)
    # df.loc[mask, "Actual"] = (df.loc[mask, "Actual"] * 100).map("{:.0f}%".format)
    df = df.applymap(
        lambda x: x if isinstance(x, (float, int)) and x is not None else x
    )
    return df

    # Clean column names (strip leading/trailing spaces) and fill NaN values with 0


def clean_data(
    df_PL_BB_Results,
    df_security,
    df_segmentation_overview,
    df_principle_obligations,
    df_Availability_Borrower,
):
    df_PL_BB_Results = df_PL_BB_Results.copy().fillna(0)
    df_security = df_security.copy().fillna(0)
    df_segmentation_overview = df_segmentation_overview.copy().fillna(0)
    df_principle_obligations = df_principle_obligations.copy().fillna(0)
    df_Availability_Borrower = df_Availability_Borrower.copy().fillna(0)
    df_PL_BB_Results.columns = df_PL_BB_Results.columns.str.strip()
    df_security.columns = df_security.columns.str.strip()
    df_segmentation_overview.columns = df_segmentation_overview.columns.str.strip()
    df_principle_obligations.columns = df_principle_obligations.columns.str.strip()
    df_Availability_Borrower.columns = df_Availability_Borrower.columns.str.strip()
    return (
        df_PL_BB_Results,
        df_security,
        df_segmentation_overview,
        df_principle_obligations,
        df_Availability_Borrower,
    )


def data_for_graphs(df_security, df_segmentation_overview):
    df_seg = df_segmentation_overview.sort_values(by=["BB"], ascending=False)
    df_segmentation_overview_for_chart = df_seg[df_seg["BB"] != 0]
    df_sec = df_security.sort_values(by=["Security BB"], ascending=False)
    df_security_for_chart = df_sec[df_sec["Security BB"] != 0]
    unadjusted_BB_for_chart = (
        df_segmentation_overview_for_chart["BB"].iloc[1:11]
    ).tolist()
    name_of_industry = (
        df_segmentation_overview_for_chart["industry"].iloc[1:11]
    ).tolist()
    BB_for_chart = df_security_for_chart["Security BB"].tolist()
    name_of_security = df_security_for_chart["Security"].tolist()
    return unadjusted_BB_for_chart, name_of_industry, BB_for_chart, name_of_security

    # Extract relevant information


def required_data(
    df_PL_BB_Results, df_security, df_segmentation_overview, df_principle_obligations
):
    industry = df_segmentation_overview["industry"].tolist()
    unadjusted_BB = df_segmentation_overview["BB"].tolist()
    percent_of_unadjusted_BB = df_segmentation_overview["percent of BB"].tolist()
    security = df_security["Security"].tolist()
    BB = df_security["Security BB"].tolist()
    percent_of_BB = df_security["Security Percent of BB"].tolist()
    concentration_tests = df_PL_BB_Results["Concentration Tests"].tolist()
    concentration_limits = df_PL_BB_Results["Concentration Limit"].tolist()
    actual_values = df_PL_BB_Results["Actual"].tolist()
    obligations = df_principle_obligations["Principal Obligations"].tolist()
    currency = df_principle_obligations["Currency"].tolist()
    amount = df_principle_obligations["Amount"].tolist()
    spotrate = df_principle_obligations["Spot Rate"].tolist()
    dollarequivalent = df_principle_obligations["Dollar Equivalent"].tolist()
    unadjusted_BB_for_chart = sorted(unadjusted_BB, reverse=True)[:10]
    (
        unadjusted_BB_for_chart,
        name_of_industry,
        BB_for_chart,
        name_of_security,
    ) = data_for_graphs(df_security, df_segmentation_overview)
    pass_list = df_PL_BB_Results["Result"].tolist()
    return (
        industry,
        unadjusted_BB,
        percent_of_unadjusted_BB,
        security,
        BB,
        percent_of_BB,
        concentration_tests,
        concentration_limits,
        actual_values,
        obligations,
        currency,
        amount,
        spotrate,
        dollarequivalent,
        unadjusted_BB_for_chart,
        name_of_industry,
        BB_for_chart,
        name_of_security,
        pass_list,
    )


def generating_data_in_required_format_for_result(
    df_Availability_Borrower,
    industry,
    unadjusted_BB,
    percent_of_unadjusted_BB,
    security,
    BB,
    percent_of_BB,
    concentration_tests,
    concentration_limits,
    actual_values,
    obligations,
    currency,
    amount,
    spotrate,
    dollarequivalent,
    unadjusted_BB_for_chart,
    name_of_industry,
    BB_for_chart,
    name_of_security,
    pass_list,
):
    # Extracting specific rows from df_Availability_Borrower for card data
    card_data = {
        "Total BB": [{"data": (df_Availability_Borrower.loc[17, "B"])}],
        "Leverage BB": [{"data": (df_Availability_Borrower.loc[16, "B"])}],
        "Subscription BB": [{"data": (df_Availability_Borrower.loc[9, "B"])}],
        "Availability": [{"data": (df_Availability_Borrower.loc[22, "B"])}],
        "Obligors net capital": [
            {"data": "$" + numerize.numerize(round(dollarequivalent[0], 2))}
        ],
        "ordered_card_names": [
            "Total BB",
            "Leverage BB",
            "Subscription BB",
            "Availability",
            "Obligors net capital",
        ],
    }

    # Create required format for segmentation overview data
    segmentation_data = {
        "Industry": industry,
        "Unadjusted BB": unadjusted_BB,
        "Unadjusted % of BB": percent_of_unadjusted_BB,
    }
    segmentation_df = pd.DataFrame(segmentation_data)
    segmentation_df = segmentation_df.sort_values("Unadjusted BB", ascending=False)
    segmentation_df = segmentation_df[segmentation_df["Industry"] != "Total"]
    segmentation_Overview_data = {
        "columns": [{"data": ["Industry", "Unadjusted BB", "Unadjusted % of BB"]}],
        "Industry": [{"data": val} for val in segmentation_df["Industry"]],
        "Unadjusted BB": [
            {"data": "$" + numerize.numerize(val)}
            for val in segmentation_df["Unadjusted BB"]
        ],
        "Unadjusted % of BB": [
            {"data": "{:.2f}%".format(val * 100)}
            for val in segmentation_df["Unadjusted % of BB"]
        ],
        "Total": {
            "data": {
                "Industry": industry[-1],
                "Unadjusted BB": "$" + numerize.numerize(unadjusted_BB[-1]),
                "Unadjusted % of BB": "{:.2f}%".format(
                    percent_of_unadjusted_BB[-1] * 100
                ),
            }
        },
    }

    # Create required format for security data
    security_df_data = {"Security": security, "BB": BB, "% of BB": percent_of_BB}
    security_df = pd.DataFrame(security_df_data)
    security_df = security_df.sort_values("BB", ascending=False)
    security_df = security_df[security_df["Security"] != "Total"]
    security_data = {
        "columns": [{"data": ["Security", "BB", "% of BB"]}],
        "Security": [{"data": val} for val in security_df["Security"]],
        "BB": [{"data": "$" + numerize.numerize(val)} for val in security_df["BB"]],
        "% of BB": [
            {"data": "{:.2f}%".format(val * 100)} for val in security_df["% of BB"]
        ],
        "Total": {
            "data": {
                "Security": security[-1],
                "BB": "$" + numerize.numerize(security_df["BB"].sum()),
                "% of BB": "{:.2f}%".format(security_df["% of BB"].sum() * 100),
            }
        },
    }

    # Create required format for concentration test data
    concentration_Test_df = pd.DataFrame(
        {
            "Concentration Tests": concentration_tests,
            "Concentration Limit": concentration_limits,
            "Actual": actual_values,
            "Result": pass_list,
        }
    )
    concentraion_test_formatter = ConcentraionTestFormatter(concentration_Test_df)
    concentration_Test_data = concentraion_test_formatter.convert_to_std_table_format()
    # concentration_Test_data = {
    #     "columns": [
    #         {"data": ["Concentration Test", "Concentration Limit", "Actual", "Result"]}
    #     ],
    #     "Concentration Test": [{"data": val} for val in concentration_tests],
    #     "Concentration Limit": [{"data": (val)} for val in concentration_limits],
    #     "Actual": [{"data": (val)} for val in actual_values],
    #     "Result": [{"data": (val)} for val in pass_list],
    # }

    # Create required format for principal obligation data
    principal_obligation_data = {
        "columns": [
            {
                "data": [
                    "Obligation",
                    "Currency",
                    "Amount",
                    "Spot rate",
                    "Dollar equivalent",
                ]
            }
        ],
        "Obligation": [{"data": val} for val in obligations],
        "Currency": [{"data": val} for val in currency],
        "Amount": [{"data": "$" + numerize.numerize(val)} for val in amount],
        "Spot rate": [{"data": "{:.2f}%".format(val * 100)} for val in spotrate],
        "Dollar equivalent": [
            {"data": "$" + numerize.numerize(val)} for val in dollarequivalent
        ],
    }

    # Create required format for chart data
    segmentation_chart_data = {
        "segmentation_chart_data": [
            {"name": name, "Unadjusted BB": val}
            for name, val in zip(name_of_industry, unadjusted_BB_for_chart)
        ],
        "y_axis": "name",
        "x_axis": ["Unadjusted BB"],
    }

    security_chart_data = {
        "security_chart_data": [
            {"name": name, "BB": val}
            for name, val in zip(name_of_security, BB_for_chart)
        ],
        "x_axis": ["BB"],
        "y_axis": "name",
    }

    return (
        card_data,
        segmentation_Overview_data,
        security_data,
        concentration_Test_data,
        principal_obligation_data,
        segmentation_chart_data,
        security_chart_data,
    )


def formatted_data(
    df_PL_BB_Results,
    df_security,
    df_segmentation_overview,
    df_principle_obligations,
    df_Availability_Borrower,
):
    # Clean column names (strip leading/trailing spaces) and fill NaN values with 0
    (
        df_PL_BB_Results,
        df_security,
        df_segmentation_overview,
        df_principle_obligations,
        df_Availability_Borrower,
    ) = clean_data(
        df_PL_BB_Results,
        df_security,
        df_segmentation_overview,
        df_principle_obligations,
        df_Availability_Borrower,
    )
    df_Availability_Borrower = number_formatting_for_availablity(
        df_Availability_Borrower
    )
    df_PL_BB_Results = number_formatting_for_concentration(df_PL_BB_Results)
    # Extract relevant information
    (
        industry,
        unadjusted_BB,
        percent_of_unadjusted_BB,
        security,
        BB,
        percent_of_BB,
        concentration_tests,
        concentration_limits,
        actual_values,
        obligations,
        currency,
        amount,
        spotrate,
        dollarequivalent,
        unadjusted_BB_for_chart,
        name_of_industry,
        BB_for_chart,
        name_of_security,
        pass_list,
    ) = required_data(
        df_PL_BB_Results,
        df_security,
        df_segmentation_overview,
        df_principle_obligations,
    )  # generating_data_in_required_format_for_result
    (
        card_data,
        segmentation_Overview_data,
        security_data,
        concentration_Test_data,
        principal_obligation_data,
        segmentation_chart_data,
        security_chart_data,
    ) = generating_data_in_required_format_for_result(
        df_Availability_Borrower,
        industry,
        unadjusted_BB,
        percent_of_unadjusted_BB,
        security,
        BB,
        percent_of_BB,
        concentration_tests,
        concentration_limits,
        actual_values,
        obligations,
        currency,
        amount,
        spotrate,
        dollarequivalent,
        unadjusted_BB_for_chart,
        name_of_industry,
        BB_for_chart,
        name_of_security,
        pass_list,
    )
    return (
        card_data,
        segmentation_Overview_data,
        security_data,
        concentration_Test_data,
        principal_obligation_data,
        segmentation_chart_data,
        security_chart_data,
    )


def sheets_for_whatif_analysis(
    df_segmentation_overview,
    previous_security,
    Updated_df_segmentation_overview,
    Updated_df_security,
):
    df_segmentation_overview.rename(
        columns={"BB": "Previous BB", "percent of BB": "Previous percent of BB"},
        inplace=True,
    )
    merged_segmentation_overview = df_segmentation_overview.merge(
        Updated_df_segmentation_overview, how="inner", on="industry"
    )
    merged_segmentation_overview["change in Unadjusted BB"] = (
        merged_segmentation_overview["BB"] - merged_segmentation_overview["Previous BB"]
    ) / merged_segmentation_overview["Previous BB"]
    merged_segmentation_overview["change in Unadjusted percent of BB"] = (
        merged_segmentation_overview["percent of BB"]
        - merged_segmentation_overview["Previous percent of BB"]
    ) / merged_segmentation_overview["Previous percent of BB"]
    merged_segmentation_overview.set_index("industry", inplace=True)
    merged_segmentation_overview.reset_index(inplace=True)
    previous_security = previous_security.copy()
    previous_security.rename(
        columns={
            "Security BB": "Previous Security BB",
            "Security Percent of BB": "Previous Security Percent of BB",
        },
        inplace=True,
    )
    merged_df_security = previous_security.merge(
        Updated_df_security, how="inner", on="Security"
    )
    merged_df_security["change in Security BB"] = (
        merged_df_security["Security BB"] - merged_df_security["Previous Security BB"]
    ) / merged_df_security["Previous Security BB"]
    merged_df_security["change in Security Percent of BB"] = (
        merged_df_security["Security Percent of BB"]
        - merged_df_security["Previous Security Percent of BB"]
    ) / merged_df_security["Previous Security Percent of BB"]
    merged_df_security.set_index("Security", inplace=True)
    merged_df_security.reset_index(inplace=True)
    return merged_segmentation_overview, merged_df_security


def clean_data_for_whatif(
    df,
    df2,
    df_PL_BB_Results,
    df_principle_obligations,
    df_Availability_Borrower,
    Updated_df_Availability_Borrower,
):
    # make copy and fillna
    temp_df1 = df.copy().fillna(0)
    temp_df2 = df2.copy().fillna(0)
    df_PL_BB_Results = df_PL_BB_Results.copy().fillna(0)
    df_principle_obligations = df_principle_obligations.copy().fillna(0)
    df_Availability_Borrower = df_Availability_Borrower.copy().fillna(0)
    Updated_df_Availability_Borrower = Updated_df_Availability_Borrower.copy().fillna(0)
    # column data check
    temp_df1.columns = temp_df1.columns.str.strip()
    temp_df2.columns = temp_df2.columns.str.strip()
    df_PL_BB_Results.columns = df_PL_BB_Results.columns.str.strip()
    df_principle_obligations.columns = df_principle_obligations.columns.str.strip()
    df_Availability_Borrower.columns = df_Availability_Borrower.columns.str.strip()
    Updated_df_Availability_Borrower.columns = (
        Updated_df_Availability_Borrower.columns.str.strip()
    )
    return (
        temp_df1,
        temp_df2,
        df_PL_BB_Results,
        df_principle_obligations,
        df_Availability_Borrower,
        Updated_df_Availability_Borrower,
    )


def data_for_graphs_after_whatif(df_segmentation_overview, df_security):
    df_seg = df_segmentation_overview.sort_values(by=["BB"], ascending=False)
    df_segmentation_overview_for_chart = df_seg[df_seg["BB"] != 0]
    df_sec = df_security.sort_values(by=["Security BB"], ascending=False)
    df_security_for_chart = df_sec[df_sec["Security BB"] != 0]
    unadjusted_BB_for_chart = (
        df_segmentation_overview_for_chart["BB"].iloc[1:11]
    ).tolist()
    name_of_industry = (
        df_segmentation_overview_for_chart["industry"].iloc[1:11]
    ).tolist()
    unadjusted_previous_BB_for_chart = (
        df_segmentation_overview_for_chart["Previous BB"].iloc[1:11]
    ).tolist()
    BB_for_chart = (df_security_for_chart["Security BB"].iloc[1:11]).tolist()
    name_of_security = (df_security_for_chart["Security"].iloc[1:11]).tolist()
    previous_BB_for_chart = (
        df_security_for_chart["Previous Security BB"].iloc[1:11]
    ).tolist()
    return (
        unadjusted_BB_for_chart,
        name_of_industry,
        BB_for_chart,
        name_of_security,
        unadjusted_previous_BB_for_chart,
        previous_BB_for_chart,
    )


def required_data_for_what_if(
    temp_df1, temp_df2, df_PL_BB_Results, df_principle_obligations
):
    # extract required data
    industry_col = temp_df1["industry"].tolist()
    unadjusted_borrwing_base = temp_df1["BB"].tolist()
    unadjusted_perc_bb = temp_df1["percent of BB"].tolist()
    prev_UAB = temp_df1["Previous BB"].tolist()
    prev_percUAB = temp_df1["Previous percent of BB"].tolist()
    perc_change = temp_df1["change in Unadjusted BB"].tolist()
    perc_change_perc = temp_df1["change in Unadjusted percent of BB"].tolist()
    security_col = temp_df2["Security"].tolist()
    borrowing_base = temp_df2["Security BB"].tolist()
    perc_BB = temp_df2["Security Percent of BB"].tolist()
    prev_BB = temp_df2["Previous Security BB"].tolist()
    prev_perc_BB = temp_df2["Previous Security Percent of BB"].tolist()
    perc_change_security = temp_df2["change in Security BB"].tolist()
    perc_change_sec_perc = temp_df2["change in Security Percent of BB"].tolist()
    concentration_tests = df_PL_BB_Results["Concentration Tests"].tolist()
    concentration_limits = df_PL_BB_Results["Concentration Limit"].tolist()
    actual_values = df_PL_BB_Results["Actual"].tolist()
    obligations = df_principle_obligations["Principal Obligations"].tolist()
    currency = df_principle_obligations["Currency"].tolist()
    amount = df_principle_obligations["Amount"].tolist()
    spotrate = df_principle_obligations["Spot Rate"].tolist()
    dollarequivalent = df_principle_obligations["Dollar Equivalent"].tolist()
    (
        unadjusted_BB_for_chart,
        name_of_industry,
        BB_for_chart,
        name_of_security,
        unadjusted_previous_BB_for_chart,
        previous_BB_for_chart,
    ) = data_for_graphs_after_whatif(temp_df1, temp_df2)
    pass_list = df_PL_BB_Results["Result"].tolist()
    return (
        industry_col,
        unadjusted_borrwing_base,
        unadjusted_perc_bb,
        prev_UAB,
        prev_percUAB,
        perc_change,
        perc_change_perc,
        security_col,
        borrowing_base,
        perc_BB,
        prev_BB,
        prev_perc_BB,
        perc_change_security,
        perc_change_sec_perc,
        concentration_tests,
        concentration_limits,
        actual_values,
        obligations,
        currency,
        amount,
        spotrate,
        dollarequivalent,
        unadjusted_BB_for_chart,
        name_of_industry,
        BB_for_chart,
        name_of_security,
        unadjusted_previous_BB_for_chart,
        previous_BB_for_chart,
        pass_list,
    )


def generating_data_in_required_format_for_whatif(
    Updated_df_Availability_Borrower,
    df_Availability_Borrower,
    industry_col,
    unadjusted_borrwing_base,
    unadjusted_perc_bb,
    prev_UAB,
    prev_percUAB,
    perc_change,
    perc_change_perc,
    security_col,
    borrowing_base,
    perc_BB,
    prev_BB,
    prev_perc_BB,
    perc_change_security,
    perc_change_sec_perc,
    concentration_tests,
    concentration_limits,
    actual_values,
    obligations,
    currency,
    amount,
    spotrate,
    dollarequivalent,
    unadjusted_BB_for_chart,
    name_of_industry,
    BB_for_chart,
    name_of_security,
    unadjusted_previous_BB_for_chart,
    previous_BB_for_chart,
    pass_list,
):
    # create response data
    def get_percentageChange(
        Updated_df_Availability_Borrower_value, df_Availability_Borrower_value
    ):
        try:
            percentageChange = "{:.2f}%".format(
                (
                    (
                        Updated_df_Availability_Borrower_value
                        - df_Availability_Borrower_value
                    )
                    / df_Availability_Borrower_value
                )
                * 100
            )
        except ZeroDivisionError as zde:
            percentageChange = "0%"
        return percentageChange

    card_data = {
        "Total BB": [
            {
                "data": "$"
                + numerize.numerize(
                    round(Updated_df_Availability_Borrower.loc[17, "B"], 2)
                ),
                "changeInValue": True,
                "prevValue": "$"
                + numerize.numerize(round(df_Availability_Borrower.loc[17, "B"], 2)),
                "percentageChange": get_percentageChange(
                    Updated_df_Availability_Borrower.loc[17, "B"],
                    df_Availability_Borrower.loc[17, "B"],
                ),
            }
        ],
        "Leverage BB": [
            {
                "data": "$"
                + numerize.numerize(
                    round(Updated_df_Availability_Borrower.loc[13, "B"], 2)
                ),
                "changeInValue": True,
                "prevValue": "$"
                + numerize.numerize(round(df_Availability_Borrower.loc[13, "B"], 2)),
                "percentageChange": get_percentageChange(
                    Updated_df_Availability_Borrower.loc[13, "B"],
                    df_Availability_Borrower.loc[13, "B"],
                ),
            }
        ],
        "Subscription BB": [
            {
                "data": "$"
                + numerize.numerize(
                    round(Updated_df_Availability_Borrower.loc[9, "B"], 2)
                ),
                "changeInValue": True,
                "prevValue": "$"
                + numerize.numerize(round(df_Availability_Borrower.loc[9, "B"], 2)),
            }
        ],
        "Availability": [
            {
                "data": "$"
                + numerize.numerize(
                    round(Updated_df_Availability_Borrower.loc[22, "B"], 2)
                ),
                "changeInValue": True,
                "prevValue": "$"
                + numerize.numerize(round(df_Availability_Borrower.loc[22, "B"], 2)),
            }
        ],
        "Obligors net capital": [
            {
                "data": "$" + numerize.numerize(round(dollarequivalent[0], 2)),
                "changeInValue": True,
                "prevValue": "$" + numerize.numerize(round(dollarequivalent[-1], 0)),
            }
        ],
        "ordered_card_names": [
            "Total BB",
            "Leverage BB",
            "Subscription BB",
            "Availability",
            "Obligors net capital",
        ],
    }

    segmentation_overview_data = {
        "columns": [{"data": ["Industry", "Unadjusted BB", "Unadjusted % of BB"]}],
        "Industry": [{"data": val, "changeInValue": True} for val in industry_col[:-1]],
        "Unadjusted BB": [
            {
                "data": "$" + numerize.numerize(round(val, 2)),
                "prevValue": "$" + numerize.numerize(round(val2, 2)),
                "percentageChange": "{:.2f}%".format(val3 * 100),
            }
            for val, val2, val3 in zip(
                unadjusted_borrwing_base[:-1], prev_UAB[:-1], perc_change[:-1]
            )
        ],
        "Unadjusted % of BB": [
            {
                "data": "{:.2f}%".format(round(val, 2)),
                "prevValue": "{:.2f}%".format(round(val2, 2)),
                "percentageChange": "{:.2f}%".format(val3 * 100),
            }
            for val, val2, val3 in zip(
                unadjusted_perc_bb[:-1], prev_percUAB[:-1], perc_change_perc[:-1]
            )
        ],
        "Total": {
            "data": {
                "Industry": industry_col[-1],
                "Unadjusted BB": "$"
                + numerize.numerize(round(unadjusted_borrwing_base[-1], 2)),
                "Unadjusted % of BB": "{:.2f}%".format(unadjusted_perc_bb[-1] * 100),
            }
        },
    }

    security_data = {
        "columns": [{"data": ["Security", "BB", "% of BB"]}],
        "Security": [{"data": val, "changeInValue": True} for val in security_col[:-1]],
        "BB": [
            {
                "data": "$" + numerize.numerize(round(val, 2)),
                "prevValue": "$" + numerize.numerize(round(val2, 2)),
                "percentageChange": "{:.2f}%".format(val3 * 100),
            }
            for val, val2, val3 in zip(
                borrowing_base[:-1], prev_BB[:-1], perc_change_security[:-1]
            )
        ],
        "% of BB": [
            {
                "data": "{:.2f}%".format(round(val, 2)),
                "prevValue": "{:.2f}%".format(round(val2, 2)),
                "percentageChange": "{:.2f}%".format(val3 * 100),
            }
            for val, val2, val3 in zip(
                perc_BB[:-1], prev_perc_BB[:-1], perc_change_sec_perc[:-1]
            )
        ],
        "Total": {
            "data": {
                "Security": security_col[-1],
                "BB": "$" + numerize.numerize(round(borrowing_base[-1], 2)),
                "% of BB": "{:.2f}%".format(perc_BB[-1] * 100),
            }
        },
    }

    concentration_Test_data = {
        "columns": [
            {"data": ["Concentration Test", "Concentration Limit", "Actual", "Result"]}
        ],
        "Concentration Test": [{"data": val} for val in concentration_tests[:-1]],
        "Concentration Limit": [{"data": val} for val in concentration_limits[:-1]],
        "Actual": [{"data": val} for val in actual_values[:-1]],
        "Result": [{"data": (val)} for val in pass_list[:-1]],
    }

    principal_obligation_data = {
        "columns": [
            {
                "data": [
                    "Obligation",
                    "Currency",
                    "Amount",
                    "Spot rate",
                    "Dollar equivalent",
                ]
            }
        ],
        "Obligation": [{"data": val} for val in obligations],
        "Currency": [{"data": val} for val in currency],
        "Amount": [{"data": "$" + numerize.numerize(round(val, 2))} for val in amount],
        "Spot rate": [{"data": "{:.2f}%".format(round(val, 2))} for val in spotrate],
        "Dollar equivalent": [
            {"data": "$" + numerize.numerize(round(val, 2))} for val in dollarequivalent
        ],
    }

    # Create required format for chart data
    segmentation_chart_data = {
        "segmentation_chart_data": [
            {"name": name, "Updated unadjusted BB": val, "Unadjusted BB": value}
            for name, val, value in zip(
                name_of_industry,
                unadjusted_BB_for_chart,
                unadjusted_previous_BB_for_chart,
            )
        ],
        "y_axis": "name",
        "x_axis": ["Updated unadjusted BB", "BB"],
    }

    security_chart_data = {
        "security_chart_data": [
            {"name": name, "Updated BB": val, "BB": value}
            for name, val, value in zip(
                name_of_security, BB_for_chart, previous_BB_for_chart
            )
        ],
        "x_axis": ["Updated BB", "BB"],
        "y_axis": "name",
    }

    return (
        card_data,
        segmentation_overview_data,
        security_data,
        concentration_Test_data,
        principal_obligation_data,
        segmentation_chart_data,
        security_chart_data,
    )


def formated_response_whatif_analysis(
    df,
    df2,
    df_PL_BB_Results,
    df_principle_obligations,
    df_Availability_Borrower,
    Updated_df_Availability_Borrower,
):
    # Clean column names (strip leading/trailing spaces) and fill NaN values with 0
    (
        temp_df1,
        temp_df2,
        df_PL_BB_Results,
        df_principle_obligations,
        df_Availability_Borrower,
        Updated_df_Availability_Borrower,
    ) = clean_data_for_whatif(
        df,
        df2,
        df_PL_BB_Results,
        df_principle_obligations,
        df_Availability_Borrower,
        Updated_df_Availability_Borrower,
    )
    # converion of required data
    df_PL_BB_Results = number_formatting_for_concentration(df_PL_BB_Results)
    # extract required data
    (
        industry_col,
        unadjusted_borrwing_base,
        unadjusted_perc_bb,
        prev_UAB,
        prev_percUAB,
        perc_change,
        perc_change_perc,
        security_col,
        borrowing_base,
        perc_BB,
        prev_BB,
        prev_perc_BB,
        perc_change_security,
        perc_change_sec_perc,
        concentration_tests,
        concentration_limits,
        actual_values,
        obligations,
        currency,
        amount,
        spotrate,
        dollarequivalent,
        unadjusted_BB_for_chart,
        name_of_industry,
        BB_for_chart,
        name_of_security,
        unadjusted_previous_BB_for_chart,
        previous_BB_for_chart,
        pass_list,
    ) = required_data_for_what_if(
        temp_df1, temp_df2, df_PL_BB_Results, df_principle_obligations
    )  # create response data

    (
        card_data,
        segmentation_overview_data,
        security_data,
        concentration_Test_data,
        principal_obligation_data,
        segmentation_chart_data,
        security_chart_data,
    ) = generating_data_in_required_format_for_whatif(
        Updated_df_Availability_Borrower,
        df_Availability_Borrower,
        industry_col,
        unadjusted_borrwing_base,
        unadjusted_perc_bb,
        prev_UAB,
        prev_percUAB,
        perc_change,
        perc_change_perc,
        security_col,
        borrowing_base,
        perc_BB,
        prev_BB,
        prev_perc_BB,
        perc_change_security,
        perc_change_sec_perc,
        concentration_tests,
        concentration_limits,
        actual_values,
        obligations,
        currency,
        amount,
        spotrate,
        dollarequivalent,
        unadjusted_BB_for_chart,
        name_of_industry,
        BB_for_chart,
        name_of_security,
        unadjusted_previous_BB_for_chart,
        previous_BB_for_chart,
        pass_list,
    )
    return (
        card_data,
        segmentation_overview_data,
        security_data,
        concentration_Test_data,
        principal_obligation_data,
        segmentation_chart_data,
        security_chart_data,
    )


def obligator_net_capital_data(obligator_copy):
    obligations = obligator_copy["Principal Obligations"].tolist()
    currency = obligator_copy["Currency"].tolist()
    amount = obligator_copy["Amount"].tolist()
    spotrate = obligator_copy["Spot Rate"].tolist()
    dollarequivalent = obligator_copy["Dollar Equivalent"].tolist()
    obligators_net_capital = {
        "columns": [
            {
                "data": [
                    "Obligation",
                    "Currency",
                    "Amount",
                    "Spot rate",
                    "Dollar equivalent",
                ]
            }
        ],
        "Obligation": [{"data": val} for val in obligations],
        "Currency": [{"data": val} for val in currency],
        "Amount": [{"data": "$" + numerize.numerize(round(val, 2))} for val in amount],
        "Spot rate": [{"data": "{:.2f}%".format(round(val, 2))} for val in spotrate],
        "Dollar equivalent": [
            {"data": "$" + numerize.numerize(round(val, 2))} for val in dollarequivalent
        ],
    }
    return obligators_net_capital


def remaining_card_data(card_name, card_name_column_mapping, df_Availability_Borrower):
    search_values = card_name_column_mapping[card_name]
    # Initialize an empty list to store the information of all matching rows
    matched_rows = []
    # Iterate over the list of search values
    for value in search_values:
        # Locate the rows based on the value in the 'B' column
        row_data = df_Availability_Borrower[df_Availability_Borrower["A"] == value]
        # Check if the row exists
        if not row_data.empty:
            # Extract all information from the row and store it in a list
            row_values = row_data.values.tolist()
            matched_rows.extend(row_values)
    card_table = {
        "columns": [{"data": ["Term", "Value"]}],
        "Term": [{"data": matched_row[0]} for matched_row in matched_rows],
        "Value": [{"data": matched_row[1]} for matched_row in matched_rows],
    }
    return card_table


# def number_formatting_for_availablity(df_Availability_Borrower):
#     df_Availability_Borrower.at[1, 'B'] = str(pd.to_datetime(df_Availability_Borrower.at[1, 'B']).date())
#     df_Availability_Borrower.at[2, 'B'] = str(pd.to_datetime(df_Availability_Borrower.at[2, 'B']).date())
#     df_Availability_Borrower.at[4, 'B'] = "${:,.0f}".format(float(df_Availability_Borrower.at[4, 'B']))
#     df_Availability_Borrower.at[5, 'B'] = "${:,.0f}".format(float(df_Availability_Borrower.at[5, 'B']))
#     df_Availability_Borrower.at[6, 'B'] = "{:,.0f}".format(float(df_Availability_Borrower.at[6, 'B']))
#     df_Availability_Borrower.at[7, 'B'] = "{:,.0f}".format(float(df_Availability_Borrower.at[7, 'B']))
#     df_Availability_Borrower.at[8, 'B'] = "${:,.0f}".format(float(df_Availability_Borrower.at[8, 'B']))
#     df_Availability_Borrower.at[9, 'B'] = "${:,.0f}".format(float(df_Availability_Borrower.at[9, 'B']))
#     df_Availability_Borrower.at[10, 'B'] = "{:,.01f}%".format(float(df_Availability_Borrower.at[10, 'B']) * 100)
#     df_Availability_Borrower.at[12, 'B'] = "${:,.0f}".format(float(df_Availability_Borrower.at[12, 'B']))
#     df_Availability_Borrower.at[13, 'B'] = "${:,.0f}".format(float(df_Availability_Borrower.at[13, 'B']))
#     df_Availability_Borrower.at[14, 'B'] = "{:,.01f}%".format(float(df_Availability_Borrower.at[14, 'B']) * 100)
#     df_Availability_Borrower.at[15, 'B'] = "{:,.01f}%".format(float(df_Availability_Borrower.at[15, 'B']) * 100)
#     df_Availability_Borrower.at[16, 'B'] = "${:,.0f}".format(float(df_Availability_Borrower.at[16, 'B']))
#     df_Availability_Borrower.at[17, 'B'] = "${:,.0f}".format(float(df_Availability_Borrower.at[17, 'B']))
#     df_Availability_Borrower.at[18, 'B'] = "${:,.0f}".format(float(df_Availability_Borrower.at[18, 'B']))
#     df_Availability_Borrower.at[19, 'B'] = "${:,.0f}".format(float(df_Availability_Borrower.at[19, 'B']))
#     df_Availability_Borrower.at[20, 'B'] = "{:,.01f}%".format(float(df_Availability_Borrower.at[20, 'B']) * 100)
#     df_Availability_Borrower.at[21, 'B'] = "{:,.01f}%".format(float(df_Availability_Borrower.at[21, 'B']) * 100)
#     df_Availability_Borrower.at[22, 'B'] = "${:,.0f}".format(float(df_Availability_Borrower.at[22, 'B']))
#     return df_Availability_Borrower

# def number_formatting_for_concentration(df):
#     rows_to_keep = [
#     'Min. Eligible Issuers (#)',
#     '8 or 9 Issuers?',
#     'Max. Weighted Average Maturity (Years)',
#     'Max. Weighted Average Leverage thru Borrower'
#     ]
#     # Create a mask to identify rows to convert
#     mask = ~df['Concentration Tests'].isin(rows_to_keep)
#     # Convert values to percentages for relevant rows
#     df.loc[mask, 'Concentration Limit'] = (df.loc[mask, 'Concentration Limit'] * 100).map('{:.0f}%'.format)
#     df.loc[mask, 'Actual'] = (df.loc[mask, 'Actual'] * 100).map('{:.0f}%'.format)
#     df = df.applymap(lambda x: round(x, 0) if isinstance(x, (float, int)) and x is not None else x)
#     return df

#     # Clean column names (strip leading/trailing spaces) and fill NaN values with 0
# def clean_data(df_PL_BB_Results, df_security, df_segmentation_overview, df_principle_obligations, df_Availability_Borrower):
#     df_PL_BB_Results = df_PL_BB_Results.copy().fillna(0)
#     df_security = df_security.copy().fillna(0)
#     df_segmentation_overview = df_segmentation_overview.copy().fillna(0)
#     df_principle_obligations = df_principle_obligations.copy().fillna(0)
#     df_Availability_Borrower = df_Availability_Borrower.copy().fillna(0)
#     df_PL_BB_Results.columns = df_PL_BB_Results.columns.str.strip()
#     df_security.columns = df_security.columns.str.strip()
#     df_segmentation_overview.columns = df_segmentation_overview.columns.str.strip()
#     df_principle_obligations.columns = df_principle_obligations.columns.str.strip()
#     df_Availability_Borrower.columns = df_Availability_Borrower.columns.str.strip()
#     return df_PL_BB_Results, df_security, df_segmentation_overview, df_principle_obligations, df_Availability_Borrower

# def data_for_graphs(df_security, df_segmentation_overview):
#     df_seg = df_segmentation_overview.sort_values(by=['BB'], ascending=False)
#     df_segmentation_overview_for_chart = df_seg[df_seg['BB'] != 0]
#     df_sec = df_security.sort_values(by=['Security BB'], ascending=False)
#     df_security_for_chart = df_sec[df_sec['Security BB'] != 0]
#     unadjusted_BB_for_chart = (df_segmentation_overview_for_chart['BB'].iloc[1:11]).tolist()
#     name_of_industry = (df_segmentation_overview_for_chart['industry'].iloc[1:11]).tolist()
#     BB_for_chart = (df_security_for_chart['Security BB'].iloc[1:11]).tolist()
#     name_of_security = (df_security_for_chart['Security'].iloc[1:11]).tolist()
#     return unadjusted_BB_for_chart,name_of_industry,BB_for_chart,name_of_security

#     # Extract relevant information
# def required_data(df_PL_BB_Results, df_security, df_segmentation_overview, df_principle_obligations):
#     industry = df_segmentation_overview['industry'].tolist()
#     unadjusted_BB = df_segmentation_overview['BB'].tolist()
#     percent_of_unadjusted_BB = df_segmentation_overview['percent of BB'].tolist()
#     security = df_security['Security'].tolist()
#     BB = df_security['Security BB'].tolist()
#     percent_of_BB = df_security['Security Percent of BB'].tolist()
#     concentration_tests = df_PL_BB_Results['Concentration Tests'].tolist()
#     concentration_limits = df_PL_BB_Results['Concentration Limit'].tolist()
#     actual_values = df_PL_BB_Results['Actual'].tolist()
#     obligations = df_principle_obligations['Principal Obligations'].tolist()
#     currency = df_principle_obligations['Currency'].tolist()
#     amount = df_principle_obligations['Amount'].tolist()
#     spotrate = df_principle_obligations['Spot Rate'].tolist()
#     dollarequivalent = df_principle_obligations['Dollar Equivalent'].tolist()
#     unadjusted_BB_for_chart = sorted(unadjusted_BB, reverse=True)[:10]
#     unadjusted_BB_for_chart,name_of_industry,BB_for_chart,name_of_security = data_for_graphs(df_security, df_segmentation_overview)
#     return industry,unadjusted_BB,percent_of_unadjusted_BB,security,BB,percent_of_BB,concentration_tests,concentration_limits,actual_values,obligations,currency,amount,spotrate,dollarequivalent,unadjusted_BB_for_chart,name_of_industry,BB_for_chart,name_of_security

# def generating_data_in_required_format_for_result(df_Availability_Borrower,industry,unadjusted_BB,percent_of_unadjusted_BB,security,BB,percent_of_BB,concentration_tests,concentration_limits,actual_values,obligations,currency,amount,spotrate,dollarequivalent,unadjusted_BB_for_chart,name_of_industry,BB_for_chart,name_of_security):    # Extracting specific rows from df_Availability_Borrower for card data
#     card_data = {
#         'Total BB': [{'data': (df_Availability_Borrower.loc[17, 'B'])}],
#         'Leverage BB': [{'data': (df_Availability_Borrower.loc[13, 'B'])}],
#         'Subscription BB': [{'data': (df_Availability_Borrower.loc[9, 'B'])}],
#         'Availability': [{'data': (df_Availability_Borrower.loc[22, 'B'])}],
#         'Obligors net capital': [{'data': "${:,.0f}".format(float(dollarequivalent[0]))}]
#     }
#     # Create required format for segmentation overview data
#     segmentation_Overview_data = {
#         'columns': [{'data': ['Industry', 'Unadjusted BB', 'Unadjusted % of BB']}],
#         'Industry': [{'data': val} for val in industry[:-1]],
#         'Unadjusted BB': [{'data': "${:,.0f}".format(float(val))} for val in unadjusted_BB[:-1]],
#         'Unadjusted % of BB': [{'data': f'{round(val * 100, 2)}%'} for val in percent_of_unadjusted_BB[:-1]],
#         'Total': {'data': {'Industry': industry[-1], 'Unadjusted BB': "${:,.0f}".format(float(unadjusted_BB[-1])), 'Unadjusted % of BB': f'{round(percent_of_unadjusted_BB[-1] * 100, 2)}%'}}
#     }
#     # Create required format for security data
#     security_data = {
#         "columns": [{'data': ["Security", "BB", "% of BB"]}],
#         "Security": [{'data': val} for val in security[:-1]],
#         "BB": [{'data': "${:,.0f}".format(float(val))} for val in BB[:-1]],
#         "% of BB": [{'data': f'{round(val * 100, 2)}%'} for val in percent_of_BB[:-1]],
#         'Total': {'data': {"Security": security[-1], "BB": "${:,.0f}".format(float(BB[-1])), "% of BB": f'{round(percent_of_BB[-1] * 100, 2)}%'}}
#     }
#     # Create required format for concentration test data
#     concentration_Test_data = {
#         "columns": [{'data': ["Concentration Test", "Concentration Limit", "Actual"]}],
#         "Concentration Test": [{'data': val} for val in concentration_tests[:-1]],
#         "Concentration Limit": [{'data': (val)}  for val in concentration_limits[:-1]],
#         "Actual": [{'data': (val)}  for val in actual_values[:-1]],
#         # 'Total': {'data': {"Concentration Test": "Total", "Concentration Limit": "${:,.0f}".format(float(sum(concentration_limits[:-1]) * 100)), "Actual": "${:,.0f}".format(float(sum(actual_values[:-1])) if all(isinstance(val, (int, float)) for val in actual_values[:-1]) else "NaN")}}
#     }
#     # Create required format for principal obligation data
#     principal_obligation_data = {
#         "columns": [{'data': ["Obligation", "Currency", "Amount", "Spot rate", "Dollar equivalent"]}],
#         "Obligation": [{'data': val} for val in obligations],
#         "Currency": [{'data': val} for val in currency],
#         "Amount": [{'data': "${:,.0f}".format(float(val))} for val in amount],
#         "Spot rate": [{'data': "{:,.0f}%".format(float(val))} for val in spotrate],
#         "Dollar equivalent": [{'data': "${:,.0f}".format(float(val))} for val in dollarequivalent]
#     }
#     # Create required format for chart data
#     segmentation_chart_data = [
#     {
#         "name": name,
#         "Unadjusted BB": val
#     }
#     for name, val in zip(name_of_industry, unadjusted_BB_for_chart)
#     ]

#     security_chart_data = [
#     {
#         "name": name,
#         "BB": val
#     }
#     for name, val in zip(name_of_security, BB_for_chart)
#     ]
#     return card_data, segmentation_Overview_data, security_data, concentration_Test_data, principal_obligation_data, segmentation_chart_data, security_chart_data

# def formatted_data(df_PL_BB_Results, df_security, df_segmentation_overview, df_principle_obligations, df_Availability_Borrower):
#     # Clean column names (strip leading/trailing spaces) and fill NaN values with 0
#     df_PL_BB_Results, df_security, df_segmentation_overview, df_principle_obligations, df_Availability_Borrower = clean_data(
#         df_PL_BB_Results, df_security, df_segmentation_overview, df_principle_obligations, df_Availability_Borrower)
#     df_Availability_Borrower = number_formatting_for_availablity(df_Availability_Borrower)
#     df_PL_BB_Results = number_formatting_for_concentration(df_PL_BB_Results)
#     # Extract relevant information
#     industry,unadjusted_BB,percent_of_unadjusted_BB,security,BB,percent_of_BB,concentration_tests,concentration_limits,actual_values,obligations,currency,amount,spotrate,dollarequivalent,unadjusted_BB_for_chart,name_of_industry,BB_for_chart,name_of_security = required_data(df_PL_BB_Results, df_security, df_segmentation_overview, df_principle_obligations)    # generating_data_in_required_format_for_result
#     card_data, segmentation_Overview_data, security_data, concentration_Test_data, principal_obligation_data, segmentation_chart_data, security_chart_data = generating_data_in_required_format_for_result(df_Availability_Borrower,industry,unadjusted_BB,percent_of_unadjusted_BB,security,BB,percent_of_BB,concentration_tests,concentration_limits,actual_values,obligations,currency,amount,spotrate,dollarequivalent,unadjusted_BB_for_chart,name_of_industry,BB_for_chart,name_of_security)
#     return card_data, segmentation_Overview_data, security_data, concentration_Test_data, principal_obligation_data , segmentation_chart_data, security_chart_data

# def sheets_for_whatif_analysis(df_segmentation_overview,previous_security,Updated_df_segmentation_overview,Updated_df_security):
#     df_segmentation_overview.rename(columns= {'BB':'Previous BB','percent of BB':'Previous percent of BB'},inplace=True)
#     merged_segmentation_overview = df_segmentation_overview.merge(Updated_df_segmentation_overview,how='inner',on='industry')
#     merged_segmentation_overview['change in Unadjusted BB'] = (merged_segmentation_overview['BB'] - merged_segmentation_overview['Previous BB'])/merged_segmentation_overview['Previous BB']
#     merged_segmentation_overview['change in Unadjusted percent of BB'] = (merged_segmentation_overview['percent of BB'] - merged_segmentation_overview['Previous percent of BB'])/merged_segmentation_overview['Previous percent of BB']
#     merged_segmentation_overview.set_index('industry',inplace=True)
#     merged_segmentation_overview.reset_index(inplace=True)
#     previous_security = previous_security.copy()
#     previous_security.rename(columns= {'Security BB':'Previous Security BB','Security Percent of BB':'Previous Security Percent of BB'},inplace=True)
#     merged_df_security = previous_security.merge(Updated_df_security,how='inner',on='Security')
#     merged_df_security['change in Security BB'] = (merged_df_security['Security BB'] - merged_df_security['Previous Security BB'])/merged_df_security['Previous Security BB']
#     merged_df_security['change in Security Percent of BB'] = (merged_df_security['Security Percent of BB'] - merged_df_security['Previous Security Percent of BB'])/merged_df_security['Previous Security Percent of BB']
#     merged_df_security.set_index('Security',inplace=True)
#     merged_df_security.reset_index(inplace=True)
#     return merged_segmentation_overview, merged_df_security

# def clean_data_for_whatif(df, df2,df_PL_BB_Results,df_principle_obligations,df_Availability_Borrower,Updated_df_Availability_Borrower):
#     # make copy and fillna
#     temp_df1 = df.copy().fillna(0)
#     temp_df2 = df2.copy().fillna(0)
#     df_PL_BB_Results = df_PL_BB_Results.copy().fillna(0)
#     df_principle_obligations = df_principle_obligations.copy().fillna(0)
#     df_Availability_Borrower = df_Availability_Borrower.copy().fillna(0)
#     Updated_df_Availability_Borrower = Updated_df_Availability_Borrower.copy().fillna(0)
#     # column data check
#     temp_df1.columns = temp_df1.columns.str.strip()
#     temp_df2.columns = temp_df2.columns.str.strip()
#     df_PL_BB_Results.columns = df_PL_BB_Results.columns.str.strip()
#     df_principle_obligations.columns = df_principle_obligations.columns.str.strip()
#     df_Availability_Borrower.columns = df_Availability_Borrower.columns.str.strip()
#     Updated_df_Availability_Borrower.columns = Updated_df_Availability_Borrower.columns.str.strip()
#     return temp_df1,temp_df2,df_PL_BB_Results,df_principle_obligations,df_Availability_Borrower,Updated_df_Availability_Borrower

# def data_for_graphs_after_whatif(df_segmentation_overview,df_security):
#     df_seg = df_segmentation_overview.sort_values(by=['BB'], ascending=False)
#     df_segmentation_overview_for_chart = df_seg[df_seg['BB'] != 0]
#     df_sec = df_security.sort_values(by=['Security BB'], ascending=False)
#     df_security_for_chart = df_sec[df_sec['Security BB'] != 0]
#     unadjusted_BB_for_chart = (df_segmentation_overview_for_chart['BB'].iloc[1:11]).tolist()
#     name_of_industry = (df_segmentation_overview_for_chart['industry'].iloc[1:11]).tolist()
#     unadjusted_previous_BB_for_chart = (df_segmentation_overview_for_chart['Previous BB'].iloc[1:11]).tolist()
#     BB_for_chart = (df_security_for_chart['Security BB'].iloc[1:11]).tolist()
#     name_of_security = (df_security_for_chart['Security'].iloc[1:11]).tolist()
#     previous_BB_for_chart = (df_security_for_chart['Previous Security BB'].iloc[1:11]).tolist()
#     return unadjusted_BB_for_chart,name_of_industry,BB_for_chart,name_of_security,unadjusted_previous_BB_for_chart,previous_BB_for_chart

# def required_data_for_what_if(temp_df1,temp_df2,df_PL_BB_Results,df_principle_obligations):
#     # extract required data
#     industry_col = temp_df1['industry'].tolist()
#     unadjusted_borrwing_base = temp_df1['BB'].tolist()
#     unadjusted_perc_bb = temp_df1['percent of BB'].tolist()
#     prev_UAB = temp_df1['Previous BB'].tolist()
#     prev_percUAB = temp_df1['Previous percent of BB'].tolist()
#     perc_change = temp_df1['change in Unadjusted BB'].tolist()
#     perc_change_perc = temp_df1['change in Unadjusted percent of BB'].tolist()
#     security_col = temp_df2['Security'].tolist()
#     borrowing_base = temp_df2['Security BB'].tolist()
#     perc_BB = temp_df2['Security Percent of BB'].tolist()
#     prev_BB = temp_df2['Previous Security BB'].tolist()
#     prev_perc_BB = temp_df2['Previous Security Percent of BB'].tolist()
#     perc_change_security = temp_df2['change in Security BB'].tolist()
#     perc_change_sec_perc = temp_df2['change in Security Percent of BB'].tolist()
#     concentration_tests = df_PL_BB_Results['Concentration Tests'].tolist()
#     concentration_limits = df_PL_BB_Results['Concentration Limit'].tolist()
#     actual_values = df_PL_BB_Results['Actual'].tolist()
#     obligations = df_principle_obligations['Principal Obligations'].tolist()
#     currency = df_principle_obligations['Currency'].tolist()
#     amount = df_principle_obligations['Amount'].tolist()
#     spotrate = df_principle_obligations['Spot Rate'].tolist()
#     dollarequivalent = df_principle_obligations['Dollar Equivalent'].tolist()
#     unadjusted_BB_for_chart,name_of_industry,BB_for_chart,name_of_security,unadjusted_previous_BB_for_chart,previous_BB_for_chart = data_for_graphs_after_whatif(temp_df1,temp_df2)
#     return industry_col,unadjusted_borrwing_base,unadjusted_perc_bb,prev_UAB,prev_percUAB,perc_change,perc_change_perc,security_col,borrowing_base,perc_BB,prev_BB,prev_perc_BB,perc_change_security,perc_change_sec_perc,concentration_tests,concentration_limits,actual_values,obligations,currency,amount,spotrate,dollarequivalent,unadjusted_BB_for_chart,name_of_industry,BB_for_chart,name_of_security,unadjusted_previous_BB_for_chart,previous_BB_for_chart

# def generating_data_in_required_format_for_whatif(Updated_df_Availability_Borrower,df_Availability_Borrower,industry_col,unadjusted_borrwing_base,unadjusted_perc_bb,prev_UAB,prev_percUAB,perc_change,perc_change_perc,security_col,borrowing_base,perc_BB,prev_BB,prev_perc_BB,perc_change_security,perc_change_sec_perc,concentration_tests,concentration_limits,actual_values,obligations,currency,amount,spotrate,dollarequivalent,unadjusted_BB_for_chart,name_of_industry,BB_for_chart,name_of_security,unadjusted_previous_BB_for_chart,previous_BB_for_chart):
#         # create response data
#     card_data = {
#         'Total BB': [{'data': "${:,.0f}".format(float(round(Updated_df_Availability_Borrower.loc[17, 'B'], 2))), 'changeInValue':True, 'prevValue': "${:,.0f}".format(float(round(df_Availability_Borrower.loc[17, 'B'], 2))), 'percentageChange': f'{round(((Updated_df_Availability_Borrower.loc[17, "B"] - df_Availability_Borrower.loc[17, "B"]) / df_Availability_Borrower.loc[17, "B"]) * 100, 2)}%'}],
#         'Leverage BB': [{'data': "${:,.0f}".format(float(round(Updated_df_Availability_Borrower.loc[13, 'B'], 2))), 'changeInValue':True, 'prevValue': "${:,.0f}".format(float(round(df_Availability_Borrower.loc[13, 'B'], 2))), 'percentageChange': f'{round(((Updated_df_Availability_Borrower.loc[13, "B"] - df_Availability_Borrower.loc[13, "B"]) / df_Availability_Borrower.loc[13, "B"]) * 100, 2)}%'}],
#         'Subscription BB': [{'data': "${:,.0f}".format(float(round(Updated_df_Availability_Borrower.loc[9, 'B'], 2))), 'changeInValue':True, 'prevValue': "${:,.0f}".format(float(round(df_Availability_Borrower.loc[9, 'B'], 2)))}],
#         'Availability': [{'data': "${:,.0f}".format(float(round(Updated_df_Availability_Borrower.loc[22, 'B'], 2))), 'changeInValue':True, 'prevValue': "${:,.0f}".format(float(round(df_Availability_Borrower.loc[22, 'B'], 2)))}],
#         'Obligors net capital': [{'data': "${:,.0f}".format(float(round(dollarequivalent[0], 2))), 'changeInValue':True, 'prevValue': "${:,.0f}".format(float(round(dollarequivalent[-1], 0)))}]
#     }
#     segmentation_overview_data = {
#         'columns': [{'data': ['Industry', 'Unadjusted BB', 'Unadjusted % of BB']}],
#         'Industry': [{'data': val, 'changeInValue':True} for val in industry_col[:-1]],
#         'Unadjusted BB': [{'data': "${:,.0f}".format(float(val)), 'prevValue': "${:,.0f}".format(float(val2)), 'percentageChange': f'{round(val3 * 100, 2)}%'} for val, val2, val3 in zip(unadjusted_borrwing_base[:-1], prev_UAB[:-1], perc_change[:-1])],
#         'Unadjusted % of BB': [{'data': f'{round(val * 100, 2)}%', 'prevValue': f'{round(val2 * 100, 2)}%', 'percentageChange': f'{round(val3 * 100, 2)}%'} for val, val2, val3 in zip(unadjusted_perc_bb[:-1], prev_percUAB[:-1], perc_change_perc[:-1])],
#         'Total': {'data': {'Industry': industry_col[-1], 'Unadjusted BB': "${:,.0f}".format(float(round(unadjusted_borrwing_base[-1], 2))), 'Unadjusted % of BB': f'{round(unadjusted_perc_bb[-1] * 100, 2)}%'}}
#     }
#     security_data = {
#         "columns": [{'data': ["Security", "BB", "% of BB"]}],
#         "Security": [{'data': val, 'changeInValue':True} for val in security_col[:-1]],
#         "BB": [{'data': "${:,.0f}".format(float(val)), 'prevValue': "${:,.0f}".format(float(val2)), 'percentageChange': f'{round(val3 * 100, 2)}%'} for val, val2, val3 in zip(borrowing_base[:-1], prev_BB[:-1], perc_change_security[:-1])],
#         "% of BB": [{'data': f'{round(val * 100, 2)}%', 'prevValue': f'{round(val2 * 100, 2)}%', 'percentageChange': f'{round(val3 * 100, 2)}%'} for val, val2, val3 in zip(perc_BB[:-1], prev_perc_BB[:-1], perc_change_sec_perc[:-1])],
#         'Total': {'data': {"Security": security_col[-1], "BB": "${:,.0f}".format(float(round(borrowing_base[-1], 2))), "% of BB": f'{round(perc_BB[-1] * 100, 2)}%'}}
#     }
#     concentration_Test_data = {
#         "columns": [{'data': ["Concentration Test", "Concentration Limit", "Actual"]}],
#         "Concentration Test": [{'data': val} for val in concentration_tests[:-1]],
#         "Concentration Limit": [{'data': (val)}  for val in concentration_limits[:-1]],
#         "Actual": [{'data': (val)}  for val in actual_values[:-1]],
#         # 'Total': {'data': {"Concentration Test": "Total", "Concentration Limit": "${:,.0f}".format(float(round(sum(concentration_limits[:-1]) * 100, 2))), "Actual": "${:,.0f}".format(float(round(sum(actual_values[:-1]) if all(isinstance(val, (int, float)) for val in actual_values[:-1]) else "NaN", 2)))}}
#     }
#     principal_obligation_data = {
#         "columns": [{'data': ["Obligation", "Currency", "Amount", "Spot rate", "Dollar equivalent"]}],
#         "Obligation": [{'data': val} for val in obligations],
#         "Currency": [{'data': val} for val in currency],
#         "Amount": [{'data': "${:,.0f}".format(float(val))} for val in amount],
#         "Spot rate": [{'data': "{:,.0f}%".format(float(val))} for val in spotrate],
#         "Dollar equivalent": [{'data': "${:,.0f}".format(float(val))} for val in dollarequivalent]
#     }
#         # Create required format for chart data
#     segmentation_chart_data = [
#     {
#         "name": name,
#         "Updated unadjusted BB": val,
#         "Unadjusted BB": value

#     }
#     for name, val, value in zip(name_of_industry, unadjusted_BB_for_chart, unadjusted_previous_BB_for_chart)
#     ]

#     security_chart_data = [
#     {
#         "name": name,
#         "Updated BB": val,
#         "BB": value
#     }
#     for name, val, value in zip(name_of_security, BB_for_chart, previous_BB_for_chart)
#     ]

#     return card_data,segmentation_overview_data, security_data,concentration_Test_data,principal_obligation_data,segmentation_chart_data,security_chart_data

# def formated_response_whatif_analysis(df, df2,df_PL_BB_Results,df_principle_obligations,df_Availability_Borrower,Updated_df_Availability_Borrower):
#     # Clean column names (strip leading/trailing spaces) and fill NaN values with 0
#     temp_df1,temp_df2,df_PL_BB_Results,df_principle_obligations,df_Availability_Borrower,Updated_df_Availability_Borrower = clean_data_for_whatif(df, df2,df_PL_BB_Results,df_principle_obligations,df_Availability_Borrower,Updated_df_Availability_Borrower)
#     #converion of required data
#     df_PL_BB_Results = number_formatting_for_concentration(df_PL_BB_Results)
#     # extract required data
#     industry_col,unadjusted_borrwing_base,unadjusted_perc_bb,prev_UAB,prev_percUAB,perc_change,perc_change_perc,security_col,borrowing_base,perc_BB,prev_BB,prev_perc_BB,perc_change_security,perc_change_sec_perc,concentration_tests,concentration_limits,actual_values,obligations,currency,amount,spotrate,dollarequivalent,unadjusted_BB_for_chart,name_of_industry,BB_for_chart,name_of_security,unadjusted_previous_BB_for_chart,previous_BB_for_chart = required_data_for_what_if(temp_df1,temp_df2,df_PL_BB_Results,df_principle_obligations)    # create response data

#     card_data,segmentation_overview_data, security_data,concentration_Test_data,principal_obligation_data,segmentation_chart_data,security_chart_data = generating_data_in_required_format_for_whatif(Updated_df_Availability_Borrower,df_Availability_Borrower,industry_col,unadjusted_borrwing_base,unadjusted_perc_bb,prev_UAB,prev_percUAB,perc_change,perc_change_perc,security_col,borrowing_base,perc_BB,prev_BB,prev_perc_BB,perc_change_security,perc_change_sec_perc,concentration_tests,concentration_limits,actual_values,obligations,currency,amount,spotrate,dollarequivalent,unadjusted_BB_for_chart,name_of_industry,BB_for_chart,name_of_security,unadjusted_previous_BB_for_chart,previous_BB_for_chart)
#     return card_data,segmentation_overview_data, security_data,concentration_Test_data,principal_obligation_data,segmentation_chart_data,security_chart_data

# def obligator_net_capital_data(obligator_copy):
#     obligations = obligator_copy['Principal Obligations'].tolist()
#     currency = obligator_copy['Currency'].tolist()
#     amount = obligator_copy['Amount'].tolist()
#     spotrate = obligator_copy['Spot Rate'].tolist()
#     dollarequivalent = obligator_copy['Dollar Equivalent'].tolist()
#     obligators_net_capital = {
#         "columns": [{'data': ["Obligation", "Currency", "Amount", "Spot rate", "Dollar equivalent"]}],
#         "Obligation": [{'data': val} for val in obligations],
#         "Currency": [{'data': val} for val in currency],
#         "Amount": [{'data': "${:,.0f}".format(float(val))} for val in amount],
#         "Spot rate": [{'data': "{:,.0f}%".format(float(val))} for val in spotrate],
#         "Dollar equivalent": [{'data': "${:,.0f}".format(float(val))} for val in dollarequivalent]
#     }
#     return obligators_net_capital

# def remaining_card_data(card_name, card_name_column_mapping, df_Availability_Borrower):
#     search_values = card_name_column_mapping[card_name]
#     # Initialize an empty list to store the information of all matching rows
#     matched_rows = []
#     # Iterate over the list of search values
#     for value in search_values:
#         # Locate the rows based on the value in the 'B' column
#         row_data = df_Availability_Borrower[df_Availability_Borrower['A'] == value]
#         # Check if the row exists
#         if not row_data.empty:
#             # Extract all information from the row and store it in a list
#             row_values = row_data.values.tolist()
#             matched_rows.extend(row_values)
#     card_table = {
#         "columns": [{"data": ["Term", "Value"]}],
#         "Term": [{"data": matched_row[0]} for matched_row in matched_rows],
#         "Value": [{"data": matched_row[1]} for matched_row in matched_rows]
#     }
#     return card_table
