import pandas as pd
import math

pd.set_option("display.max_columns", None)

# --------------------------------------------------------------------------------

# BG=IFERROR(IF(#REF!>=Inputs!$D$124,"Yes","No"),"N/A") --for Cash
# BG=IFERROR(IF(AV13>=Inputs1$D$124,"Yes","No"),"N/A")
##AV was given as !REF which could not be interpreted so i used AV from above columns


def EBITDA_Threshold(data, Other_metrics, cash_index):
    try:
        match_other_index = Other_metrics[
            Other_metrics["Other Metrics"] == "Trailing 12-Month EBITDA"
        ].index[0]
        input_trailing_12_month_EBITDA = Other_metrics["values"].iloc[match_other_index]
        if (
            data.loc[cash_index, "Financials LTM EBITDA ($MMs)"]
            >= input_trailing_12_month_EBITDA
        ):
            data.loc[cash_index, "Test 1 EBITDA Threshold"] = "Yes"
        else:
            data.loc[cash_index, "Test 1 EBITDA Threshold"] = "No"
    except:
        data.loc[cash_index, "Test 1 EBITDA Threshold"] = "N/A"
    return data


# df_PL_BB_Build = EBITDA_Threshold(df_PL_BB_Build,df_Inputs_Other_Metrics,cash_index)


def ONW_Adjustments(data, cash_index):
    data.loc[cash_index, "ONW Adjustments % of ONC > 7.5%"] = 0
    data.loc[cash_index, "ONW Adjustments % of ONC > 10%"] = 0
    data.loc[cash_index, "ONW Adjustments > 7.5% ONC Share"] = 0
    data.loc[cash_index, "ONW Adjustments > 10% ONC Share"] = 0
    data.loc[cash_index, "ONW Adjustments ONC haircut for Elig. Amount"] = 0
    return data


# df_PL_BB_Build = ONW_Adjustments(df_PL_BB_Build,cash_index)

# % BB (DQ33)
# DQ33=IFERROR(DP33/$DP$35,"")
# global cash_index
# cash_index = df[df.iloc[:, 0] == "cash"].index[0]


def percentBBCash(dataframe, formula_column, cash_index, target_column):
    # Find the row index where the condition column value is 'cash'
    # row_index = dataframe[dataframe.iloc[:, 0] == condition_value].index[0]

    try:
        # Calculate the result using the formula and assign it to the target column
        result = (
            dataframe.loc[cash_index, formula_column]
            / dataframe["Borrowing Base"].sum()
        )
    except:
        result = ""

    dataframe.loc[cash_index, target_column] = result

    return dataframe


# df_PL_BB_Build = percentBBCash(df_PL_BB_Build, "Borrowing Base",cash_index, "Borrowing % of BB")


# Borrowing Base cash
# DP33=IFERROR(DL33+DM33,"n/a")
def borrowingBaseCash(dataframe, columnDL, columnDM, target_column, cash_index):
    # Calculate the result using the formula and assign it to the target column
    result = [dataframe.loc[cash_index, columnDL], dataframe.loc[cash_index, columnDM]]
    output = sum([i for i in result if not math.isnan(i)])

    dataframe.loc[cash_index, target_column] = output

    return dataframe


# df_PL_BB_Build = borrowingBaseCash(df_PL_BB_Build, "Borrowing Adj. Contribution", "Borrowing Other Adjustment", "Borrowing Base")


# DL33 - Adj. Contribution Cash
# DL33 =IFERROR(((CJ33-DD33-DE33)*CV33)+DI33,0)
def adjContributionCash(
    dataframe, colCJ, colDD, colDE, colCV, colDI, cash_index, target_column
):
    try:
        result = (
            (
                dataframe.loc[cash_index, colCJ]
                - dataframe.loc[cash_index, colDD]
                - dataframe.loc[cash_index, colDE]
            )
            * dataframe.loc[cash_index, colCV]
        ) + dataframe.loc[cash_index, colDI]

    except:
        result = 0

    dataframe.loc[cash_index, target_column] = result

    return dataframe


# df_PL_BB_Build = adjContributionCash(df_PL_BB_Build, "Concentration Adj. Elig. Amount", "ONW Adjustments > 7.5% ONC Share", "ONW Adjustments > 10% ONC Share", "First Lien Adj. Advance Rate", "ONW Adjustments Concentration BB Adj. Contribution", cash_index, "Borrowing Adj. Contribution")


# DK33 - ONW Adjustment
# DK33=DL33-CW33
def onwAdjustmentCash(dataframe, colDL, colCW, cash_index, target_column):
    result = dataframe.loc[cash_index, colDL] - dataframe.loc[cash_index, colCW]

    dataframe.loc[cash_index, target_column] = result

    return dataframe


# df_PL_BB_Build = onwAdjustmentCash(df_PL_BB_Build, "Borrowing Adj. Contribution", "First Lien Contribution", cash_index, "Borrowing ONW Adjustment")

# DH33 - Adj. Contr. % (issuer)
# DH33=+SUMIF($E$7:$E$33,E33,$DG$7:$DG$33)/'PL BB Results'!$F$13
#'ONW Adjustments Adj. Contr. % (issuer)'


def adjContrPercentIssuerCash(
    dataframe, colE, colDG, criteria, df_ObligorNetCapital, target_column, cash_index
):
    filtered_df = dataframe[dataframe[colE] == criteria]

    # Sum the values in the sum_range column of the filtered dataframe
    sumif_value = filtered_df[colDG].sum()
    match_index = df_ObligorNetCapital[
        df_ObligorNetCapital["Obligors' Net Capital"]
        == "Obligors' Net Capital ((a) + (b))"
    ].index[0]
    value = df_ObligorNetCapital["values"].iloc[match_index]
    result = sumif_value / value

    # Add the result value to the 'value' column in the target dataframe at the specified row
    dataframe.at[cash_index, target_column] = result

    return dataframe


# df_PL_BB_Build = adjContrPercentIssuerCash(df_PL_BB_Build, "Investment Name", "ONW Adjustments Adj. Elig. Amount", "cash", df_Obligors_Net_Capital, 'ONW Adjustments Adj. Contr. % (issuer)')

# CY - Second Lien Share
# CY=IF(CO33="n/a","N/A",IF(AND(CO33>0,AK33="First Lien",BG33>Inputs!$D$120),(BG33-Inputs!$D$120)/BG33,0))


def secondLienShareCash(
    df, df_otherMetrics, colCO, colAK, colBG, cash_index, target_column
):
    if df.loc[cash_index, colCO] == "n/a":
        result = "N/A"
    elif (
        df.loc[cash_index, colCO] > 0
        and df.loc[cash_index, colAK] == "First Lien"
        and df.loc[cash_index, colBG]
        > df_otherMetrics.loc[
            df_otherMetrics["Other Metrics"] == "First Lien Leverage Cut-Off Point",
            "Values",
        ].values[0]
    ):
        result = (
            df.loc[cash_index, colBG]
            - df_otherMetrics.loc[
                df["Other Metrics"] == "First Lien Leverage Cut-Off Point", "Values"
            ].values[0]
        ) / df.loc[cash_index, colBG]
    else:
        result = 0

    df.loc[cash_index, target_column] = result

    return df


# df_PL_BB_Build = secondLienShareCash(df_PL_BB_Build, df_Inputs_Other_Metrics, 'Adv. Adv. Rate','Classifications Approved Foreign Jurisdiction', 'Test 1 EBITDA Threshold', cash_index, 'Warehouse Second Lien Share')

# CW33 - Contribution
# CW33=IFERROR(CJ33*CV33,0)


def contributionCash(df, colCJ, colCV, cash_index, target_column):
    try:
        result = df.loc[cash_index, colCJ] * df.loc[cash_index, colCV]
    except:
        result = 0

    df.loc[cash_index, target_column] = result
    return df


# df_PL_BB_Build = contributionCash(df_PL_BB_Build,"Concentration Adj. Elig. Amount","First Lien Adj. Advance Rate", cash_index, "First Lien Contribution")


# O33 = N33
def calculate_Investment_Cost(data, cash_index):
    val = data["Investment Par"].iloc[cash_index]

    data.loc[cash_index, "Investment Cost"] = val

    return data


# df_PL_BB_Build = calculate_Investment_Cost(df_PL_BB_Build, cash_index)
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# P33 =O33
def calculate_Investment_External_Valuation(data, cash_index):
    data = calculate_Investment_Cost(data, cash_index)
    val = data["Investment Cost"].iloc[cash_index]

    data.loc[cash_index, "Investment External Valuation"] = val
    return data


# df_PL_BB_Build = calculate_Investment_External_Valuation(df_PL_BB_Build, cash_index)
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# Q33 = P33
def calculate_Investment_Internal_Valuation(data, cash_index):
    data = calculate_Investment_External_Valuation(data, cash_index)
    val = data["Investment External Valuation"].iloc[cash_index]

    data.loc[cash_index, "Investment Internal Valuation"] = val
    return data


# df_PL_BB_Build = calculate_Investment_Internal_Valuation(df_PL_BB_Build, cash_index)
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# R33 = Q33
def calculate_Investment_FMV(data, cash_index):
    data = calculate_Investment_Internal_Valuation(data, cash_index)
    val = data["Investment Internal Valuation"].iloc[cash_index]

    data.loc[cash_index, "Investment FMV"] = val
    return data


# df_PL_BB_Build = calculate_Investment_FMV(df_PL_BB_Build, cash_index)
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CT33 #Already calculated function
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# AE33
def calculate_Classification_for_BB(data, cash_index):
    data.loc[cash_index, "Classifications Classification for BB"] = "cash"
    return data


# df_PL_BB_Build = calculate_Classification_for_BB(df_PL_BB_Build, cash_index)

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# CV33=IF(CT33<>0,((CT33*CU33)+((1-CT33)*CO33)),CO33)
def calculate_First_Adj_Advance_Rate(data, cash_index):
    ct = data["First Lien Second Lien Share"].iloc[cash_index]
    cu = data["First Lien Second Lien Rate"].iloc[cash_index]
    co = data["Adv. Adv. Rate"].iloc[cash_index]

    if ct != 0:
        val = (ct * cu) + ((1 - ct) * co)
    else:
        val = co

    data.loc[cash_index, "First Lien Adj. Advance Rate"] = val
    return data


# df_PL_BB_Build = calculate_First_Adj_Advance_Rate(df_PL_BB_Build, cash_index)
