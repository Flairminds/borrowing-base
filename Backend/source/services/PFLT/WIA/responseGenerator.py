from numerize import numerize

from source.concentration_test_application import ConcentraionTestFormatter

"""
"card_data": {
        "Advance Outstandings": [
            {
                "data": "$218.86M"
            }
        ],
        "Availability": [
            {
                "data": "$62.44M"
            }
        ],
        "Borrowing Base": [
            {
                "data": "$414.58M"
            }
        ],
        "Maximum Available Amount": [
            {
                "data": "$281.31M"
            }
        ],
        "Total Credit Facility Balance": [
            {
                "data": "$210.9M"
            }
        ],
        "ordered_card_names": [
            "Borrowing Base",
            "Maximum Available Amount",
            "Advance Outstandings",
            "Availability",
            "Total Credit Facility Balance"
        ]
    }

---------------------------------WIA-----------------------------
"card_data": {
        "Availability": [
            {
                "changeInValue": true,
                "data": "$0",
                "prevValue": "$0"
            }
        ],
        "Leverage BB": [
            {
                "changeInValue": true,
                "data": "$63.58M",
                "percentageChange": "13.15%",
                "prevValue": "$56.2M"
            }
        ],
        "Obligors net capital": [
            {
                "changeInValue": true,
                "data": "$60M",
                "prevValue": "$60M"
            }
        ],
        "Subscription BB": [
            {
                "changeInValue": true,
                "data": "$30.09M",
                "prevValue": "$30.09M"
            }
        ],
        "Total BB": [
            {
                "changeInValue": true,
                "data": "$93.67M",
                "percentageChange": "8.56%",
                "prevValue": "$86.28M"
            }
        ],
        "ordered_card_names": [
            "Total BB",
            "Leverage BB",
            "Subscription BB",
            "Availability",
            "Obligors net capital"
        ]
    }


"""


def get_card_data(initial_xl_df_map, calculated_xl_df_map):
    initial_borrowing_base_df = initial_xl_df_map["Borrowing Base"]
    calculated_borrowing_base_df = calculated_xl_df_map["Borrowing Base"]

    initial_Credit_Balance_Projection_df = initial_xl_df_map[
        "Credit Balance Projection"
    ]
    calculated_Credit_Balance_Projection_df = calculated_xl_df_map[
        "Credit Balance Projection"
    ]

    card_data = {
        "Advance Outstandings": [
            {
                "changeInValue": 
                    calculated_borrowing_base_df.loc[calculated_borrowing_base_df["Terms"]== "Advances Outstanding as of & TEXT", "Values"].values[0] != initial_borrowing_base_df.loc[initial_borrowing_base_df["Terms"]== "Advances Outstanding as of & TEXT", "Values"].values[0],
                "data": "$"
                + numerize.numerize(
                    calculated_borrowing_base_df.loc[
                        calculated_borrowing_base_df["Terms"]
                        == "Advances Outstanding as of & TEXT",
                        "Values",
                    ].values[0]
                ),
                "prevValue": "$"
                + numerize.numerize(
                    initial_borrowing_base_df.loc[
                        initial_borrowing_base_df["Terms"]
                        == "Advances Outstanding as of & TEXT",
                        "Values",
                    ].values[0]
                ),
                "percentageChange": 
                    '{:.2%}'.format(((calculated_borrowing_base_df.loc[calculated_borrowing_base_df["Terms"]== "Advances Outstanding as of & TEXT", "Values"].values[0] - initial_borrowing_base_df.loc[initial_borrowing_base_df["Terms"]== "Advances Outstanding as of & TEXT", "Values"].values[0]) / (initial_borrowing_base_df.loc[initial_borrowing_base_df["Terms"]== "Advances Outstanding as of & TEXT", "Values"].values[0]))),
            }
        ],
        "Availability": [
            {
                "changeInValue": 
                    calculated_borrowing_base_df.loc[calculated_borrowing_base_df["Terms"]== "AVAILABILITY - (a) minus (b)", "Values"].values[0] != initial_borrowing_base_df.loc[initial_borrowing_base_df["Terms"]=="AVAILABILITY - (a) minus (b)", "Values"].values[0],
                "data": numerize.numerize(
                    calculated_borrowing_base_df.loc[
                        calculated_borrowing_base_df["Terms"]
                        == "AVAILABILITY - (a) minus (b)",
                        "Values",
                    ].values[0]
                ),
                "prevValue": "$"
                + numerize.numerize(
                    initial_borrowing_base_df.loc[
                        initial_borrowing_base_df["Terms"]
                        == "AVAILABILITY - (a) minus (b)",
                        "Values",
                    ].values[0]
                ),
                "percentageChange":
                    '{:.2%}'.format(((calculated_borrowing_base_df.loc[calculated_borrowing_base_df["Terms"]== "AVAILABILITY - (a) minus (b)", "Values"].values[0] - initial_borrowing_base_df.loc[initial_borrowing_base_df["Terms"]=="AVAILABILITY - (a) minus (b)", "Values"].values[0])/initial_borrowing_base_df.loc[initial_borrowing_base_df["Terms"]=="AVAILABILITY - (a) minus (b)", "Values"].values[0]))
            }
        ],
        "Borrowing Base": [
            {
                "changeInValue": 
                    calculated_borrowing_base_df.loc[calculated_borrowing_base_df["Terms"]=="BORROWING BASE - (A) minus (B) minus (A)(iv)", "Values"].values[0] != initial_borrowing_base_df.loc[initial_borrowing_base_df["Terms"]=="BORROWING BASE - (A) minus (B) minus (A)(iv)", "Values"].values[0],
                "data": "$"
                + numerize.numerize(
                    calculated_borrowing_base_df.loc[
                        calculated_borrowing_base_df["Terms"]
                        == "BORROWING BASE - (A) minus (B) minus (A)(iv)",
                        "Values",
                    ].values[0]
                ),
                "prevValue": "$"
                + numerize.numerize(
                    initial_borrowing_base_df.loc[
                        initial_borrowing_base_df["Terms"]
                        == "BORROWING BASE - (A) minus (B) minus (A)(iv)",
                        "Values",
                    ].values[0]
                ),
                "percentageChange": 
                    '{:.2%}'.format(((calculated_borrowing_base_df.loc[calculated_borrowing_base_df["Terms"]=="BORROWING BASE - (A) minus (B) minus (A)(iv)", "Values"].values[0] - initial_borrowing_base_df.loc[initial_borrowing_base_df["Terms"]=="BORROWING BASE - (A) minus (B) minus (A)(iv)", "Values"].values[0]) / initial_borrowing_base_df.loc[initial_borrowing_base_df["Terms"]=="BORROWING BASE - (A) minus (B) minus (A)(iv)", "Values"].values[0]))
            }
        ],
        "Maximum Available Amount": [
            {
                "changeInValue": 
                    calculated_borrowing_base_df.loc[calculated_borrowing_base_df["Terms"]=="MAXIMUM AVAILABLE AMOUNT - Least of (A), (B) and (C)", "Values"].values[0] != initial_borrowing_base_df.loc[initial_borrowing_base_df["Terms"]=="MAXIMUM AVAILABLE AMOUNT - Least of (A), (B) and (C)", "Values"].values[0],
                "data": "$"
                + numerize.numerize(
                    calculated_borrowing_base_df.loc[
                        calculated_borrowing_base_df["Terms"]
                        == "MAXIMUM AVAILABLE AMOUNT - Least of (A), (B) and (C)",
                        "Values",
                    ].values[0]
                ),
                "prevValue": "$"
                + numerize.numerize(
                    initial_borrowing_base_df.loc[
                        initial_borrowing_base_df["Terms"]
                        == "MAXIMUM AVAILABLE AMOUNT - Least of (A), (B) and (C)",
                        "Values",
                    ].values[0]
                ),
                "percentageChange": 
                    '{:.2%}'.format(((calculated_borrowing_base_df.loc[calculated_borrowing_base_df["Terms"]=="MAXIMUM AVAILABLE AMOUNT - Least of (A), (B) and (C)", "Values"].values[0] - initial_borrowing_base_df.loc[initial_borrowing_base_df["Terms"]=="MAXIMUM AVAILABLE AMOUNT - Least of (A), (B) and (C)", "Values"].values[0])/initial_borrowing_base_df.loc[initial_borrowing_base_df["Terms"]=="MAXIMUM AVAILABLE AMOUNT - Least of (A), (B) and (C)", "Values"].values[0]))
            }
        ],
        "Total Credit Facility Balance": [
            {
                "changeInValue": sum(calculated_Credit_Balance_Projection_df["Exchange Rates"] * calculated_Credit_Balance_Projection_df["Projected Credit Facility Balance"].tolist()) != sum(initial_Credit_Balance_Projection_df["Exchange Rates"] * initial_Credit_Balance_Projection_df["Projected Credit Facility Balance"].tolist()),
                "data": "$"
                + numerize.numerize(
                    sum(
                        calculated_Credit_Balance_Projection_df["Exchange Rates"]
                        * calculated_Credit_Balance_Projection_df[
                            "Projected Credit Facility Balance"
                        ].tolist()
                    )
                ),
                "prevValue": "$"
                + numerize.numerize(
                    sum(
                        initial_Credit_Balance_Projection_df["Exchange Rates"]
                        * initial_Credit_Balance_Projection_df[
                            "Projected Credit Facility Balance"
                        ].tolist()
                    )
                ),
                "percentageChange": 
                    '{:.2%}'.format(((sum(calculated_Credit_Balance_Projection_df["Exchange Rates"] * calculated_Credit_Balance_Projection_df["Projected Credit Facility Balance"].tolist()) - sum(initial_Credit_Balance_Projection_df["Exchange Rates"] * initial_Credit_Balance_Projection_df["Projected Credit Facility Balance"].tolist())) / sum(initial_Credit_Balance_Projection_df["Exchange Rates"] * initial_Credit_Balance_Projection_df["Projected Credit Facility Balance"].tolist())))
            }
        ],
        "ordered_card_names": [
            "Borrowing Base",
            "Maximum Available Amount",
            "Advance Outstandings",
            "Availability",
            "Total Credit Facility Balance",
        ]
    }
    return card_data


def get_concentration_test_data(initial_xl_df_map, calculated_xl_df_map):
    concentration_test_df = calculated_xl_df_map["Concentration Test"]
    concentraion_test_formatter = ConcentraionTestFormatter(concentration_test_df)
    concentration_test_data = concentraion_test_formatter.convert_to_std_table_format()
    return concentration_test_data


def get_principle_obligation_data(initial_xl_df_map, calculated_xl_df_map):
    Credit_Balance_Projection_df = calculated_xl_df_map["Credit Balance Projection"]
    principle_obligation_data = {
        column: [
            {
                "data": (
                    "{:.2f}%".format(round(cell * 100, 2))
                    if column == "Exchange Rates"
                    else (
                        "$" + numerize.numerize(cell)
                        if type(cell) == int or type(cell) == float
                        else cell
                    )
                )
            }
            for cell in Credit_Balance_Projection_df[column]
        ]
        for column in Credit_Balance_Projection_df.columns.tolist()
    }
    principle_obligation_data["columns"] = [
        {"data": Credit_Balance_Projection_df.columns.tolist()}
    ]
    return principle_obligation_data


def get_security_chart_data(initial_xl_df_map, calculated_xl_df_map):
    initial_loan_list_df = initial_xl_df_map["Loan List"].copy(deep=True)
    calculated_loan_list_df = calculated_xl_df_map["Loan List"].copy(deep=True)

    initial_loan_list_df = initial_loan_list_df[
        ["Borrowing Base", "Loan Type (Term / Delayed Draw / Revolver)"]
    ]
    calculated_loan_list_df = calculated_loan_list_df[
        ["Borrowing Base", "Loan Type (Term / Delayed Draw / Revolver)"]
    ]

    initial_loan_list_df.rename(
        columns={"Loan Type (Term / Delayed Draw / Revolver)": "Loan Type"},
        inplace=True,
    )
    calculated_loan_list_df.rename(
        columns={"Loan Type (Term / Delayed Draw / Revolver)": "Loan Type"},
        inplace=True,
    )

    initial_security_bb_sum = (
        initial_loan_list_df.groupby("Loan Type")["Borrowing Base"].sum().reset_index()
    )
    initial_security_bb_sum = initial_security_bb_sum.sort_values(
        "Borrowing Base", ascending=False
    )

    calculated_security_bb_sum = (
        calculated_loan_list_df.groupby("Loan Type")["Borrowing Base"]
        .sum()
        .reset_index()
    )
    calculated_security_bb_sum = calculated_security_bb_sum.sort_values(
        "Borrowing Base", ascending=False
    )

    merged_security_bb_df = calculated_security_bb_sum.merge(
        initial_security_bb_sum, on="Loan Type", how="left"
    )

    merged_security_bb_df.rename(
        columns={
            "Borrowing Base_x": "Updated Borrowing Base",
            "Borrowing Base_y": "Borrowing Base",
        },
        inplace=True,
    )

    merged_security_bb_df[["Updated Borrowing Base", "Borrowing Base"]] = (
        merged_security_bb_df[["Updated Borrowing Base", "Borrowing Base"]].fillna(0)
    )

    chart_data = merged_security_bb_df.to_dict(orient="records")
    security_graph_data = {
        "security_chart_data": chart_data,
        "x_axis": ["Updated Borrowing Base", "Borrowing Base"],
        "y_axis": "Loan Type",
    }
    return security_graph_data


def get_segmentation_chart_data(initial_xl_df_map, calculated_xl_df_map):
    initial_loan_list_df = initial_xl_df_map["Loan List"].copy(deep=True)
    calculated_loan_list_df = calculated_xl_df_map["Loan List"].copy(deep=True)

    initial_loan_list_df = initial_loan_list_df[["Borrowing Base", "Obligor Industry"]]
    calculated_loan_list_df = calculated_loan_list_df[
        ["Borrowing Base", "Obligor Industry"]
    ]

    initial_loan_list_df.rename(
        columns={"Obligor Industry": "name"},
        inplace=True,
    )
    calculated_loan_list_df.rename(
        columns={"Obligor Industry": "name"},
        inplace=True,
    )

    initial_segmentation_bb_sum = (
        initial_loan_list_df.groupby("name")["Borrowing Base"].sum().reset_index()
    )
    initial_segmentation_bb_sum = initial_segmentation_bb_sum.sort_values(
        "Borrowing Base", ascending=False
    )

    calculated_segmentation_bb_sum = (
        calculated_loan_list_df.groupby("name")["Borrowing Base"].sum().reset_index()
    )
    calculated_segmentation_bb_sum = calculated_segmentation_bb_sum.sort_values(
        "Borrowing Base", ascending=False
    )

    merged_segmentation_bb_df = calculated_segmentation_bb_sum.merge(
        initial_segmentation_bb_sum, on="name", how="left"
    )

    merged_segmentation_bb_df.rename(
        columns={
            "Borrowing Base_x": "Updated Borrowing Base",
            "Borrowing Base_y": "Borrowing Base",
        },
        inplace=True,
    )

    merged_segmentation_bb_df[["Updated Borrowing Base", "Borrowing Base"]] = (
        merged_segmentation_bb_df[["Updated Borrowing Base", "Borrowing Base"]].fillna(
            0
        )
    )

    chart_data = merged_segmentation_bb_df.to_dict(orient="records")
    segmentation_graph_data = {
        "segmentation_chart_data": chart_data,
        "x_axis": ["Updated Borrowing Base", "Borrowing Base"],
        "y_axis": "name",
    }
    return segmentation_graph_data


def get_security_bb_sum(security_bb):
    security_bb = security_bb[
        ["Borrowing Base", "Loan Type (Term / Delayed Draw / Revolver)"]
    ]
    security_bb.rename(
        columns={"Loan Type (Term / Delayed Draw / Revolver)": "Security"},
        inplace=True,
    )
    security_bb_sum = (
        security_bb.groupby("Security")["Borrowing Base"].sum().reset_index()
    )
    security_bb_sum = security_bb_sum.sort_values("Borrowing Base", ascending=False)

    return security_bb_sum


def get_security_data(initial_xl_df_map, calculated_xl_df_map):
    initial_loan_list_df = initial_xl_df_map["Loan List"].copy(deep=True)
    calculated_loan_list_df = calculated_xl_df_map["Loan List"].copy(deep=True)

    initial_security_bb_sum = get_security_bb_sum(initial_loan_list_df)
    calculated_security_bb_sum = get_security_bb_sum(calculated_loan_list_df)

    initial_security_bb_sum["% of Borrowing Base"] = (
        initial_security_bb_sum["Borrowing Base"]
        / initial_security_bb_sum["Borrowing Base"].sum()
    )

    calculated_security_bb_sum["% of Borrowing Base"] = (
        calculated_security_bb_sum["Borrowing Base"]
        / calculated_security_bb_sum["Borrowing Base"].sum()
    )

    merged_security_bb_df = calculated_security_bb_sum.merge(
        initial_security_bb_sum, on="Security", how="left"
    )

    merged_security_bb_df.rename(
        columns={
            "Borrowing Base_x": "Updated Borrowing Base",
            "Borrowing Base_y": "Borrowing Base",
            "% of Borrowing Base_x": "Updated % of Borrowing Base",
            "% of Borrowing Base_y": "initial % of Borrowing Base",
        },
        inplace=True,
    )
    cols_to_fillna = [
        "Updated Borrowing Base",
        "Updated % of Borrowing Base",
        "Borrowing Base",
        "initial % of Borrowing Base",
    ]

    merged_security_bb_df[cols_to_fillna] = merged_security_bb_df[
        cols_to_fillna
    ].fillna(0)

    percent_of_borrowing_base = [
        {
            "data": "{:.2f}%".format(
                merged_security_bb_df["Updated % of Borrowing Base"][i] * 100
            ),
            "prevValue": "{:.2f}%".format(
                merged_security_bb_df["initial % of Borrowing Base"][i] * 100
            ),
            "percentageChange": "{:.2f}%".format(
                (
                    (
                        (
                            merged_security_bb_df["Updated % of Borrowing Base"][i]
                            - merged_security_bb_df["initial % of Borrowing Base"][i]
                        )
                        / merged_security_bb_df["initial % of Borrowing Base"][i]
                    )
                    * 100
                )
                if merged_security_bb_df["initial % of Borrowing Base"][i] != 0
                else 0
            ),
        }
        for i in range(len(merged_security_bb_df))
    ]

    borrowing_base = [
        {
            "data": "$"
            + numerize.numerize(merged_security_bb_df["Updated Borrowing Base"][i]),
            "percentageChange": "{:.2f}%".format(
                (
                    (
                        (
                            merged_security_bb_df["Updated Borrowing Base"][i]
                            - merged_security_bb_df["Borrowing Base"][i]
                        )
                        / merged_security_bb_df["Borrowing Base"][i]
                    )
                    * 100
                )
                if merged_security_bb_df["Borrowing Base"][i] != 0
                else 0
            ),
            "prevValue": "$"
            + numerize.numerize(merged_security_bb_df["Borrowing Base"][i]),
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
            "% of Borrowing Base": "{:.2f}%".format(
                merged_security_bb_df["Updated % of Borrowing Base"].sum()
            ),
            "Borrowing Base": "$"
            + numerize.numerize(merged_security_bb_df["Updated Borrowing Base"].sum()),
        }
    }

    columns = [{"data": ["Security", "Borrowing Base", "% of Borrowing Base"]}]

    security_data = {
        "% of Borrowing Base": percent_of_borrowing_base,
        "Borrowing Base": borrowing_base,
        "Security": secuity,
        "Total": total,
        "columns": columns,
    }
    return security_data
    # (current - previous)/previous


def get_segmentation_overview_data(initial_xl_df_map, calculated_xl_df_map):
    initial_loan_list_df = initial_xl_df_map["Loan List"].copy(deep=True)
    calculated_loan_list_df = calculated_xl_df_map["Loan List"].copy(deep=True)

    initial_loan_list_df = initial_loan_list_df[["Borrowing Base", "Obligor Industry"]]
    calculated_loan_list_df = calculated_loan_list_df[
        ["Borrowing Base", "Obligor Industry"]
    ]

    initial_loan_list_df.rename(
        columns={"Obligor Industry": "name"},
        inplace=True,
    )
    calculated_loan_list_df.rename(
        columns={"Obligor Industry": "name"},
        inplace=True,
    )

    initial_segmentation_bb_sum = (
        initial_loan_list_df.groupby("name")["Borrowing Base"].sum().reset_index()
    )
    initial_segmentation_bb_sum = initial_segmentation_bb_sum.sort_values(
        "Borrowing Base", ascending=False
    )

    calculated_segmentation_bb_sum = (
        calculated_loan_list_df.groupby("name")["Borrowing Base"].sum().reset_index()
    )
    calculated_segmentation_bb_sum = calculated_segmentation_bb_sum.sort_values(
        "Borrowing Base", ascending=False
    )

    initial_segmentation_bb_sum["% of Borrowing Base"] = (
        initial_segmentation_bb_sum["Borrowing Base"]
        / initial_segmentation_bb_sum["Borrowing Base"].sum()
    )

    calculated_segmentation_bb_sum["% of Borrowing Base"] = (
        calculated_segmentation_bb_sum["Borrowing Base"]
        / calculated_segmentation_bb_sum["Borrowing Base"].sum()
    )

    merged_segmentation_bb_df = calculated_segmentation_bb_sum.merge(
        initial_segmentation_bb_sum, on="name", how="left"
    )

    merged_segmentation_bb_df.rename(
        columns={
            "Borrowing Base_x": "Updated Borrowing Base",
            "Borrowing Base_y": "Borrowing Base",
            "% of Borrowing Base_x": "Updated % of Borrowing Base",
            "% of Borrowing Base_y": "initial % of Borrowing Base",
        },
        inplace=True,
    )
    cols_to_fillna = [
        "Updated Borrowing Base",
        "Updated % of Borrowing Base",
        "Borrowing Base",
        "initial % of Borrowing Base",
    ]

    merged_segmentation_bb_df[cols_to_fillna] = merged_segmentation_bb_df[
        cols_to_fillna
    ].fillna(0)

    unadjusted_percent_of_bb = [
        {
            "data": "{:.2f}%".format(
                merged_segmentation_bb_df["Updated % of Borrowing Base"][i] * 100
            ),
            "prevValue": "{:.2f}%".format(
                merged_segmentation_bb_df["initial % of Borrowing Base"][i] * 100
            ),
            "percentageChange": "{:.2f}%".format(
                (
                    (
                        (
                            merged_segmentation_bb_df["Updated % of Borrowing Base"][i]
                            - merged_segmentation_bb_df["initial % of Borrowing Base"][
                                i
                            ]
                        )
                        / merged_segmentation_bb_df["initial % of Borrowing Base"][i]
                    )
                    * 100
                )
                if merged_segmentation_bb_df["initial % of Borrowing Base"][i] != 0
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
        {"data": merged_segmentation_bb_df["name"][i], "changeInValue": True}
        for i in range(len(merged_segmentation_bb_df))
    ]

    total = {
        "data": {
            "Industry": "Total",
            "Unadjusted % of BB": "{:.2f}%".format(
                merged_segmentation_bb_df["Updated % of Borrowing Base"].sum() * 100
            ),
            "Unadjusted BB": "$"
            + numerize.numerize(
                merged_segmentation_bb_df["Updated Borrowing Base"].sum()
            ),
        }
    }

    columns = [{"data": ["Industry", "Unadjusted BB", "Unadjusted % of BB"]}]

    segmentation_overview_data = {
        "Industry": industries,
        "Unadjusted BB": borrowing_base,
        "Unadjusted % of BB": unadjusted_percent_of_bb,
        "Total": total,
        "columns": columns,
    }
    return segmentation_overview_data


def generateResponse(initial_xl_df_map, calculated_xl_df_map):
    card_data = get_card_data(initial_xl_df_map, calculated_xl_df_map)
    concentration_test_data = get_concentration_test_data(
        initial_xl_df_map, calculated_xl_df_map
    )
    principle_obligation_data = get_principle_obligation_data(
        initial_xl_df_map, calculated_xl_df_map
    )
    security_chart_data = get_security_chart_data(
        initial_xl_df_map, calculated_xl_df_map
    )
    segmentation_chart_data = get_segmentation_chart_data(
        initial_xl_df_map, calculated_xl_df_map
    )
    security_data = get_security_data(initial_xl_df_map, calculated_xl_df_map)
    segmentation_overview_data = get_segmentation_overview_data(
        initial_xl_df_map, calculated_xl_df_map
    )
    

    response_data = {
        "card_data": card_data,
        "concentration_test_data": concentration_test_data,
        "principal_obligation_data": principle_obligation_data,
        "security_chart_data": security_chart_data,
        "segmentation_chart_data": segmentation_chart_data,
        "security_data": security_data,
        "segmentation_overview_data": segmentation_overview_data,
    }
    return response_data
