from numerize import numerize


def sheets_for_whatif_analysis(
    initial_segmentation_overview_df,
    initial_security_df,
    Updated_df_segmentation_overview,
    Updated_df_security,
):
    initial_segmentation_overview_df.rename(
        columns={"BB": "Previous BB", "percent of BB": "Previous percent of BB"},
        inplace=True,
    )
    merged_segmentation_overview = initial_segmentation_overview_df.merge(
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
    initial_security_df = initial_security_df.copy()
    initial_security_df.rename(
        columns={
            "Security BB": "Previous Security BB",
            "Security Percent of BB": "Previous Security Percent of BB",
        },
        inplace=True,
    )
    merged_df_security = initial_security_df.merge(
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
    merged_segmentation_overview,
    merged_df_security,
    df_PL_BB_Results,
    df_principle_obligations,
    df_Availability_Borrower,
    Updated_df_Availability_Borrower,
):
    temp_df1 = merged_segmentation_overview.copy().fillna(0)
    temp_df2 = merged_df_security.copy().fillna(0)
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
    merged_segmentation_overview,
    merged_df_security,
    df_PL_BB_Results,
    df_principle_obligations,
):
    # extract required data
    industry_col = merged_segmentation_overview["industry"].tolist()
    unadjusted_borrwing_base = merged_segmentation_overview["BB"].tolist()
    unadjusted_perc_bb = merged_segmentation_overview["percent of BB"].tolist()
    prev_UAB = merged_segmentation_overview["Previous BB"].tolist()
    prev_percUAB = merged_segmentation_overview["Previous percent of BB"].tolist()
    perc_change = merged_segmentation_overview["change in Unadjusted BB"].tolist()
    perc_change_perc = merged_segmentation_overview[
        "change in Unadjusted percent of BB"
    ].tolist()
    security_col = merged_df_security["Security"].tolist()
    borrowing_base = merged_df_security["Security BB"].tolist()
    perc_BB = merged_df_security["Security Percent of BB"].tolist()
    prev_BB = merged_df_security["Previous Security BB"].tolist()
    prev_perc_BB = merged_df_security["Previous Security Percent of BB"].tolist()
    perc_change_security = merged_df_security["change in Security BB"].tolist()
    perc_change_sec_perc = merged_df_security[
        "change in Security Percent of BB"
    ].tolist()
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
    ) = data_for_graphs_after_whatif(merged_segmentation_overview, merged_df_security)
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
        "x_axis": ["Updated unadjusted BB", "Unadjusted BB"],
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


def generate_response(
    merged_segmentation_overview,
    merged_df_security,
    Updated_df_PL_BB_Results,
    df_principle_obligations,
    calculated_df_Availability_Borrower,
    Updated_df_Availability_Borrower,
):

    (
        merged_segmentation_overview,
        merged_df_security,
        df_PL_BB_Results,
        df_principle_obligations,
        calculated_df_Availability_Borrower,
        Updated_df_Availability_Borrower,
    ) = clean_data_for_whatif(
        merged_segmentation_overview,
        merged_df_security,
        Updated_df_PL_BB_Results,
        df_principle_obligations,
        calculated_df_Availability_Borrower,
        Updated_df_Availability_Borrower,
    )

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
        merged_segmentation_overview,
        merged_df_security,
        df_PL_BB_Results,
        df_principle_obligations,
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
        calculated_df_Availability_Borrower,
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
