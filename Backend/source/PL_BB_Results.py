import pandas as pd
import numpy as np
import math


# Minimum eligible issuers value for PL BB Result sheet
def minEligibleIssuersActual(df, df2, search_value, col_Actual):
    """`Actual value `Min. E`ligible Issuers (#)` in PL BB Results table is derived from maximum value of  `Eligible Issuers` from PL BB Build table

    `Actual` = max(`Eligible Issuers`)

    """
    # Find the row index where the search_value is present in the first column
    row_index = df[df.iloc[:, 0] == search_value].index

    # max_value = df2['Issuer'].max()
    max_value = df2["Eligible Issuers"].max()
    # Add the new_value to the corresponding row and column
    df.loc[row_index, col_Actual] = max_value

    return df


# 8 or 9 Issuers value for the PL BB Result sheet
def issuers(df, df2, search_value, col_Actual):
    # Find the row index where the search_value is present in the first column
    row_index = df[df.iloc[:, 0] == search_value].index
    max_value = df2["Eligible Issuers"].max()
    # Add the new_value to the corresponding row and column
    df.loc[row_index, col_Actual] = max_value

    return df


def maxIssuerConcentrationPercent(df, df2, search_value, col_Actual):
    max_value = df2["ONW Adjustments Adj. Contr. % (issuer)"].max()
    row_index = df[df.iloc[:, 0] == search_value].index
    df.loc[row_index, col_Actual] = max_value

    return df


# Max. Industry Concentration (Largest Industry, % BB)


def maxIndustryConcentrationLargestIndustry(
    df, df2, search_value, col_Actual, largest_index
):
    # Find the row index where the search_value is present in the first column of df
    row_index = df[df.iloc[:, 0] == search_value].index

    # Get the largest value from the specified column in df2
    largest_value = (
        df2["percent of BB"].nlargest(largest_index).iloc[-1]
    )  # df2 is segmentation overview industry
    # Add the largest_value to the corresponding row and column in df
    df.loc[row_index, col_Actual] = largest_value

    return df


# Max. Industry Concentration (2nd Largest Industry, % BB)


def maxIndustryConcentrationSecondLargestIndustry(
    df, df2, search_value, col_Actual, largest_index
):
    # Find the row index where the search_value is present in the first column of df
    row_index = df[df.iloc[:, 0] == search_value].index

    # Get the largest value from the specified column in df2
    largest_value = (
        df2["percent of BB"].nlargest(largest_index).iloc[-1]
    )  # df2 is segmentation overview industry
    # Add the largest_value to the corresponding row and column in df
    df.loc[row_index, col_Actual] = largest_value

    return df


# Max. Industry Concentration (For all other industries, % BB)


def maxIndustryConcentrationAllOtherIndustry(
    df, df2, search_value, col_Actual, largest_index
):
    # Find the row index where the search_value is present in the first column of df
    row_index = df[df.iloc[:, 0] == search_value].index

    # Get the largest value from the specified column in df2
    largest_value = (
        df2["percent of BB"].nlargest(largest_index).iloc[-1]
    )  # df2 is segmentation overview industry
    # Add the largest_value to the corresponding row and column in df
    df.loc[row_index, col_Actual] = largest_value

    return df


# Max weighted average maturity (Year)


def maxWeightedAverageMaturity(df, weighted_avg_df):
    # value = weighted_avg_df.loc[2, 'Value']
    df.loc[df.iloc[:, 0] == "Max. Weighted Average Maturity (Years)", "Actual"] = (
        weighted_avg_df
    )
    return df


# Max. Contribution to BB with Maturity > 8 years


def maxContributiionToBBMaturity8Yrs(
    df, df2, col_InvetmentOverviewTenor, criteria, col_BBPercentofBB
):
    # Apply the criteria to the dataframe and filter the rows
    filtered_df = df2[df2[col_InvetmentOverviewTenor] > criteria]
    # Sum the values in the sum_range column of the filtered dataframe
    sumif_value = filtered_df[col_BBPercentofBB].sum()

    # Find the row where the first column value is 'Maturity' greater than 8 in the target dataframe
    row_index = df[
        df.iloc[:, 0] == "Max. Contribution to BB with Maturity > 8 years"
    ].index[0]

    # Add the result value to the 'value' column in the target dataframe at the specified row
    df.at[row_index, "Actual"] = sumif_value

    return df


# Max. Weighted Average Leverage thru Borrower


def maxWeightedAverageLeverage(df, weightedAverageAdjEligiblePortfolio):
    df.loc[
        df.iloc[:, 0] == "Max. Weighted Average Leverage thru Borrower", "Actual"
    ] = weightedAverageAdjEligiblePortfolio
    return df


# Max PIK, DIP


def maxPIKDIP(df_security, df):
    sum_values = df_security["Security Percent of BB"].iloc[7:9].sum()
    row_index = df[df.iloc[:, 0] == "Max. PIK, DIP"].index[0]
    df.at[row_index, "Actual"] = sum_values
    return df


# Min cash, First lien and Cov-lite


def minCashFirstLienCovLite(dataframe, df_results_concentrations, range_values):
    """ """
    total_sum = 0

    for value in range_values:
        if isinstance(value, range):
            total_sum += dataframe["Security Percent of BB"].iloc[value].sum()
        else:
            total_sum += dataframe["Security Percent of BB"].iloc[value]

    row_index = df_results_concentrations[
        df_results_concentrations.iloc[:, 0] == "Min. Cash, First Lien, and Cov-Lite"
    ].index[0]
    df_results_concentrations.at[row_index, "Actual"] = total_sum
    return df_results_concentrations


# Min. senior secured
def minSeniorSecured(dataframe, PL_BB_Build_results, range_values):
    total_sum = 0

    for value in range_values:
        if isinstance(value, range):
            total_sum += dataframe["Security Percent of BB"].iloc[value].sum()
        else:
            total_sum += dataframe["Security Percent of BB"].iloc[value]

    row_index = PL_BB_Build_results[
        PL_BB_Build_results.iloc[:, 0] == "Min. Senior Secured"
    ].index[0]
    PL_BB_Build_results.at[row_index, "Actual"] = total_sum
    return PL_BB_Build_results


# Min. Weighted Average Cash Fixed Coupon
def minWeightedAverageCashFixedCoupon(df, PL_BB_Build_df):
    value = PL_BB_Build_df["Weighted Fixed"].dropna().sum()

    # Sum of values from Weighted Average Stastics Fixed column from PL BB Build, CD35
    df.loc[df.iloc[:, 0] == "Min. Weighted Average Cash Fixed Coupon", "Actual"] = value
    return df


# Min. Weighted Average Cash Floating Coupon
def minWeightedAverageCashFloatingCoupon(df, PL_BB_Build_df):
    value = (
        PL_BB_Build_df["Weighted Floating"].dropna().sum()
    )  # Sum of values from Weighted Average Stastics Fixed column from PL BB Build, CF35
    df.loc[df.iloc[:, 0] == "Min. Weighted Average Cash Floating Coupon", "Actual"] = (
        value
    )
    return df


# Max. LTV Transactions
# =SUMIF('PL BB Build'!AL4:AL28,"Yes",'PL BB Build'!DQ4:DQ28)
def maxLTVTransaction(
    df, df2, col_LTVTransaction, criteria, col_BBPercentofBB
):  # df2 is PL Bb Build
    # Apply the criteria to the dataframe and filter the rows
    filtered_df = df2[df2[col_LTVTransaction] > criteria]

    # Sum the values in the sum_range column of the filtered dataframe
    sumif_value = filtered_df[col_BBPercentofBB].sum()

    # Find the row where the first column value is 'Maturity' greater than 8 in the target dataframe
    row_index = df[df.iloc[:, 0] == "Max. LTV Transactions"].index[0]

    # Add the result value to the 'value' column in the target dataframe at the specified row
    df.at[row_index, "Actual"] = sumif_value

    return df


# Max. Third Party Finance Companies
# =SUMIF('PL BB Build'!AP5:AP32,"Yes",'PL BB Build'!DQ5:DQ32)


def maxThirdPartyFinanceCompanies(
    df, df2, col_ThirdPartyFinanceCompany, criteria, col_BBPercentofBB
):  # df2 is PL Bb Build
    # Apply the criteria to the dataframe and filter the rows
    filtered_df = df2[df2[col_ThirdPartyFinanceCompany] > criteria]

    # Sum the values in the sum_range column of the filtered dataframe
    sumif_value = filtered_df[col_BBPercentofBB].sum()

    # Find the row where the first column value is 'Maturity' greater than 8 in the target dataframe
    row_index = df[df.iloc[:, 0] == "Max. Third Party Finance Companies"].index[0]

    # Add the result value to the 'value' column in the target dataframe at the specified row
    df.at[row_index, "Actual"] = sumif_value

    return df


# Max. Foreign Eligible Portfolio Investments
# =SUMIF('PL BB Build'!AK6:AK33,"Yes",'PL BB Build'!DQ6:DQ33)


def maxForeignEligiblePortfolioInvestments(
    df, df2, col_ApprovedForeignJurisdiction, criteria, col_BBPercentofBB
):  # df2 is PL Bb Build
    # Apply the criteria to the dataframe and filter the rows
    filtered_df = df2[df2[col_ApprovedForeignJurisdiction] == criteria]

    # Sum the values in the sum_range column of the filtered dataframe
    sumif_value = filtered_df[col_BBPercentofBB].sum()

    # Find the row where the first column value is 'Maturity' greater than 8 in the target dataframe
    row_index = df[
        df.iloc[:, 0] == "Max. Foreign Eligible Portfolio Investments"
    ].index[0]

    # Add the result value to the 'value' column in the target dataframe at the specified row
    df.at[row_index, "Actual"] = sumif_value

    return df


# Max. Affiliate Investments
# =SUMIF('PL BB Build'!AQ5:AQ32,"Yes",'PL BB Build'!DQ5:DQ32)


def maxAffiliateInvestment(
    df, df2, col_AffiliateInvestment, criteria, col_BBPercentofBB
):  # df2 is PL Bb Build
    # Apply the criteria to the dataframe and filter the rows
    filtered_df = df2[df2[col_AffiliateInvestment] > criteria]

    # Sum the values in the sum_range column of the filtered dataframe
    sumif_value = filtered_df[col_BBPercentofBB].sum()

    # Find the row where the first column value is 'Maturity' greater than 8 in the target dataframe
    row_index = df[df.iloc[:, 0] == "Max. Affiliate Investments"].index[0]

    # Add the result value to the 'value' column in the target dataframe at the specified row
    df.at[row_index, "Actual"] = sumif_value

    return df


# Max. Warehouse Assets
# =SUMIF('PL BB Build'!AG7:AG34,"Yes",'PL BB Build'!DQ7:DQ34)


def maxWarehouseAssets(
    df, df2, col_WarehouseAsset, criteria, col_BBPercentofBB
):  # df2 is PL Bb Build
    # Apply the criteria to the dataframe and filter the rows
    filtered_df = df2[df2[col_WarehouseAsset] > criteria]

    # Sum the values in the sum_range column of the filtered dataframe
    sumif_value = filtered_df[col_BBPercentofBB].sum()

    # Find the row where the first column value is 'Maturity' greater than 8 in the target dataframe
    row_index = df[df.iloc[:, 0] == "Max. Warehouse Assets"].index[0]

    # Add the result value to the 'value' column in the target dataframe at the specified row
    df.at[row_index, "Actual"] = sumif_value

    return df


def totals_row(df):
    df.loc[df.index[-1], "Concentration Tests"] = "Total"
    df.loc[df.index[-1], "Concentration Limit"] = df["Concentration Limit"].sum()
    return df


import pandas as pd


def pass_columns(df):
    df["Result"] = df.apply(
        lambda row: "Pass" if row["Actual"] < row["Concentration Limit"] else "Fail",
        axis=1,
    )
    return df


def min_eligible_issuers(df):
    df.loc[df["Concentration Tests"] == "Min. Eligible Issuers (#)", "Result"] = (
        df.apply(
            lambda row: (
                "Pass" if row["Actual"] >= row["Concentration Limit"] else "Fail"
            ),
            axis=1,
        )
    )
    return df


def min_case_senior(df):
    df.loc[
        df["Concentration Tests"].isin(
            ["Min. Cash, First Lien, and Cov-Lite", "Min. Senior Secured"]
        ),
        "Result",
    ] = df.apply(
        lambda row: "Pass" if row["Actual"] > row["Concentration Limit"] else "Fail",
        axis=1,
    )
    return df


def min_weighted_avg_fixed_floating(df):
    df.loc[
        df["Concentration Tests"].isin(
            [
                "Min. Weighted Average Cash Fixed Coupon",
                "Min. Weighted Average Cash Floating Coupon",
            ]
        ),
        "Result",
    ] = df.apply(
        lambda row: (
            "N/A"
            if row["Actual"] == 0
            else ("Pass" if row["Actual"] > row["Concentration Limit"] else "Fail")
        ),
        axis=1,
    )
    return df


def issuers_8_9(df):
    df.loc[df["Concentration Tests"] == "8 or 9 Issuers?", "Result"] = df.apply(
        lambda row: "Adjust A/R in Column DM" if row["Actual"] in [8, 9] else "Fail",
        axis=1,
    )
    return df


# Max. Preferred Stock

# Pass column

# def apply_conditions(df):
#     conditions_above = [2, 3, 4, 5, 6, 7, 8, 9, 14, 15, 16, 17, 18, 19]
#     conditions_below = [0, 10, 11]

#     # Apply condition for rows 2-19 (above condition)
#     df['Result'] = np.where(df.index.isin(conditions_above) & (df['Actual'] < df['Concentration Limit']), 'Pass', 'Fail')

#     # Apply condition for row 0, 10, 11 (below condition)
#     df['Result'] = np.where(df.index.isin(conditions_below) & (df['Actual'] > df['Concentration Limit']), 'Pass', 'Fail')

#     # Apply condition for row 12, 13 (below condition)
#     df['Result'] = np.where(df.index == 12 or df.indexx == 13, np.where(df['Actual'] > df['Concentration Limit'], 'Pass', np.where(df['Actual'] == 0, 'N/A', 'Fail')), df['Result'])

#     # Apply condition for row 1
#     df['Result'] = np.where(df.index == 1, np.where(df['Actual'] == 9, 'Adjust A/R in Column DM', np.where(df['Actual'] == 8, 'Adjust A/R in Column DM', 'No')), df['Result'])

#     return df

# Unadjusted BB for the table Industry
# =SUMIF('PL BB Build'!$J$7:$J$33,'PL BB Results'!D42,'PL BB Build'!$DL$7:$DL$33)


def unadjustedBBIndustrySum(filtered_df):
    #   filtered_df['Borrowing Base Adj. Contribution']=filtered_df['Borrowing Base Adj. Contribution'].fillnan(0)
    filtered_df["Borrowing Base Adj. Contribution"].fillna(0, inplace=True)

    sumif_value = filtered_df["Borrowing Base Adj. Contribution"].sum()

    return sumif_value


def unadjustedBBIndustry(df_industry, PL_BB_Build_df):
    df_industry["Unadjusted BB"] = df_industry.apply(
        lambda x: unadjustedBBIndustrySum(
            PL_BB_Build_df[PL_BB_Build_df["Investment Industry"] == x["Industries"]]
        ),
        axis=1,
    )

    return df_industry


# Unadjuste BB percent value for Industry table on PL BB Result sheet
def unadjustedPercentBB(df_industry):
    sum_unadjusted_BB = df_industry["Unadjusted BB"].sum()
    df_industry["Unadjusted Percent BB"] = (
        df_industry["Unadjusted BB"] / sum_unadjusted_BB
    )

    return df_industry


# Security table from PL BB Result sheet
# =SUMIF('PL BB Build'!$BN$7:$BN$33,'PL BB Results'!D100,'PL BB Build'!$DP$7:$DP$35)


def securityBBSum(filtered_df):
    sumif_value = filtered_df["Borrowing Base"].sum()
    return sumif_value


def securityBB(df_security, PL_BB_Build_df):
    df_security["Security BB"] = df_security.apply(
        lambda x: securityBBSum(
            PL_BB_Build_df[
                PL_BB_Build_df["Classification Adj. Adjusted Type"] == x["Security"]
            ]
        ),
        axis=1,
    )

    return df_security


# Security percent BB


def securityPercentBB(df_security):
    sum_security_BB = df_security["Security BB"].sum()
    df_security["Security Percent of BB"] = df_security["Security BB"] / sum_security_BB

    return df_security


def totals_row_security(df):
    df.loc[df.index[-1], "Security"] = "Total"
    df.loc[df.index[-1], "Security BB"] = df["Security BB"].sum()
    df.loc[df.index[-1], "Security Percent of BB"] = df["Security Percent of BB"].sum()
    return df


def Obligator_calculations(
    df_Obligors_Net_Capital,
    df_Availability,
    total_capitalCalled,
    total_uncalled_Capital,
):
    # Calculating PL BB Results "Obligors' Net Capital" table
    df_Obligors_Net_Capital.loc[
        df_Obligors_Net_Capital["Obligors' Net Capital"] == "Equity Paid in Capital",
        "values",
    ] = total_capitalCalled

    if (
        df_Availability.loc[
            (
                df_Availability["A"]
                == "Commitment Period (3 years from Final Closing Date, as defined in LPA)"
            )
            & (df_Availability["B"] == "Yes")
        ]
        .any()
        .any()
    ):
        df_Obligors_Net_Capital.loc[
            df_Obligors_Net_Capital["Obligors' Net Capital"]
            == "(b) Uncalled Capital Commitments (excl. Defaulting Investors)",
            "values",
        ] = total_uncalled_Capital
    else:
        df_Obligors_Net_Capital.loc[
            df_Obligors_Net_Capital["Obligors' Net Capital"]
            == "(b) Uncalled Capital Commitments (excl. Defaulting Investors)",
            "values",
        ] = 0
    sum_Equity_Paid_Distributions_Retaind = df_Obligors_Net_Capital[
        df_Obligors_Net_Capital["Obligors' Net Capital"].isin(
            ["Equity Paid in Capital", "Distributions", "Retained Earnings"]
        )
    ]["values"].sum()
    df_Obligors_Net_Capital.loc[
        df_Obligors_Net_Capital["Obligors' Net Capital"] == "(a) Partners' Capital",
        "values",
    ] = sum_Equity_Paid_Distributions_Retaind
    df_Obligors_Net_Capital.loc[
        df_Obligors_Net_Capital["Obligors' Net Capital"]
        == "Obligors' Net Capital ((a) + (b))",
        "values",
    ] = df_Obligors_Net_Capital[
        df_Obligors_Net_Capital["Obligors' Net Capital"].isin(
            [
                "(a) Partners' Capital",
                "(b) Uncalled Capital Commitments (excl. Defaulting Investors)",
            ]
        )
    ][
        "values"
    ].sum()
    # infinite value giving runtime wraning
    # df_Obligors_Net_Capital.loc[df_Obligors_Net_Capital["Obligors' Net Capital"]=="Debt / Equity",'values']=df_Availability['Unnamed: 8'][30]/df_Obligors_Net_Capital[df_Obligors_Net_Capital["Obligors' Net Capital"]=="(a) Partners' Capital"]['values'].iloc[0]
    return df_Obligors_Net_Capital
