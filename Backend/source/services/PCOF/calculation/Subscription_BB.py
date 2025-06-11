import numpy as np


def calculate_Uncalled_Capital(subscription_df):
    """<b>Uncalled Capital</b> in SubscriptionBB table is derived from two values corresponding to terms <b>Commitment</b> and <b>Capital Called</b> from SubscriptionBB table
    <br>
    <br>
    <b>Uncalled Capital</b> = <b>Commitment</b> - <b>Capital Called</b>
    """
    subscription_df["Uncalled Capital"] = (
        subscription_df["Commitment"] - subscription_df["Capital Called"]
    )
    return subscription_df


def calculate_percent_of_Uncalled(subscription_df, total_allInvestors):
    subscription_df["percent of Uncalled"] = subscription_df["Uncalled Capital"] / (
        total_allInvestors
    )
    return subscription_df


def calculate_of_Elig_Uncalled(subscription_df, Total_Eligible_Commitments, eligible_designations):
    subscription_df["percent of Elig Uncalled"] = subscription_df[
        "Uncalled Capital"
    ] / (Total_Eligible_Commitments)
    subscription_df["percent of Elig Uncalled"] = subscription_df.apply(
        lambda x: (x["Uncalled Capital"] / Total_Eligible_Commitments if x['Designation'] not in eligible_designations else np.nan),
        axis=1,
    )
    return subscription_df


# need to change value according to json values of inputs file
def return_Concentration_Limit(
    designation, Institutional_Investors_Investors, HNW_Investors_Individual
):
    match designation:
        case "Institutional Investors": return Institutional_Investors_Investors
        case "HNW Investors": return HNW_Investors_Individual
    return np.nan


def calculate_Concentration_Limit(
    subscription_df, Institutional_Investors_Investors, HNW_Investors_Individual
):
    subscription_df["Concentration_Limit"] = subscription_df["Designation"].apply(
        lambda x: return_Concentration_Limit(
            x, Institutional_Investors_Investors, HNW_Investors_Individual
        )
    )
    return subscription_df


def return_excess_concentration(x, y, Total_Eligible_Commitments):
    if x > y:
        return -(x - y) * Total_Eligible_Commitments
    else:
        return 0


def calculate_Excess_Concentration(subscription_df, Total_Eligible_Commitments):
    subscription_df["Excess Concentration"] = subscription_df.apply(
        lambda x: return_excess_concentration(
            x["percent of Elig Uncalled"],
            x["Concentration_Limit"],
            Total_Eligible_Commitments,
        ),
        axis=1,
    )
    return subscription_df


def calculate_Less_Excess_Conc(subscription_df):
    subscription_df["Less Excess Conc"] = (
        subscription_df["Uncalled Capital"] + subscription_df["Excess Concentration"]
    )
    return subscription_df


# need to change values from inputs files


def calculate_Advance_Rate(subscription_df, Institutional_Investors, HNW_Investors):
    subscription_df["Advance Rate"] = subscription_df["Designation"].apply(
        lambda x: (
            Institutional_Investors if x == "Institutional Investors" else HNW_Investors
        )
    )
    return subscription_df


def borrowing_rate(x, y):
    try:
        return x * y

    except:
        return "N/A"


def calculate_Borrowing_Base_subscription(subscription_df):
    """<b>Subscription Borrowing Base</b> in SubscriptionBB table is derived from two values corresponding to terms <b>Less Excess Conc.</b> and <b>Advance Rate</b> from SubscriptionBB table

    <b>Subscription Borrowing Base</b> = <b>Less Excess Conc.</b> * <b>Advance Rate</b>
    """
    subscription_df["Borrowing Base"] = subscription_df.apply(
        lambda x: borrowing_rate(x["Less Excess Conc"], x["Advance Rate"]), axis=1
    )
    return subscription_df
