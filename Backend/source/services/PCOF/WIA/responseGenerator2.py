from numerize import numerize

from source.concentration_test_application import ConcentraionTestFormatter

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

def get_card_data(initial_xl_df_map, calculated_xl_df_map):
    df_Availability_Borrower = initial_xl_df_map["df_Availability_Borrower"]
    Updated_df_Availability_Borrower = calculated_xl_df_map["Updated_df_Availability_Borrower"]
    df_principle_obligations = calculated_xl_df_map["df_principle_obligations"]
    df_principle_obligations["Dollar Equivalent"] = df_principle_obligations["Dollar Equivalent"].fillna(0)
    dollarequivalent = df_principle_obligations["Dollar Equivalent"].tolist()
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
    return card_data

def get_principal_obligation_data(initial_xl_df_map, calculated_xl_df_map):
    df_principle_obligations = calculated_xl_df_map["df_principle_obligations"]
    df_principle_obligations = df_principle_obligations.fillna(0)
    principal_obligation_data = {
        column: [
            {
                "data": numerize.numerize(cell) 
                            if column in ["Amount", "Dollar equivalent"] 
                            else
                                "{:.2f}%".format(round(cell, 2))
                                    if column in ["Spot rate"]
                                    else
                                        cell

            } for cell in df_principle_obligations[column]
        ] for column in df_principle_obligations.columns 
    }
    principal_obligation_data["columns"] = [{"data": df_principle_obligations.columns.tolist()}]
    return principal_obligation_data

def get_security_chart_data(initial_xl_df_map, calculated_xl_df_map):
    initial_df_security = initial_xl_df_map["df_security"]
    calculated_df_security = calculated_xl_df_map["Updated_df_security"]

    initial_df_security = initial_df_security[initial_df_security["Security"]!="Total"]
    calculated_df_security = calculated_df_security[calculated_df_security["Security"]!="Total"]

    initial_security_bb_sum = (initial_df_security.groupby("Security")["Security BB"].sum().reset_index())
    calculated_security_bb_sum = (calculated_df_security.groupby("Security")["Security BB"].sum().reset_index())

    merged_security_bb_df = calculated_security_bb_sum.merge(initial_security_bb_sum, on="Security", how="left")

    merged_security_bb_df.rename(
        columns={
            "Security BB_x": "Updated Borrowing Base",
            "Security BB_y": "Borrowing Base",
        },
        inplace=True,
    )

    merged_security_bb_df[["Updated Borrowing Base", "Borrowing Base"]] = (merged_security_bb_df[["Updated Borrowing Base", "Borrowing Base"]].fillna(0))

    merged_security_bb_df = merged_security_bb_df.sort_values("Updated Borrowing Base", ascending=False).reset_index()

    chart_data = merged_security_bb_df.to_dict(orient="records")
    security_graph_data = {
        "security_chart_data": chart_data,
        "x_axis": ["Updated Borrowing Base", "Borrowing Base"],
        "y_axis": "Security",
    }
    return security_graph_data

def get_segmentation_chart_data(initial_xl_df_map, calculated_xl_df_map):
    initial_df_segmentation_overview = initial_xl_df_map["df_segmentation_overview"]
    calculated_df_segmentation_overview = calculated_xl_df_map["Updated_df_segmentation_overview"]

    initial_df_segmentation_overview = initial_df_segmentation_overview[initial_df_segmentation_overview["industry"]!="Total"]
    calculated_df_segmentation_overview = calculated_df_segmentation_overview[calculated_df_segmentation_overview["industry"]!="Total"]

    initial_segmentation_bb_sum = initial_df_segmentation_overview.groupby("industry")["BB"].sum().reset_index()
    calculated_segmentation_bb_sum = calculated_df_segmentation_overview.groupby("industry")["BB"].sum().reset_index()

    initial_segmentation_bb_sum = initial_segmentation_bb_sum.sort_values("BB", ascending=False)
    calculated_segmentation_bb_sum = initial_segmentation_bb_sum.sort_values("BB", ascending=False)

    merged_segmentation_bb_df = calculated_segmentation_bb_sum.merge(initial_segmentation_bb_sum, on="industry", how="left")

    merged_segmentation_bb_df = merged_segmentation_bb_df.rename(columns={"BB_x": "Updated Borrowing Base","BB_y": "Borrowing Base"})

    merged_segmentation_bb_df[["Updated Borrowing Base", "Borrowing Base"]] = (
        merged_segmentation_bb_df[["Updated Borrowing Base", "Borrowing Base"]].fillna(0)
    )

    chart_data = merged_segmentation_bb_df.to_dict(orient="records")
    segmentation_graph_data = {
        "segmentation_chart_data": chart_data,
        "x_axis": ["Updated Borrowing Base", "Borrowing Base"],
        "y_axis": "industry",
    }
    return segmentation_graph_data


def get_concentration_test_data(initial_xl_df_map, calculated_xl_df_map):
    concentration_test_df = calculated_xl_df_map["Updated_df_PL_BB_Results"]
    concentraion_test_formatter = ConcentraionTestFormatter(concentration_test_df)
    concentration_test_data = concentraion_test_formatter.convert_to_std_table_format()
    return concentration_test_data

def get_security_data(initial_xl_df_map, calculated_xl_df_map):
    initial_df_security = initial_xl_df_map["df_security"]
    calculated_df_security = calculated_xl_df_map["Updated_df_security"]

    initial_df_security = initial_df_security[initial_df_security["Security"]!="Total"]
    calculated_df_security = calculated_df_security[calculated_df_security["Security"]!="Total"]

    initial_security_bb_sum = (initial_df_security.groupby("Security")["Security BB", "Security Percent of BB"].sum().reset_index())
    calculated_security_bb_sum = (calculated_df_security.groupby("Security")["Security BB", "Security Percent of BB"].sum().reset_index())

    merged_security_bb_df = calculated_security_bb_sum.merge(initial_security_bb_sum, on="Security", how="left")

    merged_security_bb_df = merged_security_bb_df.rename(
        columns={
            "Security BB_x": "Updated Borrowing Base",
            "Security BB_y": "Borrowing Base",
            "Security Percent of BB_x": "Updated Percent of BB",
            "Security Percent of BB_y": "Percent of BB"
        }
    )

    cols_to_fillna = [
        "Updated Borrowing Base", "Borrowing Base", "Updated Percent of BB", "Percent of BB"]

    merged_security_bb_df[cols_to_fillna] = merged_security_bb_df[cols_to_fillna].fillna(0)
    merged_security_bb_df = merged_security_bb_df.sort_values("Updated Borrowing Base", ascending=False).reset_index()

    percent_of_borrowing_base = [
        {
            "data": "{:.2f}%".format(merged_security_bb_df["Updated Percent of BB"][i] * 100),
            "prevValue": "{:.2f}%".format(merged_security_bb_df["Percent of BB"][i] * 100),
            "percentageChange": "{:.2f}%".format(
                (
                    (
                        (merged_security_bb_df["Updated Percent of BB"][i]  - merged_security_bb_df["Percent of BB"][i]) / merged_security_bb_df["Percent of BB"][i]
                    ) * 100
                )
                if merged_security_bb_df["Percent of BB"][i] != 0
                else 0
            ),
        }
        for i in range(len(merged_security_bb_df))
    ]

    borrowing_base = [
        {
            "data": "$" + numerize.numerize(merged_security_bb_df["Updated Borrowing Base"][i]),
            "percentageChange": "{:.2f}%".format(
                (
                    (
                        (merged_security_bb_df["Updated Borrowing Base"][i] - merged_security_bb_df["Borrowing Base"][i]) / merged_security_bb_df["Borrowing Base"][i]
                    ) * 100
                )
                if merged_security_bb_df["Borrowing Base"][i] != 0
                else 0
            ),
            "prevValue": "$" + numerize.numerize(merged_security_bb_df["Borrowing Base"][i]),
        }
        for i in range(len(merged_security_bb_df))
    ]

    secuity = [
        {"data": merged_security_bb_df["Security"][i], "changeInValue": True}
        for i in range(len(merged_security_bb_df))
    ]

    total = {
        "data": {
            "Security": "Total",
            "% Borrowing Base": "{:.2f}%".format(merged_security_bb_df["Updated Percent of BB"].sum()),
            "Borrowing Base": "$" + numerize.numerize(merged_security_bb_df["Updated Borrowing Base"].sum()),
        }
    }

    columns = [{"data": ["Security", "Borrowing Base", "% Borrowing Base"]}]

    security_data = {
        "% Borrowing Base": percent_of_borrowing_base,
        "Borrowing Base": borrowing_base,
        "Security": secuity,
        "Total": total,
        "columns": columns,
    }
    return security_data

def get_segmentation_overview_data(initial_xl_df_map, calculated_xl_df_map):
    initial_df_segmentation_overview = initial_xl_df_map["df_segmentation_overview"]
    calculated_df_segmentation_overview = calculated_xl_df_map["Updated_df_segmentation_overview"]

    initial_df_segmentation_overview = initial_df_segmentation_overview[initial_df_segmentation_overview["industry"]!="Total"]
    calculated_df_segmentation_overview = calculated_df_segmentation_overview[calculated_df_segmentation_overview["industry"]!="Total"]

    initial_segmentation_bb_sum = initial_df_segmentation_overview.groupby("industry")["BB", "percent of BB"].sum().reset_index()
    calculated_segmentation_bb_sum = calculated_df_segmentation_overview.groupby("industry")["BB", "percent of BB"].sum().reset_index()

    initial_segmentation_bb_sum = initial_segmentation_bb_sum.sort_values("BB", ascending=False)
    calculated_segmentation_bb_sum = initial_segmentation_bb_sum.sort_values("BB", ascending=False)

    merged_segmentation_bb_df = calculated_segmentation_bb_sum.merge(initial_segmentation_bb_sum, on="industry", how="left")

    merged_segmentation_bb_df = merged_segmentation_bb_df.rename(columns={"BB_x": "Updated Borrowing Base","BB_y": "Borrowing Base", "percent of BB_x": "Updated percent of BB", "percent of BB_y": "percent of BB"})

    merged_segmentation_bb_df[["Updated Borrowing Base", "Borrowing Base", "Updated percent of BB", "percent of BB"]] = (merged_segmentation_bb_df[["Updated Borrowing Base", "Borrowing Base", "Updated percent of BB", "percent of BB"]].fillna(0))

    unadjusted_percent_of_bb = [
        {
            "data": "{:.2f}%".format(
                merged_segmentation_bb_df["Updated percent of BB"][i] * 100
            ),
            "prevValue": "{:.2f}%".format(
                merged_segmentation_bb_df["percent of BB"][i] * 100
            ),
            "percentageChange": "{:.2f}%".format(
                (
                    (
                        (
                            merged_segmentation_bb_df["Updated percent of BB"][i]
                            - merged_segmentation_bb_df["percent of BB"][
                                i
                            ]
                        )
                        / merged_segmentation_bb_df["percent of BB"][i]
                    )
                    * 100
                )
                if merged_segmentation_bb_df["percent of BB"][i] != 0
                else 0
            ),
        }
        for i in range(len(merged_segmentation_bb_df))
    ]

    borrowing_base = [
        {
            "data": "$"
            + numerize.numerize(merged_segmentation_bb_df["Updated Borrowing Base"][i]),
            "percentageChange": "{:.2f}%".format(
                (
                    (
                        (
                            merged_segmentation_bb_df["Updated Borrowing Base"][i]
                            - merged_segmentation_bb_df["Borrowing Base"][i]
                        )
                        / merged_segmentation_bb_df["Borrowing Base"][i]
                    )
                    * 100
                )
                if merged_segmentation_bb_df["Borrowing Base"][i] != 0
                else 0
            ),
            "prevValue": "$"
            + numerize.numerize(merged_segmentation_bb_df["Borrowing Base"][i]),
        }
        for i in range(len(merged_segmentation_bb_df))
    ]

    industries = [
        {"data": merged_segmentation_bb_df["industry"][i], "changeInValue": True}
        for i in range(len(merged_segmentation_bb_df))
    ]

    total = {
        "data": {
            "Industry": "Total",
            "% Borrowing Base": "{:.2f}%".format(
                merged_segmentation_bb_df["Updated percent of BB"].sum() * 100
            ),
            "Borrowing Base": "$"
            + numerize.numerize(
                merged_segmentation_bb_df["Updated Borrowing Base"].sum()
            ),
        }
    }

    columns = [{"data": ["Industry", "Borrowing Base", "% Borrowing Base"]}]

    segmentation_overview_data = {
        "Industry": industries,
        "Borrowing Base": borrowing_base,
        "% Borrowing Base": unadjusted_percent_of_bb,
        "Total": total,
        "columns": columns,
    }
    return segmentation_overview_data


def generate_response(initial_xl_df_map, calculated_xl_df_map):
    card_data = get_card_data(initial_xl_df_map, calculated_xl_df_map)
    principal_obligation_data = get_principal_obligation_data(initial_xl_df_map, calculated_xl_df_map)
    security_chart_data = get_security_chart_data(initial_xl_df_map, calculated_xl_df_map)
    segmentation_chart_data = get_segmentation_chart_data(initial_xl_df_map, calculated_xl_df_map)
    concentration_test_data = get_concentration_test_data(initial_xl_df_map, calculated_xl_df_map)
    security_data = get_security_data(initial_xl_df_map, calculated_xl_df_map)
    segmentation_overview_data = get_segmentation_overview_data(initial_xl_df_map, calculated_xl_df_map)

    return (card_data, segmentation_overview_data, security_data, concentration_test_data, principal_obligation_data, segmentation_chart_data, security_chart_data)

