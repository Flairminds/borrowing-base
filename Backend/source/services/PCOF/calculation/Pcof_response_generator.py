import pandas as pd
from numerize import numerize

from source.concentration_test_application import ConcentraionTestFormatter


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


def generate_response(
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
