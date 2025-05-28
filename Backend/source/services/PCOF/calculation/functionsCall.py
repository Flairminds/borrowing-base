import pandas as pd
import math
from source.services.PCOF.calculation.PL_BB_Build import *
from source.services.PCOF.calculation.Subscription_BB import *
from source.services.PCOF.calculation.PL_BB_Results import *
from source.services.PCOF.calculation.cash import *
from source.services.PCOF.calculation.pl_bb_build_Availability import *
import numpy as np

from source.services.concTestService.concTestService import ConcentrationTestExecutor

# from std_file_formater import std_file_format


def calculation_for_subscription(
    df_subscriptionBB, df_Inputs_Concentration_limit, df_Inputs_Advance_Rates
):
    df_subscriptionBB = calculate_Uncalled_Capital(df_subscriptionBB)
    Total_Eligible_Commitments = df_subscriptionBB[
        (df_subscriptionBB["Designation"] == "Institutional Investors")
        | (df_subscriptionBB["Designation"] == "High Net Worth Investors")
    ]["Uncalled Capital"].sum()
    total_allInvestors = df_subscriptionBB["Uncalled Capital"].sum()
    df_subscriptionBB = calculate_percent_of_Uncalled(
        df_subscriptionBB, total_allInvestors
    )
    df_subscriptionBB = calculate_of_Elig_Uncalled(
        df_subscriptionBB, Total_Eligible_Commitments
    )
    df_subscriptionBB = calculate_Concentration_Limit(
        df_subscriptionBB,
        df_Inputs_Concentration_limit[
            df_Inputs_Concentration_limit["Investors"]
            == "Institutional Investors Investors"
        ]["Concentration Limit"].iloc[0],
        df_Inputs_Concentration_limit[
            df_Inputs_Concentration_limit["Investors"] == "HNW Investors Individual"
        ]["Concentration Limit"].iloc[0],
    )
    df_subscriptionBB = calculate_Excess_Concentration(
        df_subscriptionBB, Total_Eligible_Commitments
    )
    df_subscriptionBB = calculate_Less_Excess_Conc(df_subscriptionBB)
    df_subscriptionBB = calculate_Advance_Rate(
        df_subscriptionBB,
        df_Inputs_Advance_Rates[
            df_Inputs_Advance_Rates["Investor Type"] == "Institutional Investors"
        ]["Advance Rate"].iloc[0],
        df_Inputs_Advance_Rates[
            df_Inputs_Advance_Rates["Investor Type"] == "HNW Investors"
        ]["Advance Rate"].iloc[0],
    )
    df_subscriptionBB = calculate_Borrowing_Base_subscription(df_subscriptionBB)
    return df_subscriptionBB


def calculation_for_build(
    df_PL_BB_Build,
    df_Inputs_Other_Metrics,
    df_Availability_Borrower,
    total_capitalCalled,
    df_Inputs_Portfolio_LeverageBorrowingBase,
    total_uncalled_Capital,
    df_Obligors_Net_Capital,
):

    # Function call for PL_BB_Build
    df_PL_BB_Build = Weighted_LTM_EBITDA(df_PL_BB_Build, df_Inputs_Other_Metrics)

    df_PL_BB_Build = Weighted_maturity(
        df_PL_BB_Build, df_Inputs_Other_Metrics, df_Availability_Borrower
    )

    df_PL_BB_Build = Test_applies(df_PL_BB_Build, df_Inputs_Other_Metrics)

    df_PL_BB_Build = Eligible_Issuer(df_PL_BB_Build, df_Inputs_Other_Metrics)

    df_PL_BB_Build = Eligible_Industry(df_PL_BB_Build, df_Inputs_Other_Metrics)

    df_PL_BB_Build = calculate_weighted_fixed(df_PL_BB_Build, df_Inputs_Other_Metrics)

    df_PL_BB_Build = calculate_Weighted_Floating(
        df_PL_BB_Build, df_Inputs_Other_Metrics
    )

    df_PL_BB_Build = calculate_percent_Adj_Elig_Amount_excluding_cash(
        df_PL_BB_Build, df_Inputs_Other_Metrics
    )

    sum_of_FMV = df_PL_BB_Build[df_PL_BB_Build["Is Eligible Issuer"] == "Yes"][
        "Investment FMV"
    ].sum()

    # Obligors table
    df_Obligors_Net_Capital = Obligator_calculations(
        df_Obligors_Net_Capital,
        df_Availability_Borrower,
        total_capitalCalled,
        total_uncalled_Capital,
    )

    df_PL_BB_Build = calculate_concentration_percent_of_ONC(
        df_PL_BB_Build, df_Obligors_Net_Capital
    )  # check obligators dataframe name

    df_PL_BB_Build = calculate_Revolver_Adj_Advance_Rate(
        df_PL_BB_Build,
        df_Inputs_Portfolio_LeverageBorrowingBase,
        df_Inputs_Other_Metrics,
    )

    df_PL_BB_Build = calculate_First_Second_Lien_Rate(
        df_PL_BB_Build,
        df_Inputs_Portfolio_LeverageBorrowingBase,
        df_Inputs_Other_Metrics,
    )

    date_as_of = df_Availability_Borrower[
        df_Availability_Borrower["A"] == "Date of determination:"
    ]["B"].iloc[0]

    df_PL_BB_Build = calculate_Warehouse_Day_Count(df_PL_BB_Build, date_as_of)

    df_PL_BB_Build = calculate_All_In(df_PL_BB_Build)

    df_PL_BB_Build = calculate_All_In_Cash(df_PL_BB_Build)

    df_PL_BB_Build = calculate_percent_of_FMV(df_PL_BB_Build, sum_of_FMV)

    df_PL_BB_Build = calculate_FMV_Cost(df_PL_BB_Build)

    df_PL_BB_Build = calculate_FMV_Par(df_PL_BB_Build)
    df_PL_BB_Build = calculate_classification_Eligible(df_PL_BB_Build)

    df_PL_BB_Build = calculate_Final_Eligible(df_PL_BB_Build)

    df_PL_BB_Build = calculate_Eligible(df_PL_BB_Build)

    df_PL_BB_Build = calculate_Warehouse_Second_Lien_Share(
        df_PL_BB_Build,
        df_Inputs_Other_Metrics[
            df_Inputs_Other_Metrics["Other Metrics"]
            == "Warehouse First Lien Leverage Cut-Off"
        ]["values"].iloc[0],
    )

    df_PL_BB_Build = calculate_Warehouse_Second_Lien_Rate(
        df_PL_BB_Build,
        df_Inputs_Portfolio_LeverageBorrowingBase[
            df_Inputs_Portfolio_LeverageBorrowingBase["Investment Type"]
            == "Second Lien"
        ],
    )

    df_PL_BB_Build = calculate_First_Lien_Second_Lien_Share(
        df_PL_BB_Build,
        df_Inputs_Other_Metrics[
            df_Inputs_Other_Metrics["Other Metrics"]
            == "First Lien Leverage Cut-Off Point"
        ]["values"].iloc[0],
    )

    df_PL_BB_Build = calculate_First_Lien_Adj_Advance_Rate(df_PL_BB_Build)

    df_PL_BB_Build = calculate_First_Lien_Contribution(df_PL_BB_Build)
    df_PL_BB_Build = calculate_Concentration_Issuer_percent_of_ONC(df_PL_BB_Build)

    df_PL_BB_Build = calculate_ONW_Adjustments_percent_of_ONC_greater_10_percent(
        df_PL_BB_Build,
        df_Inputs_Other_Metrics[
            df_Inputs_Other_Metrics["Other Metrics"] == "Concentration Test Threshold 1"
        ],
    )

    df_PL_BB_Build = calculate_ONW_Adjustments_percent_of_ONC_greater_7_point_5_percent(
        df_PL_BB_Build,
        df_Inputs_Other_Metrics[
            df_Inputs_Other_Metrics["Other Metrics"] == "Concentration Test Threshold 1"
        ],
    )

    df_PL_BB_Build = calculate_ONW_Adjustments_greater_10_percent_ONC_Share(
        df_PL_BB_Build, df_Obligors_Net_Capital
    )
    df_PL_BB_Build = calculate_ONW_Adjustments_greater_7_point_5_percent_ONC_Share(
        df_PL_BB_Build, df_Obligors_Net_Capital
    )
    df_PL_BB_Build = calculate_ONW_Adjustments_ONC_haircut_for_Elig_Amount(
        df_PL_BB_Build, df_Inputs_Other_Metrics
    )
    df_PL_BB_Build = calculate_ONW_Adjustments_Adj_Elig_Amount(df_PL_BB_Build)

    df_PL_BB_Build = calculate_ONW_Adjustments_Concentration_BB_Adj_Contribution(
        df_PL_BB_Build, df_Inputs_Other_Metrics
    )
    df_PL_BB_Build = calculate_Borrowing_Base_Adj_Contribution(df_PL_BB_Build)
    df_PL_BB_Build = calculate_Borrowing_Base_ONW_Adjustment(df_PL_BB_Build)

    df_PL_BB_Build = calculate_Borrowing_Base(df_PL_BB_Build)

    df_PL_BB_Build = calculate_Borrowing_Base_percent_of_BB(df_PL_BB_Build)
    df_PL_BB_Build = calculate_Adj_Contr_percent_issuer(
        df_PL_BB_Build, df_Obligors_Net_Capital
    )
    df_PL_BB_Build = calculate_Eligible_Issuers(df_PL_BB_Build)

    # Cash functions
    global cash_index
    cash_index = df_PL_BB_Build[df_PL_BB_Build["Investment Name"] == "Cash"].index[0]

    df_PL_BB_Build = calculate_Investment_Cost(df_PL_BB_Build, cash_index)
    df_PL_BB_Build = calculate_Investment_External_Valuation(df_PL_BB_Build, cash_index)
    df_PL_BB_Build = calculate_Investment_Internal_Valuation(df_PL_BB_Build, cash_index)
    df_PL_BB_Build = calculate_Investment_FMV(df_PL_BB_Build, cash_index)
    df_PL_BB_Build = calculate_Classification_for_BB(df_PL_BB_Build, cash_index)

    df_PL_BB_Build = EBITDA_Threshold(
        df_PL_BB_Build, df_Inputs_Other_Metrics, cash_index
    )
    df_PL_BB_Build = ONW_Adjustments(df_PL_BB_Build, cash_index)
    df_PL_BB_Build = calculate_First_Adj_Advance_Rate(df_PL_BB_Build, cash_index)
    df_PL_BB_Build = contributionCash(
        df_PL_BB_Build,
        "Concentration Adj. Elig. Amount",
        "First Lien Adj. Advance Rate",
        cash_index,
        "First Lien Contribution",
    )
    df_PL_BB_Build = secondLienShareCash(
        df_PL_BB_Build,
        df_Inputs_Other_Metrics,
        "Adv. Adv. Rate",
        "Classifications Approved Foreign Jurisdiction",
        "Test 1 EBITDA Threshold",
        cash_index,
        "Warehouse Second Lien Share",
    )
    df_PL_BB_Build = adjContrPercentIssuerCash(
        df_PL_BB_Build,
        "Investment Name",
        "ONW Adjustments Adj. Elig. Amount",
        "cash",
        df_Obligors_Net_Capital,
        "ONW Adjustments Adj. Contr. % (issuer)",
        cash_index,
    )
    df_PL_BB_Build = onwAdjustmentCash(
        df_PL_BB_Build,
        "Borrowing Base Adj. Contribution",
        "First Lien Contribution",
        cash_index,
        "Borrowing ONW Adjustment",
    )

    df_PL_BB_Build = adjContributionCash(
        df_PL_BB_Build,
        "Concentration Adj. Elig. Amount",
        "ONW Adjustments > 7.5% ONC Share",
        "ONW Adjustments > 10% ONC Share",
        "First Lien Adj. Advance Rate",
        "ONW Adjustments Concentration BB Adj. Contribution",
        cash_index,
        "Borrowing Adj. Contribution",
    )
    df_PL_BB_Build = borrowingBaseCash(
        df_PL_BB_Build,
        "Borrowing Base Adj. Contribution",
        "Borrowing Base Other Adjustment",
        "Borrowing Base",
        cash_index,
    )
    df_PL_BB_Build = percentBBCash(
        df_PL_BB_Build, "Borrowing Base", cash_index, "Borrowing % of BB"
    )

    return df_PL_BB_Build


def calculation_for_Segmentation_overview(df_industry, df_PL_BB_Build):
    df_segmentation_overview = pd.DataFrame()

    # Assign 'industry' column from df_industry to df_segmentation_overview
    df_segmentation_overview["industry"] = df_industry["Industries"]

    sum_results = []
    for index, row in df_segmentation_overview.iterrows():
        # Extracting the industry from each row
        industry = row["industry"]

        # Filtering df_PL_BB_Build based on the industry and specific rows
        filtered_df = df_PL_BB_Build[
            (df_PL_BB_Build["Investment Industry"].str.lower() == industry.lower())
            & (df_PL_BB_Build["Is Eligible Issuer"] == "Yes")
        ]

        # Summing the 'Adj. Contribution' column for the filtered DataFrame
        sum_result = filtered_df["Borrowing Base Adj. Contribution"].sum()
        sum_results.append(sum_result)

    # Assign the sum_results to 'BB' column in df_segmentation_overview
    df_segmentation_overview["BB"] = sum_results

    value_to_add = []
    # Calculate the '% of BB' for each industry
    for index, row in df_segmentation_overview.iterrows():
        # Calculate the percentage contribution of each industry to total 'BB'
        final_value = row["BB"] / df_segmentation_overview["BB"].sum()
        value_to_add.append(final_value)

    # Assign the calculated values to '% of BB' column in df_segmentation_overview
    df_segmentation_overview["percent of BB"] = value_to_add
    # total row
    # df_segmentation_overview.loc[df_segmentation_overview.index[-1], 'industry'] = 'Total'
    # df_segmentation_overview.loc[df_segmentation_overview.index[-1], 'BB'] = df_segmentation_overview['BB'].sum()
    # df_segmentation_overview.loc[df_segmentation_overview.index[-1], 'percent of BB'] = df_segmentation_overview['percent of BB'].sum()

    total_row_df = pd.DataFrame(
        {
            "industry": ["Total"],
            "BB": [df_segmentation_overview["BB"].sum()],
            "percent of BB": [df_segmentation_overview["percent of BB"].sum()],
        }
    )

    df_segmentation_overview = pd.concat(
        [df_segmentation_overview, total_row_df], ignore_index=True
    )

    return df_segmentation_overview


def calculation_results_function_Call(
    df_PL_BB_Results,
    df_PL_BB_Build,
    df_Inputs_Other_Metrics,
    df_security,
    df_industry,
    df_Availability_Borrower,
):
    df_segmentation_overview = calculation_for_Segmentation_overview(
        df_industry, df_PL_BB_Build
    )

    # df_PL_BB_Results = minEligibleIssuersActual(
    #     df_PL_BB_Results, df_PL_BB_Build, "Min. Eligible Issuers (#)", "Actual"
    # )
    # df_PL_BB_Results = minEligibleIssuersActual(
    #     df_PL_BB_Results, df_PL_BB_Build, "Min. Eligible Issuers (#)", "Actual"
    # )

    # df_PL_BB_Results = issuers(
    #     df_PL_BB_Results, df_PL_BB_Build, "8 or 9 Issuers?", "Actual"
    # )
    # df_PL_BB_Results = issuers(
    #     df_PL_BB_Results, df_PL_BB_Build, "8 or 9 Issuers?", "Actual"
    # )

    # df_industry = unadjustedBBIndustry(df_industry, df_PL_BB_Build)
    # sum_unadjusted_BB = df_industry["Unadjusted BB"].sum()
    # df_industry = unadjustedPercentBB(df_industry)
    # df_industry = unadjustedBBIndustry(df_industry, df_PL_BB_Build)
    # sum_unadjusted_BB = df_industry["Unadjusted BB"].sum()
    # df_industry = unadjustedPercentBB(df_industry)

    # df_PL_BB_Results = maxIssuerConcentrationPercent(
    #     df_PL_BB_Results, df_PL_BB_Build, "Max. Issuer Concentration (% BB)", "Actual"
    # )  # Values dependends on G column in Industry calculation
    # df_PL_BB_Results = maxIndustryConcentrationLargestIndustry(
    #     df_PL_BB_Results,
    #     df_segmentation_overview,
    #     "Max. Industry Concentration (Largest Industry, % BB)",
    #     "Actual",
    #     2,
    # )
    # df_PL_BB_Results = maxIndustryConcentrationSecondLargestIndustry(
    #     df_PL_BB_Results,
    #     df_segmentation_overview,
    #     "Max. Industry Concentration (2nd Largest Industry, % BB)",
    #     "Actual",
    #     3,
    # )
    # df_PL_BB_Results = maxIssuerConcentrationPercent(
    #     df_PL_BB_Results, df_PL_BB_Build, "Max. Issuer Concentration (% BB)", "Actual"
    # )  # Values dependends on G column in Industry calculation
    # df_PL_BB_Results = maxIndustryConcentrationLargestIndustry(
    #     df_PL_BB_Results,
    #     df_segmentation_overview,
    #     "Max. Industry Concentration (Largest Industry, % BB)",
    #     "Actual",
    #     2,
    # )
    # df_PL_BB_Results = maxIndustryConcentrationSecondLargestIndustry(
    #     df_PL_BB_Results,
    #     df_segmentation_overview,
    #     "Max. Industry Concentration (2nd Largest Industry, % BB)",
    #     "Actual",
    #     3,
    # )

    # df_PL_BB_Results = maxIndustryConcentrationAllOtherIndustry(
    #     df_PL_BB_Results,
    #     df_segmentation_overview,
    #     "Max. Industry Concentration (All Other Industries, % BB)",
    #     "Actual",
    #     4,
    # )
    # df_PL_BB_Results = maxIndustryConcentrationAllOtherIndustry(
    #     df_PL_BB_Results,
    #     df_segmentation_overview,
    #     "Max. Industry Concentration (All Other Industries, % BB)",
    #     "Actual",
    #     4,
    # )

    # weighted_avg_df = Weighted_Average_Adj_Eligible_Portfolio(
    #     df_PL_BB_Build, df_Inputs_Other_Metrics
    # )
    # df_PL_BB_Results = maxWeightedAverageMaturity(df_PL_BB_Results, weighted_avg_df)
    # weighted_avg_df = Weighted_Average_Adj_Eligible_Portfolio(
    #     df_PL_BB_Build, df_Inputs_Other_Metrics
    # )
    # df_PL_BB_Results = maxWeightedAverageMaturity(df_PL_BB_Results, weighted_avg_df)

    # df_PL_BB_Results = maxContributiionToBBMaturity8Yrs(
    #     df_PL_BB_Results,
    #     df_PL_BB_Build,
    #     "Investment Tenor",
    #     8,
    #     "Borrowing Base % of BB",
    # )
    # weighted_average = Weighted_Average_leverage_thru_Borrower(
    #     df_PL_BB_Build, df_Inputs_Other_Metrics
    # )
    # df_PL_BB_Results = maxContributiionToBBMaturity8Yrs(
    #     df_PL_BB_Results,
    #     df_PL_BB_Build,
    #     "Investment Tenor",
    #     8,
    #     "Borrowing Base % of BB",
    # )
    # weighted_average = Weighted_Average_leverage_thru_Borrower(
    #     df_PL_BB_Build, df_Inputs_Other_Metrics
    # )

    # df_PL_BB_Results = maxWeightedAverageLeverage(df_PL_BB_Results, weighted_average)
    # df_PL_BB_Results = maxWeightedAverageLeverage(df_PL_BB_Results, weighted_average)

    # df_industry = unadjustedBBIndustry(df_industry, df_PL_BB_Build)
    df_security = securityBB(df_security, df_PL_BB_Build)

    df_security = securityPercentBB(df_security)
    # df_PL_BB_Results = maxPIKDIP(df_security, df_PL_BB_Results)

    # G100_G101_range = range(0, 2)
    # range_values = [G100_G101_range, 6, 9]
    # df_PL_BB_Results = minCashFirstLienCovLite(
    #     df_security, df_PL_BB_Results, range_values
    # )

    # G100_G103_range = range(0, 4)
    # range_values = [G100_G103_range, 6, 9]

    # df_PL_BB_Results = minSeniorSecured(df_security, df_PL_BB_Results, range_values)

    # df_PL_BB_Results = minWeightedAverageCashFixedCoupon(
    #     df_PL_BB_Results, df_PL_BB_Build
    # )
    # df_PL_BB_Results = minWeightedAverageCashFloatingCoupon(
    #     df_PL_BB_Results, df_PL_BB_Build
    # )
    # df_PL_BB_Results = maxLTVTransaction(
    #     df_PL_BB_Results,
    #     df_PL_BB_Build,
    #     "Classifications LTV Transaction",
    #     "Yes",
    #     "Borrowing Base % of BB",
    # )

    # df_PL_BB_Results = maxThirdPartyFinanceCompanies(
    #     df_PL_BB_Results,
    #     df_PL_BB_Build,
    #     "Classifications Third Party Finance Company",
    #     "Yes",
    #     "Borrowing Base % of BB",
    # )
    # df_PL_BB_Results = maxForeignEligiblePortfolioInvestments(
    #     df_PL_BB_Results,
    #     df_PL_BB_Build,
    #     "Classifications Approved Foreign Jurisdiction",
    #     "Yes",
    #     "Borrowing Base % of BB",
    # )
    # df_PL_BB_Results = maxAffiliateInvestment(
    #     df_PL_BB_Results,
    #     df_PL_BB_Build,
    #     "Classifications Affiliate Investment",
    #     "Yes",
    #     "Borrowing Base % of BB",
    # )

    # df_PL_BB_Results = maxWarehouseAssets(
    #     df_PL_BB_Results,
    #     df_PL_BB_Build,
    #     "Classifications Warehouse Asset",
    #     "Yes",
    #     "Borrowing Base % of BB",
    # )
    # df_PL_BB_Results = totals_row(df_PL_BB_Results)
    # df_PL_BB_Results = pass_columns(df_PL_BB_Results)
    # df_PL_BB_Results = min_eligible_issuers(df_PL_BB_Results)
    # df_PL_BB_Results = min_case_senior(df_PL_BB_Results)
    # df_PL_BB_Results = min_weighted_avg_fixed_floating(df_PL_BB_Results)
    # df_PL_BB_Results = issuers_8_9(df_PL_BB_Results)

    # sum_unadjusted_BB = df_industry["Unadjusted BB"].sum()
    # df_industry = unadjustedPercentBB(df_industry)
    df_security = totals_row_security(df_security)

    # return df_PL_BB_Results, df_security, df_industry

    df_security = securityBB(df_security, df_PL_BB_Build)
    df_security = securityPercentBB(df_security)
    concentrationrestExecutor = ConcentrationTestExecutor(
        {
            "PL BB Build": df_PL_BB_Build,
            "Availability Borrower": df_Availability_Borrower,
            "Segmentation Overview": df_segmentation_overview,
        },
        "PCOF",
    )
    df_PL_BB_Results = concentrationrestExecutor.executeConentrationTest()
    return df_PL_BB_Results, df_security, df_industry


def calculation_for_Availability(
    df_Availability_Borrower,
    df_subscriptionBB,
    df_PL_BB_Results,
    df_PL_BB_Build,
    df_Input_pricing,
):
    df_Availability_Borrower = calculate_Months_since_Revolving_Closing_Date(
        df_Availability_Borrower
    )
    df_Availability_Borrower = calculate_Uncalled_Capital_Commitments_availability(
        df_Availability_Borrower, df_subscriptionBB
    )

    df_Availability_Borrower = calculate_subscription_Borrowing_Base(
        df_Availability_Borrower, df_subscriptionBB
    )
    df_Availability_Borrower = (
        calculate_Effective_Advance_Rate_on_Total_Uncalled_Capital(
            df_Availability_Borrower, df_subscriptionBB
        )
    )
    df_Availability_Borrower = Portfolio_greater_than_8_Eligible_Issuers(
        df_Availability_Borrower, df_PL_BB_Build
    )
    df_Availability_Borrower = Portfolio_FMV_of_Portfolio(
        df_Availability_Borrower, df_PL_BB_Build, df_PL_BB_Results
    )
    df_Availability_Borrower = Portfolio_Portfolio_Leverage_Borrowing_Base_calculated(
        df_Availability_Borrower, df_PL_BB_Build, df_PL_BB_Results
    )
    df_Availability_Borrower = Portfolio_Effective_Advance_Rate_on_FMV_of_Portfolio(
        df_Availability_Borrower, df_PL_BB_Build, df_PL_BB_Results
    )
    df_Availability_Borrower = Portfolio_Maximum_Advance_Rate_on_PL_Borrowing_Base(
        df_PL_BB_Build, df_Input_pricing, df_Availability_Borrower
    )

    df_Availability_Borrower = Portfolio_Portfolio_Leverage_Borrowing_Base(
        df_Availability_Borrower, df_PL_BB_Results, df_PL_BB_Build, df_Input_pricing
    )

    df_Availability_Borrower = calculate_A_Total_Borrowing_Base(
        df_Availability_Borrower, df_subscriptionBB
    )
    df_Availability_Borrower = calculate_Outstandings(df_Availability_Borrower)
    df_Availability_Borrower = calculate_lesser_of_a_b(
        df_Availability_Borrower, df_subscriptionBB
    )

    df_Availability_Borrower = calculate_Gross_BB_Utilization(
        df_Availability_Borrower, df_subscriptionBB
    )
    df_Availability_Borrower = calculate_Facility_Utilization(
        df_Availability_Borrower, df_subscriptionBB
    )

    df_Availability_Borrower = calculate_A_Net_Debt_A(
        df_Availability_Borrower, df_subscriptionBB
    )
    return df_Availability_Borrower


def intermediate_metrics(df_PL_BB_Build, df_PL_BB_Output):
    df_PL_BB_Output["Company"] = df_PL_BB_Build["Investment Name"]
    df_PL_BB_Output["Eligible"] = df_PL_BB_Build["Final Eligible"]
    df_PL_BB_Output["Maturity"] = df_PL_BB_Build["Investment Maturity"]
    df_PL_BB_Output["Industry"] = df_PL_BB_Build["Investment Industry"]
    df_PL_BB_Output["Quoted / Unquoted"] = df_PL_BB_Build[
        "Classifications Quoted / Unquoted"
    ]
    df_PL_BB_Output["Security"] = df_PL_BB_Build["Classification Adj. Adjusted Type"]
    df_PL_BB_Output["Cost"] = df_PL_BB_Build["Investment Cost"]
    df_PL_BB_Output["FMV"] = df_PL_BB_Build["Investment FMV"]
    df_PL_BB_Output["Eligible Investments"] = df_PL_BB_Build[
        "Portfolio Eligible Amount"
    ]
    df_PL_BB_Output["Ineligible Investments"] = (
        df_PL_BB_Output["Eligible Investments"] - df_PL_BB_Output["FMV"]
    )

    df_PL_BB_Output["Adjustments"] = df_PL_BB_Build["Concentration Adjustment"]
    df_PL_BB_Output["Adj. Eligible Investments"] = (
        df_PL_BB_Output["Eligible Investments"] + df_PL_BB_Output["Adjustments"]
    )

    df_PL_BB_Output["Adj. Advance Rate"] = df_PL_BB_Build[
        "First Lien Adj. Advance Rate"
    ]

    def Contribution(df_PL_BB_Output):
        try:
            df_PL_BB_Output["Contribution"] = df_PL_BB_Output.apply(
                lambda x: Contribution_helper(
                    x["Adj. Eligible Investments"], x["Adj. Advance Rate"]
                ),
                axis=1,
            )
        except Exception as e:
            raise Exception(e)

        return df_PL_BB_Output

    def Contribution_helper(Adj_Eligible_Investments, Adj_Advance_Rate):
        try:
            return Adj_Eligible_Investments * Adj_Advance_Rate
        except:
            return 0

    df_PL_BB_Output = Contribution(df_PL_BB_Output)

    df_PL_BB_Output["Adjustments"] = (
        df_PL_BB_Build["Borrowing Base ONW Adjustment"]
        + df_PL_BB_Build["Borrowing Base Other Adjustment"]
        + df_PL_BB_Build["Borrowing Base Industry Concentration"]
    )
    df_PL_BB_Output["Borrowing Base"] = (
        df_PL_BB_Output["Contribution"] + df_PL_BB_Output["Adjustments"]
    )

    return df_PL_BB_Output


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


def calculate_bb(
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
    df_PL_BB_Output=pd.DataFrame(),
):
    try:
        # cash_index = df_PL_BB_Build[df_PL_BB_Build['Investment Name']=='cash'].index[0]
        # Function call for SubscriptionBB
        df_PL_BB_Build = df_PL_BB_Build.copy()
        df_Inputs_Other_Metrics = df_Inputs_Other_Metrics.copy()
        df_Availability_Borrower = df_Availability_Borrower.copy()
        df_PL_BB_Results = df_PL_BB_Results.copy()
        df_subscriptionBB = df_subscriptionBB.copy()
        df_security = df_security.copy()
        df_industry = df_industry.copy()
        df_Input_pricing = df_Input_pricing.copy()
        df_Inputs_Portfolio_LeverageBorrowingBase = (
            df_Inputs_Portfolio_LeverageBorrowingBase.copy()
        )
        df_Obligors_Net_Capital = df_Obligors_Net_Capital.copy()
        df_Inputs_Advance_Rates = df_Inputs_Advance_Rates.copy()
        df_Inputs_Concentration_limit = df_Inputs_Concentration_limit.copy()
        df_principle_obligations = df_principle_obligations.copy()

        df_subscriptionBB = calculation_for_subscription(
            df_subscriptionBB, df_Inputs_Concentration_limit, df_Inputs_Advance_Rates
        )

        # I69
        total_capitalCalled = df_subscriptionBB["Capital Called"].sum()
        # J69

        total_uncalled_Capital = df_subscriptionBB["Uncalled Capital"].sum()

        df_PL_BB_Build = calculation_for_build(
            df_PL_BB_Build,
            df_Inputs_Other_Metrics,
            df_Availability_Borrower,
            total_capitalCalled,
            df_Inputs_Portfolio_LeverageBorrowingBase,
            total_uncalled_Capital,
            df_Obligors_Net_Capital,
        )

        # passing updated segemtation overview

        # df_segmentation_overview = calculation_for_Segmentation_overview(df_industry,df_PL_BB_Build)

        df_PL_BB_Results, df_security, df_industry = calculation_results_function_Call(
            df_PL_BB_Results,
            df_PL_BB_Build,
            df_Inputs_Other_Metrics,
            df_security,
            df_industry,
            df_Availability_Borrower,
        )

        df_Availability_Borrower = calculation_for_Availability(
            df_Availability_Borrower,
            df_subscriptionBB,
            df_PL_BB_Results,
            df_PL_BB_Build,
            df_Input_pricing,
        )
        df_segmentation_overview = calculation_for_Segmentation_overview(
            df_industry, df_PL_BB_Build
        )

        df_PL_BB_Build = df_PL_BB_Build.fillna(0)
        df_PL_BB_Output = intermediate_metrics(df_PL_BB_Build, df_PL_BB_Output)

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
            df_segmentation_overview,
            df_PL_BB_Output,
        )
    except Exception as e:
        raise Exception(e)
