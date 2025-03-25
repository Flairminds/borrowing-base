import math
import numpy as np
import pandas as pd

# --------------------------------------Jay's Code ----------------------------------------------------------


# R=MIN(N7,P7,Q7)
def FMV_helper(lis):
    try:
        min_value = min([x for x in lis if not math.isnan(x)])
        return min_value
    except:
        return np.nan


def FMV(data):
    # data['Investment FMV'] = data.apply(lambda x : FMV_helper([x['Investment Par'],x['Investment External Valuation'],x['Investment Internal Valuation']]),axis=1)
    data["Investment FMV"] = data[
        [
            "Investment Par",
            "Investment External Valuation",
            "Investment Internal Valuation",
        ]
    ].min(axis=1, skipna=True)
    return data


# -----------------------------------------------------------------------------------------


# BG=IFERROR(IF(AV13>=Inputs1$D$124,"Yes","No"),"N/A")
def Helper_EBITDA_Threshold(x, Other_metrics):
    try:
        match_index = Other_metrics[
            Other_metrics["Other Metrics"] == "Trailing 12-Month EBITDA"
        ].index[0]
        input_trailing_12_month_EBITDA = Other_metrics["values"].iloc[match_index]
        if x >= input_trailing_12_month_EBITDA:
            return "Yes"
        else:
            return "No"
    except:
        return "N/A"


def EBITDA_Threshold(data, Other_metrics):
    data["Test 1 EBITDA Threshold"] = data["Financials LTM EBITDA ($MMs)"].apply(
        lambda x: Helper_EBITDA_Threshold(x, Other_metrics)
    )
    return data


# -----------------------------------------------------------------------------------------


# BH=IF(BG25="Yes","N/A","Test")
def Test_applies(data, Other_metrics):
    df = EBITDA_Threshold(data, Other_metrics)
    df["Test 1 Test Applies?"] = df["Test 1 EBITDA Threshold"].apply(
        lambda x: "N/A" if x == "Yes" else "Test"
    )
    return df


# -----------------------------------------------------------------------------------------


# BI=IFERROR(IF(BG16="Yes","Yes",IF(BA16<Inputs1$D$126,"Yes","No")),"N/A")
def Helper_Leverage_greater_than_45x(et, tl, Other_metrics):
    try:
        match_index = Other_metrics[
            Other_metrics["Other Metrics"] == "Total Leverage"
        ].index[0]
        input_total_leverage = Other_metrics["values"].iloc[match_index]

        if et == "Yes":
            return "Yes"
        else:
            if tl < input_total_leverage or np.isnan(tl):
                return "Yes"
            else:
                return "No"

    except:
        return "N/A"


def Leverage_greater_than_45x(data, Other_metrics):
    df = EBITDA_Threshold(data, Other_metrics)
    df["Test 1 Leverage < 4.5x"] = df.apply(
        lambda x: Helper_Leverage_greater_than_45x(
            x["Test 1 EBITDA Threshold"], x["Leverage Total Leverage"], Other_metrics
        ),
        axis=1,
    )
    return df


# -----------------------------------------------------------------------------------------

# AS=IF(OR(AO12="Yes",AP12="Yes",AQ12="Yes",AR12="Yes"),"No","Yes")


def Classification_Eligible(data):
    data["Classification Eligible"] = data.apply(
        lambda x: (
            "No"
            if x["Classifications Structured Finance Obligation"] == "Yes"
            or x["Classifications Third Party Finance Company"] == "Yes"
            or x["Classifications Affiliate Investment"] == "Yes"
            or x["Classifications Defaulted / Restructured"] == "Yes"
            else "Yes"
        ),
        axis=1,
    )
    return data


# -----------------------------------------------------------------------------------------


# BJ=IFERROR(IF(BG16="Yes","Yes",IF(BE16<=Inputs1$D$127,"Yes","No")),"N/A")
def Helper_LTV_greater_than_65(et, pcof, Other_metrics):
    try:
        match_index = Other_metrics[Other_metrics["Other Metrics"] == "LTV"].index[0]
        input_LTV = Other_metrics["values"].iloc[match_index]
        if et == "Yes":
            return "Yes"
        else:
            if pcof < input_LTV or np.isnan(pcof):
                return "Yes"
            else:
                return "No"

    except:
        return "N/A"


def LTV_greater_than_65(data, Other_metrics):
    df = EBITDA_Threshold(data, Other_metrics)
    df["Test 1 LTV < 65%"] = df.apply(
        lambda x: Helper_LTV_greater_than_65(
            x["Test 1 EBITDA Threshold"], x["Leverage LTV Thru PCOF IV"], Other_metrics
        ),
        axis=1,
    )
    return df


# -----------------------------------------------------------------------------------------


# BK=IF(BG16="Yes","Yes",IF(AND(BI16="No",BJ16="No"),"No","Yes"))
def Pass_1(data, Other_metrics):
    data["Test 1 EBITDA Threshold"] = EBITDA_Threshold(data, Other_metrics)[
        "Test 1 EBITDA Threshold"
    ]
    data["Test 1 Leverage < 4.5x"] = Leverage_greater_than_45x(data, Other_metrics)[
        "Test 1 Leverage < 4.5x"
    ]
    data["Test 1 LTV < 65%"] = LTV_greater_than_65(data, Other_metrics)[
        "Test 1 LTV < 65%"
    ]
    data["Test 1 Pass"] = data.apply(
        lambda x: (
            "Yes"
            if x["Test 1 EBITDA Threshold"] == "Yes"
            else (
                "No"
                if x["Test 1 Leverage < 4.5x"] == "No" and x["Test 1 LTV < 65%"] == "No"
                else "Yes"
            )
        ),
        axis=1,
    )
    return data


# ------------------------------------------------------------------------------------


# BR=IF(OR(AS15="No",BK15="No",BP15="No"),"No","Yes")
def Final_Eligible(data, Other_metrics):
    data["Classification Eligible"] = Classification_Eligible(data)[
        "Classification Eligible"
    ]
    data["Test 1 Pass"] = Pass_1(data, Other_metrics)["Test 1 Pass"]
    data["Final Eligible"] = data.apply(
        lambda x: (
            "No"
            if x["Classification Eligible"] == "No"
            or x["Test 1 Pass"] == "No"
            or x["Final Eligibility Override"] == "No"
            else "Yes"
        ),
        axis=1,
    )
    return data


# ------------------------------------------------------------------------------------


# BW=IF($BR12="Yes",MIN(R12,O12,N12),0)
def Helper_Portfolio_Eligible_Amount(lis):
    try:
        min_value = min([x for x in lis if not math.isnan(x)])
        return min_value
    except:
        return np.nan


def Portfolio_Eligible_Amount(data, Other_metrics):
    data["Investment FMV"] = FMV(data)["Investment FMV"]
    data["Final Eligible"] = Final_Eligible(data, Other_metrics)["Final Eligible"]
    data["Portfolio Eligible Amount"] = data.apply(
        lambda x: (
            Helper_Portfolio_Eligible_Amount(
                [
                    float(x["Investment FMV"]),
                    float(x["Investment Cost"]),
                    float(x["Investment Par"]),
                ]
            )
            if x["Final Eligible"] == "Yes"
            else 0
        ),
        axis=1,
    )

    return data


# ------------------------------------------------------------------------------------


# BY=IF(BR9="Yes",BW9/$BW$46,0)
def Eligible_percent_FMV_Eligible_excluding_cash(data, Other_metrics):
    data["Final Eligible"] = Final_Eligible(data, Other_metrics)["Final Eligible"]
    data["Portfolio Eligible Amount"] = Portfolio_Eligible_Amount(data, Other_metrics)[
        "Portfolio Eligible Amount"
    ]
    addition = data[data["Is Eligible Issuer"] == "Yes"][
        "Portfolio Eligible Amount"
    ].sum()
    try:
        match_index = data[data["Investment Name"] == "Cash"].index[0]
        value = data["Portfolio Eligible Amount"].iloc[match_index]
    except Exception as e:
        value = 0

    bw46 = addition - value
    data["Eligible % FMV Eligible (excluding cash)"] = data.apply(
        lambda x: (
            x["Portfolio Eligible Amount"] / bw46 if x["Final Eligible"] == "Yes" else 0
        ),
        axis=1,
    )
    return data


# ------------------------------------------------------------------------------------

# M=IFERROR((L8-$E$4)/365," ")


# M=IFERROR((L8-$E$4)/365," ")
def Helper_Investment_Tenor(value, Borrower):
    try:
        match_index = Borrower[Borrower["A"] == "Date of determination:"].index[0]
        date = Borrower["B"].iloc[match_index]
        output = (value - date) / pd.Timedelta(days=365)
    except IndexError:
        return "The input Column does not exist"
    except:
        output = " "
    return output


def Investment_Tenor(data, Borrower):
    data["Investment Maturity"] = pd.to_datetime(data["Investment Maturity"])
    data["Investment Tenor"] = data.apply(
        lambda x: Helper_Investment_Tenor(x["Investment Maturity"], Borrower), axis=1
    )
    return data


# def Helper_Investment_Tenor(value,data_as_of_now):
#     try:
#         # match_index = Borrower[Borrower['Availability']=='Date of determination:'].index[0]
#         # date = Borrower['DATA'].iloc[match_index]
#         # output = (value - date) / pd.Timedelta(days=365)

#         # return output

#         return (value-data_as_of_now)/365

#     except:
#       return " "

# def tenorM(df, colDatedf, df1, colDatedf1, target_column):
#     dateOfDetermination = df[colDatedf].iloc[0]
#     dateOfDetermination = pd.to_datetime(dateOfDetermination)

#     df1[target_column] = (df1[colDatedf1] - dateOfDetermination).dt.days / 365.25

#     df1[target_column] = df1[target_column].round(2)

#     return df1


# def Investment_Tenor(data,data_as_of_now):
#     data['Investment Tenor']=data.apply(lambda x : Helper_Investment_Tenor(x['Investment Maturity'],data_as_of_now),axis=1)
#     # data['Investment Maturity'] = pd.to_datetime(data['Investment Maturity'])
#     # data['Investment Tenor'] = data.apply(lambda x: Helper_Investment_Tenor(x['Investment Maturity'],Borrower),axis=1)
#     return data
# ------------------------------------------------------------------------------------


# CB=IFERROR(BY9*M9,0)
def Helper_Weighted_maturity(epf, it):
    try:
        return epf * it
    except:
        return 0


def Weighted_maturity(data, Other_metrics, Borrower):
    data["Eligible % FMV Eligible (excluding cash)"] = (
        Eligible_percent_FMV_Eligible_excluding_cash(data, Other_metrics)[
            "Eligible % FMV Eligible (excluding cash)"
        ]
    )
    data["Investment Tenor"] = Investment_Tenor(data, Borrower)["Investment Tenor"]
    data["Weighted Maturity"] = data.apply(
        lambda x: Helper_Weighted_maturity(
            x["Investment Tenor"], x["Eligible % FMV Eligible (excluding cash)"]
        ),
        axis=1,
    )
    return data


# ------------------------------------------------------------------------------------


# BT=IF($BR14="Yes",E14,"")
def Eligible_Issuer(data, Other_metrics):
    data["Final Eligible"] = Final_Eligible(data, Other_metrics)["Final Eligible"]
    data["Eligible Issuer"] = data.apply(
        lambda x: x["Investment Name"] if x["Final Eligible"] == "Yes" else "", axis=1
    )
    return data


# ------------------------------------------------------------------------------------


# BU=IF($BR11="Yes",J11,"")
def Eligible_Industry(data, Other_metrics):
    data["Final Eligible"] = Final_Eligible(data, Other_metrics)["Final Eligible"]
    data["Eligible Industry"] = data.apply(
        lambda x: x["Investment Industry"] if x["Final Eligible"] == "Yes" else "",
        axis=1,
    )
    return data


# ------------------------------------------------------------------------------------


# CA=IFERROR(BY14*AV14,"NA")
def Helper_Weighted_LTM_EBITDA(epf, it):
    try:
        return epf * it
    except:
        return "N/A"


def Weighted_LTM_EBITDA(data, Other_metrics):
    data["Eligible % FMV Eligible (excluding cash)"] = (
        Eligible_percent_FMV_Eligible_excluding_cash(data, Other_metrics)[
            "Eligible % FMV Eligible (excluding cash)"
        ]
    )
    data["Weighted LTM EBITDA"] = data.apply(
        lambda x: Helper_Weighted_LTM_EBITDA(
            x["Eligible % FMV Eligible (excluding cash)"],
            x["Financials LTM EBITDA ($MMs)"],
        ),
        axis=1,
    )
    return data


# -----------------------------------------------------------------------------------


# CJ Calculation
# =IFERROR(BW11+CH11,"n/a")
def calculate_Concentration_Adj_Elig_Amount(data, Other_metrics):
    """
    <b>Concentration Adj. Elig. Amount</b> in PL BB Build table is derived from the values of <b>Concentration Adjustment</b> and <b>Portfolio Eligible Amount</b> of PL BB Build table
    <br>
    <b>Concentration Adj. Elig. Amount</b> = # =IFERROR(<b>Concentration Adjustment</b>+<b>Portfolio Eligible Amount</b>,"n/a")
    """
    data["Concentration Adjustment"] = data["Concentration Adjustment"].replace(
        np.nan, 0
    )
    data["Portfolio Eligible Amount"] = Portfolio_Eligible_Amount(data, Other_metrics)[
        "Portfolio Eligible Amount"
    ]
    data["Concentration Adj. Elig. Amount"] = data.apply(
        lambda x: calculate_Concentration_Adj_Elig_Amount_helper(
            x["Concentration Adjustment"], x["Portfolio Eligible Amount"]
        ),
        axis=1,
    )

    return data


def calculate_Concentration_Adj_Elig_Amount_helper(x, y):
    try:
        c = x + y
    except:
        c = 0
        # c = "n/a"
    return c


# -----------------------------------------------------------------------------------


# CK calculation
# =IFERROR(CJ7/$CJ$46,"n/a")
def calculate_percent_Adj_Elig_Amount_excluding_cash(data, Other_metrics):
    data["Concentration Adj. Elig. Amount"] = calculate_Concentration_Adj_Elig_Amount(
        data, Other_metrics
    )["Concentration Adj. Elig. Amount"]
    addition = data[data["Is Eligible Issuer"] == "Yes"][
        "Concentration Adj. Elig. Amount"
    ].sum()
    try:
        match_index = data[data["Investment Name"] == "Cash"].index[0]
        value = data["Concentration Adj. Elig. Amount"].iloc[match_index]
    except Exception as e:
        value = 0

    cj46 = addition - value
    data["Concentration % Adj. Elig. Amount (excluding cash)"] = data.apply(
        lambda x: calculate_percent_Adj_Elig_Amount_excluding_cash_helper(
            x["Concentration Adj. Elig. Amount"], cj46
        ),
        axis=1,
    )
    return data


def calculate_percent_Adj_Elig_Amount_excluding_cash_helper(x, div):
    try:
        c = x / div
    except:
        c = "n/a"
    return c


# -----------------------------------------------------------------------------------


# (Weighted Average - Adj. Eligible Portfolio) is a variable which returns weighted average
# BB50 =+ SUMPRODUCT(BB$7:BB$32,$CK$7:$CK$32)
def Weighted_Average_leverage_thru_Borrower(data, Other_metrics):
    data["Concentration % Adj. Elig. Amount (excluding cash)"] = (
        calculate_percent_Adj_Elig_Amount_excluding_cash(data, Other_metrics)[
            "Concentration % Adj. Elig. Amount (excluding cash)"
        ]
    )
    df = pd.DataFrame()

    df["output"] = data.apply(
        lambda x: x["Concentration % Adj. Elig. Amount (excluding cash)"]
        * x["Leverage PCOF IV Leverage"],
        axis=1,
    )
    df2 = pd.DataFrame()
    df2["op"] = df["output"].dropna()
    return sum(df2["op"])


def Weighted_Average_Adj_Eligible_Portfolio(data, Other_metrics):
    data["Concentration % Adj. Elig. Amount (excluding cash)"] = (
        calculate_percent_Adj_Elig_Amount_excluding_cash(data, Other_metrics)[
            "Concentration % Adj. Elig. Amount (excluding cash)"
        ]
    )
    df = pd.DataFrame()

    df["output"] = data.apply(
        lambda x: x["Concentration % Adj. Elig. Amount (excluding cash)"]
        * x["Investment Tenor"],
        axis=1,
    )
    df2 = pd.DataFrame()
    df2["op"] = df["output"].dropna()
    return sum(df2["op"])


# #Availability

# #----------------------------------------------------------------------------------
# #D18=IF('[1]PL BB Results'!G18>=8,"Yes","No")
# def Portfolio_greater_than_8_Eligible_Issuers(avail,results):
#     match_index = results[results['Concentration Tests']=='Min. Eligible Issuers (#)'].index[0]
#     function_which_return_G18_from_PLBBResult = results['Actual'].iloc[match_index]
#     if function_which_return_G18_from_PLBBResult >=8:
#         new_dict = {'Availability':'Portfolio > 8 Eligible Issuers?','DATA':'Yes'}
#         avail.loc[len(avail)] = new_dict
#     else:
#         new_dict = {'Availability':'Portfolio > 8 Eligible Issuers?','DATA':'No'}
#         avail.loc[len(avail)] = new_dict
#     return avail

# #D19=(('PL BB Build'!CJ35)-SUMIF('PL BB Build'!$AE$7:$AE$34,"Warehouse First Lien",'PL BB Build'!$CJ$7:$CJ$34))
# def Portfolio_FMV_of_Portfolio(avail,pl_bb_build,results):
#     cash = 4456822
#     value =  pl_bb_build[pl_bb_build['Is Eligible Issuer'] == 'Yes']['Concentration Adj. Elig. Amount'].sum() + cash
#     classification_of_bb =  pl_bb_build[pl_bb_build['Classifications Classification for BB'] == 'Warehouse First Lien']['Concentration Adj. Elig. Amount'].sum()
#     new_dict = {'Availability':'Portfolio FMV of Portfolio','DATA':value-classification_of_bb}
#     avail.loc[len(avail)] = new_dict
#     return avail


# #D21=IF(D18="Yes",'[1]PL BB Build'!DP35,0)
# def Portfolio_Portfolio_Leverage_Borrowing_Base(avail,pl_bb_build,results):
#     cash = 4456822
#     avail = Portfolio_greater_than_8_Eligible_Issuers(avail,results)
#     match_index = avail[avail['Availability']=='Portfolio > 8 Eligible Issuers?'].index[0]
#     Portfolio_greater_than_8_Eligible_Issuer_value = avail['DATA'].iloc[match_index]
#     if Portfolio_greater_than_8_Eligible_Issuer_value == 'Yes':
#         value =  pl_bb_build[pl_bb_build['Is Eligible Issuer'] == 'Yes']['Borrowing Borrowing Base'].sum() + cash
#         new_dict = {'Availability':'Portfolio Portfolio Leverage Borrowing Base (as calculated)','DATA':value}
#         avail.loc[len(avail)] = new_dict
#     else:
#         new_dict = {'Availability':'Portfolio Portfolio Leverage Borrowing Base (as calculated)','DATA':0}
#         avail.loc[len(avail)] = new_dict
#     return avail

# #D20=IFERROR(D21/D19,"N/A")
# def Portfolio_Effective_Advance_Rate_on_FMV_of_Portfolio(avail,pl_bb_build,results):
#     avail = Portfolio_FMV_of_Portfolio(avail,pl_bb_build,results)
#     avail = Portfolio_Portfolio_Leverage_Borrowing_Base(avail,pl_bb_build,results)

#     match_index_fmv = avail[avail['Availability']=='Portfolio FMV of Portfolio'].index[0]
#     FMV_of_Portfolio = avail['DATA'].iloc[match_index_fmv]
#     match_index_lbb = avail[avail['Availability']=='Portfolio Portfolio Leverage Borrowing Base (as calculated)'].index[0]
#     Portfolio_Leverage_Borrowing_Base = avail['DATA'].iloc[match_index_lbb]

#     try:
#         value = FMV_of_Portfolio/Portfolio_Leverage_Borrowing_Base
#         new_dict = {'Availability':'Portfolio Effective Advance Rate on FMV of Portfolio','DATA':value}
#         avail.loc[len(avail)] = new_dict

#     except:
#         new_dict = {'Availability':'Portfolio Effective Advance Rate on FMV of Portfolio','DATA':'N/A'}
#         avail.loc[len(avail)] = new_dict

# #D22=IF('PL BB Results'!$G$28>Inputs!$D$11,Inputs!$D$11,Inputs!$D$12)
# #inputs contain pricing table import that
# def Portfolio_Maximum_Advance_Rate_on_PL_Borrowing_Base(results,pricing,avail):

#     match_index_FC = results[results['Concentration Tests']=='Min. Cash, First Lien, and Cov-Lite'].index[0]
#     function_which_return_G28_from_PLBBResult = results['Actual'].iloc[match_index_FC]

#     match_index_mf = pricing[pricing['Pricing']==r'Min. First Lien / Last Out Contribution to PL BB for 65% Effective A/R'].index[0]
#     contribution_for_65_effective = pricing['percent'].iloc[match_index_mf]
#     match_index_d12 = pricing[pricing['Pricing']=='Lower Effective A/R'].index[0]
#     lower_effective_ar = pricing['percent'].iloc[match_index_d12]
#     if function_which_return_G28_from_PLBBResult > contribution_for_65_effective:
#         new_dict = {'Availability':'Portfolio Maximum Advance Rate on PL Borrowing Base','DATA': contribution_for_65_effective}
#         avail.loc[len(avail)] = new_dict

#     else:
#         new_dict = {'Availability':'Portfolio Maximum Advance Rate on PL Borrowing Base','DATA': lower_effective_ar}
#         avail.loc[len(avail)] = new_dict
#     return avail


# ---------------------------------------------------------------Disha's Code-----------------------------------------------------


# BW is calculated by jai


# CJ Calculation  #done
# =IFERROR(BW11+CH11,"n/a")
def calculate_Concentration_Adj_Elig_Amount(data, oth_metr):
    """
    <b>Concentration Adj. Elig. Amount</b> derived from PL BB Build table using terms <b>Concentration Adjustment</b> and <b>Portfolio Eligible Amount</b> from PL BB Build table

    <b>Concentration Adj. Elig. Amount</b> = <b>Concentration Adjustment</b> + <b>Portfolio Eligible Amount</b>
    """
    # data = Portfolio_Eligible_Amount(data,oth_metr)
    data["Concentration Adjustment"] = data["Concentration Adjustment"].replace(
        np.nan, 0
    )
    data["Concentration Adj. Elig. Amount"] = data.apply(
        lambda x: calculate_Concentration_Adj_Elig_Amount_helper(
            x["Concentration Adjustment"], x["Portfolio Eligible Amount"]
        ),
        axis=1,
    )

    return data


def calculate_Concentration_Adj_Elig_Amount_helper(x, y):
    try:
        c = x + y
    except:
        # c = "n/a"
        c = 0
    return c


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# CC Function    #DONE  #changes in div calculation
# =IFERROR(IF(AC7="Fixed",CJ7/(SUMIF($AC$7:$AC$32,"Fixed",$CJ$7:$CJ$32)),0),0)


def calculate_Weighted_Percent_Fixed(data, oth_metr):
    data = calculate_Concentration_Adj_Elig_Amount(data, oth_metr)
    sum_floating = data.loc[
        data["Rates Fixed / Floating"] == "Fixed", "Concentration Adj. Elig. Amount"
    ].sum()

    # Create a new column 'Weighted Percent Fixed' and initialize with zeros
    data["Weighted Percent Fixed"] = 0

    # Calculate the weighted percentage for rows where 'Rates Fixed / Floating' is 'Floating'
    floating_mask = data["Rates Fixed / Floating"] == "Fixed"
    data.loc[floating_mask, "Weighted Percent Fixed"] = (
        data.loc[floating_mask, "Concentration Adj. Elig. Amount"] / sum_floating
    )
    return data


#     div = data['Concentration Adj. Elig. Amount'].sum()
#     data['Weighted Percent Fixed'] = data.apply(lambda x : calculate_Weighted_Percent_Fixed_helper(x['Rates Fixed / Floating'],x['Concentration Adj. Elig. Amount'],div),axis=1)
#     return data
# def calculate_Weighted_Percent_Fixed_helper(string_cur,Adj_elig_amount,div):
#     if string_cur=='Fixed':
#         return Adj_elig_amount/div
#     else:
#         return 0

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# CD Calculation # DONE
# =CC7*$W7
def calculate_weighted_fixed(data, oth_metr):
    data = calculate_Weighted_Percent_Fixed(data, oth_metr)
    data["Rates Fixed Coupon"] = data["Rates Fixed Coupon"].replace(np.nan, 0)
    data["Weighted Fixed"] = data.apply(
        lambda x: (x["Weighted Percent Fixed"] * x["Rates Fixed Coupon"]), axis=1
    )
    return data


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# CE Calculation  #DONE # calculated in percent
# IF(AC7="Floating",CJ7/(SUMIF($AC$7:$AC$32,"Floating",$CJ$7:$CJ$32)),0)
def calculate_Weighted_Percent_Floating(data, oth_metr):
    data = calculate_Concentration_Adj_Elig_Amount(data, oth_metr)
    sum_floating = data.loc[
        data["Rates Fixed / Floating"] == "Floating", "Concentration Adj. Elig. Amount"
    ].sum()

    # Create a new column 'Weighted Percent Fixed' and initialize with zeros
    data["Weighted Percent Floating"] = 0

    # Calculate the weighted percentage for rows where 'Rates Fixed / Floating' is 'Floating'
    floating_mask = data["Rates Fixed / Floating"] == "Floating"
    data.loc[floating_mask, "Weighted Percent Floating"] = (
        data.loc[floating_mask, "Concentration Adj. Elig. Amount"] / sum_floating
    )
    return data


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# CF Calculation  #DONE #value is calculate in percent
# =IFERROR(CE7*$X7,0)
def calculate_Weighted_Floating(data, oth_metr):
    data = calculate_Weighted_Percent_Floating(data, oth_metr)
    data["Rates Floating Cash Spread"] = data["Rates Floating Cash Spread"].replace(
        np.nan, 0
    )
    data["Weighted Floating"] = data.apply(
        lambda x: calculate_Weighted_Floating_helper(
            x["Weighted Percent Floating"], x["Rates Floating Cash Spread"]
        ),
        axis=1,
    )
    return data


def calculate_Weighted_Floating_helper(x, y):
    try:
        c = x * y
    except:
        c = 0
    return c


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# CK calculation
# =IFERROR(CJ7/$CJ$46,"n/a")
def calculate_Concentration_Percent_Adj_Elig_Amount_Excluding_Cash(data, oth_metr):
    data = calculate_Concentration_Adj_Elig_Amount(data, oth_metr)
    div = data[data["Is Eligible Issuer"] == "Yes"][
        "Concentration Adj. Elig. Amount"
    ].sum()
    data["Concentration % Adj. Elig. Amount (excluding cash)"] = data.apply(
        lambda x: calculate_Concentration_Percent_Adj_Elig_Amount_Excluding_Cash_helper(
            x["Concentration Adj. Elig. Amount"], div
        ),
        axis=1,
    )
    return data


def calculate_Concentration_Percent_Adj_Elig_Amount_Excluding_Cash_helper(x, div):
    try:
        c = x / div
    except:
        c = "n/a"
    return c


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# CL Calculation    #DONE         #Doubt about div value
# =IFERROR(CJ7/('PL BB Results'!$F$13),"n/a")
def calculate_concentration_percent_of_ONC(data, df_Obligors_Net_Capital):
    div = df_Obligors_Net_Capital[
        df_Obligors_Net_Capital["Obligors' Net Capital"]
        == "Obligors' Net Capital ((a) + (b))"
    ]["values"].iloc[0]

    data["Concentration % of ONC"] = data.apply(
        lambda x: calculate_concentration_percent_of_ONC_helper(
            x["Concentration Adj. Elig. Amount"], div
        ),
        axis=1,
    )
    return data


def calculate_concentration_percent_of_ONC_helper(x, div):
    try:
        c = x / div
    except:
        c = "n/a"

    return c


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# AE Function  #DONE
def calculate_Classification_Classification_for_BB(data):
    """
    <b>Classifications Classification for BB</b> in PL BB Build table is derived from the  value of <b>Investment Investment Type</b> of PL BB Build table
    <br>
    <b>Classifications Classification for BB</b> = <b>Investment Investment Type</b>
    """
    data["Classifications Classification for BB"] = data[
        "Investment Investment Type"
    ]  # spelling mistake in first investment

    return data


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# BM Function # DONE
# IF(AE7="Last Out",IF(BC7>Inputs!$D$122,"Yes","No")," ")
def calculate_Classification_Adj_Last_Out_Attachment(data, oth_metr):
    idx = oth_metr[oth_metr["Other Metrics"] == "Last Out Attachment Point"].index[0]
    Last_Out_Attachment_Point = oth_metr["values"].iloc[idx]

    data = calculate_Classification_Classification_for_BB(data)

    data["Classification Adj. Last Out Attachment > 2.25x"] = data.apply(
        lambda x: calculate_Last_Out_Attachment_helper(
            x["Classifications Classification for BB"],
            x["Leverage Attachment Point"],
            Last_Out_Attachment_Point,
        ),
        axis=1,
    )
    return data


def calculate_Last_Out_Attachment_helper(x, y, Last_Out_Attachment_Point):
    if x == "Last Out":
        if y > Last_Out_Attachment_Point:
            return "Yes"

        else:
            return "No"

    else:
        return " "


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# BN Calculation    #DONE (DOUBT = =+IF, significance of + in the equality)
# =+IF(AND(AE7=Inputs!$C$45,BM7="Yes"),Inputs!$C$46,AE7)
def calculate_Classification_Adjusted_Type(data, Adv_Rates, oth_metr):
    data = calculate_Classification_Classification_for_BB(data)
    data = calculate_Classification_Adj_Last_Out_Attachment(data, oth_metr)

    last_out = Adv_Rates["Investment Type"][5]
    Second_Lien = Adv_Rates["Investment Type"][6]

    data["Classification Adj. Adjusted Type"] = data.apply(
        lambda x: calculate_Classification_Adjusted_Type_helper(
            x["Classifications Classification for BB"],
            x["Classification Adj. Last Out Attachment > 2.25x"],
            last_out,
            Second_Lien,
        ),
        axis=1,
    )

    return data


def calculate_Classification_Adjusted_Type_helper(x, y, last_out, Second_Lien):
    if x == last_out and y == "Yes":
        return Second_Lien

    else:
        return x


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# BV Calculation #DONE
# =IF($BR7="Yes",BN7,"")
def calculate_Potfolio_type(data, Adv_Rates, oth_metr):
    data = calculate_Classification_Adjusted_Type(data, Adv_Rates, oth_metr)
    # data = Final_Eligible(data)
    data["Portfolio Type"] = data.apply(
        lambda x: (
            x["Classification Adj. Adjusted Type"]
            if x["Final Eligible"] == "Yes"
            else ""
        ),
        axis=1,
    )
    return data


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# CO Calculation
# IFERROR(IF(AF7="unquoted",(INDEX(Inputs!$C$40:$E$52,MATCH(BV7,Inputs!$C$40:$C$52,0),2)),IF(AF7="quoted",(INDEX(Inputs!$C$40:$E$52,MATCH(BV7,Inputs!$C$40:$C$52,0),3)),"n/a")),"n/a")
def calculate_Adv_Adv_Rate(data, Adv_Rates, oth_metr):
    data = calculate_Potfolio_type(data, Adv_Rates, oth_metr)
    data["Adv. Adv. Rate"] = data.apply(
        lambda x: calculate_Adv_Adv_Rate_helper(
            x["Classifications Quoted / Unquoted"], x["Portfolio Type"], Adv_Rates
        ),
        axis=1,
    )
    return data


def calculate_Adv_Adv_Rate_helper(x, y, Adv_Rates):
    try:
        if x == "Unquoted":
            matched_index = Adv_Rates[Adv_Rates["Investment Type"] == y].index[0]
            res = Adv_Rates["Unquoted"].iloc[matched_index]
        else:
            if x == "Quoted":
                matched_index = Adv_Rates[Adv_Rates["Investment Type"] == y].index[0]
                res = Adv_Rates["Quoted"].iloc[matched_index]

            else:
                res = "n/a"
    except:
        res = "n/a"

    return res


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# AZ Calculation #DONE
# =IF(AX7=0,0,AX7/AY7)
def calculate_Leverage_Revolver_percent_of_TEV(data):
    data["Leverage Revolver Commitment"] = data["Leverage Revolver Commitment"].replace(
        np.nan, 0
    )
    data["Leverage Total Enterprise Value"] = data[
        "Leverage Total Enterprise Value"
    ].replace(np.nan, 0)
    data["Leverage Revolver percent of TEV"] = data.apply(
        lambda x: calculate_Leverage_Revolver_percent_of_TEV_helper(
            x["Leverage Revolver Commitment"], x["Leverage Total Enterprise Value"]
        ),
        axis=1,
    )

    return data


def calculate_Leverage_Revolver_percent_of_TEV_helper(x, y):
    if x == 0:
        return 0

    else:
        return x / y


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# CQ Calculation #DONE
# =IF(AZ7>15%,"Yes","No")
def calculate_Revolver_Rev_greater_than_15_percent_TEV(data):
    data = calculate_Leverage_Revolver_percent_of_TEV(data)
    data["Revolver Rev. > 15% TEV"] = data.apply(
        lambda x: "Yes" if (x["Leverage Revolver percent of TEV"] > 0.15) else "No",
        axis=1,
    )
    return data


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# CR Calculation
# IF(OR(CQ7="No",CO7="n/a"),CO7,IF(AF7="unquoted",MIN(Inputs!$D$46,CO7),MIN(Inputs!$E$46,CO7)))
def calculate_Revolver_Adj_Advance_Rate(data, Adv_Rates, oth_metr):
    idx1 = Adv_Rates[Adv_Rates["Investment Type"] == "Second Lien"].index[0]

    adv_unquo = Adv_Rates["Unquoted"].iloc[idx1]
    adv_quo = Adv_Rates["Quoted"].iloc[idx1]

    data = calculate_Adv_Adv_Rate(data, Adv_Rates, oth_metr)
    data = calculate_Revolver_Rev_greater_than_15_percent_TEV(data)

    data["Revolver Adj. Advance Rate"] = data.apply(
        lambda x: calculate_Revolver_Adj_Advance_Rate_helper(
            x["Revolver Rev. > 15% TEV"],
            x["Adv. Adv. Rate"],
            x["Classifications Quoted / Unquoted"],
            adv_quo,
            adv_unquo,
        ),
        axis=1,
    )

    return data


def calculate_Revolver_Adj_Advance_Rate_helper(x, y, z, adv_quo, adv_unquo):
    if x == "No" or y == "n/a":
        res = y
    else:
        if z == "Unquoted":
            res = min([adv_unquo, y])
        else:
            res = min([adv_quo, y])

    return res


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# CT Calculation #DONE
# =IF(CJ7="n/a","N/A",IF(AND(CJ7>0,AE7="First Lien",BB7>Inputs!$D$120),(BB7-Inputs!$D$120)/BB7,0))
def calculate_First_Second_Lien_Share(data, oth_metr):
    idx = oth_metr[
        oth_metr["Other Metrics"] == "First Lien Leverage Cut-Off Point"
    ].index[0]

    con = oth_metr["values"].iloc[idx]

    data = calculate_Concentration_Adj_Elig_Amount(data, oth_metr)

    data = calculate_Classification_Classification_for_BB(data)

    try:
        data["First Lien Second Lien Share"] = data.apply(
            lambda x: calculate_First_Second_Lien_Share_helper(
                x["Concentration Adj. Elig. Amount"],
                x["Classifications Classification for BB"],
                x["Leverage PCOF IV Leverage"],
                con,
            ),
            axis=1,
        )
    except Exception as e:
        raise Exception(e)

    return data


def calculate_First_Second_Lien_Share_helper(x, y, z, con):
    if x == "n/a":
        res = "N/A"

    else:
        if x > 0 and y == "First Lien" and float(z) > float(con):
            res = (float(z) - float(con)) / float(z)
        else:
            res = 0
    return res


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# CU Calculation  #DONE
# IF(CT7="N/a","n/a",IF(CT7=0,0,IF(CT7>0,IF(AF7="Unquoted",Inputs!$D$46,IF(AF7="Quoted",Inputs!$E$46,"n/a")))))
def calculate_First_Second_Lien_Rate(data, Adv_Rates, oth_metr):
    idx = Adv_Rates[Adv_Rates["Investment Type"] == "Second Lien"].index[0]
    con1 = Adv_Rates["Unquoted"].iloc[idx]
    con2 = Adv_Rates["Quoted"].iloc[idx]

    data = calculate_First_Second_Lien_Share(data, oth_metr)

    data["First Lien Second Lien Rate"] = data.apply(
        lambda x: calculate_First_Second_Lien_Rate_helper(
            x["First Lien Second Lien Share"],
            x["Classifications Quoted / Unquoted"],
            con1,
            con2,
        ),
        axis=1,
    )

    return data


def calculate_First_Second_Lien_Rate_helper(x, y, con1, con2):
    if x == "N/a":
        res = "n/a"

    else:
        if x == 0:
            res = 0
        else:
            if x > 0:
                if y == "Unquoted":
                    res = con1
                else:
                    if y == "Quoted":
                        res = con2
                    else:
                        res = "n/a"
    return res


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# #M Calculation
# #=IFERROR((L7-$E$4)/365," ")

# def calculate_Investment_Tenor(data,avail):

#     data['Investment Tenor'] = data.apply(lambda x: calculate_Investment_Tenor_helper(x['Investment Maturity'],avail),axis=1)
#     return data

# def calculate_Investment_Tenor_helper(x,avail):
#     try:

#         idx = avail[avail['Availability']=='Date of determination:'].index[0]
#         date = avail['DATA'].iloc[idx]
#         yr = round((x-date)/pd.Timedelta(days=365),1)
#         # yr = YEARFRAC (date, x,3)
#     except:
#         yr = ' '

#     return yr

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# #CB Calculation
# #=+SUMPRODUCT(M$7:M$32,$CK$7:$CK$32)
# def calculate_WA_Adj_Eligible_Portfolio(data,oth_metr,avail):
#     data = calculate_Concentration_Percent_Adj_Elig_Amount_Excluding_Cash(data,oth_metr)
#     data = Investment_Tenor(data,avail)

#     idx = avail[avail['Availability']=='Date of determination'].index[0]
#     date = avail['DATA'].iloc[idx]

#     # data['Investment Tenor'] = data['Investment Tenor'].astype(float)
#     data['Adj. Eligible Portfolio'] = data.apply(lambda x : x['Investment Tenor']*x['Concentration % Adj. Elig. Amount (excluding cash)'] if x['Is Eligible Issuer']=='Yes' else 0, axis=1)

#     WA = data['Adj. Eligible Portfolio'].sum()

#     return round(WA,4)

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# AVAILABILITY


# Months since Revolving Closing Date
def calculate_Months_since_Revolving_Closing_Date(avail):
    start_idx = avail[
        avail["Availability"] == "Subscription Revolving Closing Date"
    ].index[0]
    start = avail["DATA"].iloc[start_idx]

    end_idx = avail[avail["Availability"] == "Date of determination"].index[0]
    end = avail["DATA"].iloc[end_idx]

    diff = (end.year - start.year) * 12 + end.month - start.month

    new_row = {
        "Availability": "Subscription Months since Revolving closing Date",
        "DATA": diff,
    }
    avail.loc[len(avail)] = new_row

    # new_row = {'Name': 'Daniel virmalwat', 'Age': 32, 'City': 'Tokyo'}
    # df.loc[len(df)] = new_row
    return avail


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# Q69 Calulculation
# =Q38+Q66+Q68
def calculate_Total_All_Investors_Borrowing_Base(subscription):
    sum1 = calculate_total_eligible_committments_Borrowing_Base(subscription)
    sum2 = 0  # take from suscription sheet
    sum3 = 0  # take from suscription sheet

    return sum1 + sum2 + sum3


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# Q38 Calculation
# =Q20+Q36
def calculate_total_eligible_committments_Borrowing_Base(subscription):
    sum1 = subscription[subscription["Designation"] == "Institutional Investors"][
        "Borrowing Base"
    ].sum()
    sum2 = subscription[subscription["Designation"] == "High Net Worth Investors"][
        "Borrowing Base"
    ].sum()

    return sum1 + sum2


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# Subscription Borrowing Base
# D14
# IF(D11="Yes",'Subscription BB'!Q69,0)
def calculate_subscription_Borrowing_Base(avail, subscription):
    subscript = calculate_Total_All_Investors_Borrowing_Base(subscription)

    idx = avail[
        avail["Availability"]
        == "Subscription Commitment Period (3 years from Final Closing Date, as defined in LPA)"
    ].index[0]
    commit_period = avail["DATA"].iloc[idx]

    if commit_period == "Yes":
        val = subscript

    else:
        val = 0

    new_row = {"Availability": "Subscription Borrowing Base", "DATA": val}
    avail.loc[len(avail)] = new_row
    return avail


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# Availability
# D15 = D14/13
def calculate_Effective_Advance_Rate_on_Total_Uncalled_Capital(avail, subscription):
    try:
        avail = calculate_subscription_Borrowing_Base(avail, subscription)
        idx = avail[avail["Availability"] == "Subscription Borrowing Base"].index[0]
        num = avail["DATA"].iloc[idx]

        den = 76250000  # stored value as total_uncalled_capital
        # den = subscription['uncalled capital'].sum()

        val = num / den
    except:
        val = "N/A"

    return val


# --------------------------------------Laxmi's Code -----------------------------------------------------


# Warehouse_Day_Count
def calculate_Warehouse_Day_Count(df_PL_BB_Build, date_as_of):
    inclusion_date = df_PL_BB_Build["Classifications Warehouse Asset Inclusion Date"]
    df_PL_BB_Build["Classifications Warehouse Day Count"] = (
        (date_as_of - inclusion_date).fillna("") if inclusion_date.gt(0).all() else ""
    )
    return df_PL_BB_Build


# AB All_In
def calculate_All_In_helper(w, x, y, z):
    if pd.isna(w):
        w =0
    else:
        if math.isnan(w):
            w = 0
    if pd.isna(x):
        x = 0
    else:
        if math.isnan(x):
            x = 0
    if pd.isna(y):
        y = 0
    else:
        if math.isnan(y):
            y = 0
    if pd.isna(z):
        z = 0
    else:
        if math.isnan(z):
            z = 0
    return w + y + x + z


def calculate_All_In(df_PL_BB_Build):
    # df_PL_BB_Build['Rates Fixed Coupon']=df_PL_BB_Build['Rates Fixed Coupon'].fillna(0)
    # df_PL_BB_Build['Rates PIK']=df_PL_BB_Build['Rates PIK'].fillna(0)
    # df_PL_BB_Build['Rates Floating Cash Spread']=df_PL_BB_Build['Rates Floating Cash Spread'].fillna(0)
    # df_PL_BB_Build['Rates Current LIBOR/Floor']=df_PL_BB_Build['Rates Current LIBOR/Floor'].fillna(0)
    df_PL_BB_Build["Rates All_In"] = df_PL_BB_Build.apply(
        lambda x: calculate_All_In_helper(
            x["Rates Fixed Coupon"],
            x["Rates Current LIBOR/Floor"],
            x["Rates Floating Cash Spread"],
            x["Rates PIK"],
        ),
        axis=1,
    )

    # df_PL_BB_Build['Rates All-In']=df_PL_BB_Build['Rates Fixed Coupon']+df_PL_BB_Build['Rates PIK']+df_PL_BB_Build['Rates Floating Cash Spread']+df_PL_BB_Build['Rates Current LIBOR/Floor']
    return df_PL_BB_Build


# AA All_In_Cash
def calculate_All_In_Cash_helper(w, x, y):
    if math.isnan(w):
        w = 0
    if math.isnan(x):
        x = 0
    if math.isnan(y):
        y = 0

    return w + y + x


def calculate_All_In_Cash(df_PL_BB_Build):
    # df_PL_BB_Build['Rates Fixed Coupon']=df_PL_BB_Build['Rates Fixed Coupon'].fillna(0)
    # df_PL_BB_Build['Rates Current LIBOR/Floor']=df_PL_BB_Build['Rates Current LIBOR/Floor'].fillna(0)
    # df_PL_BB_Build['Rates Floating Cash Spread']=df_PL_BB_Build['Rates Floating Cash Spread'].fillna(0)

    # df_PL_BB_Build['Rates All-In (Cash)']=df_PL_BB_Build['Rates Fixed Coupon']+df_PL_BB_Build['Rates Current LIBOR/Floor']+df_PL_BB_Build['Rates Floating Cash Spread']
    df_PL_BB_Build["Rates All-In (Cash)"] = df_PL_BB_Build.apply(
        lambda x: calculate_All_In_Cash_helper(
            x["Rates Fixed Coupon"],
            x["Rates Current LIBOR/Floor"],
            x["Rates Floating Cash Spread"],
        ),
        axis=1,
    )
    return df_PL_BB_Build


# calculation related to DH Adj_Contr_percent_issuer
def calculate_Adj_Contr_percent_issuer_helper(
    Issuer, df_PL_BB_Build_eligibleIssuer, denominator
):
    temp_df_sum = df_PL_BB_Build_eligibleIssuer[
        df_PL_BB_Build_eligibleIssuer["Issuer"] == Issuer
    ]["ONW Adjustments Adj. Elig. Amount"].sum()
    return temp_df_sum / denominator


def calculate_Adj_Contr_percent_issuer(df_PL_BB_Build, df_Obligors_Net_Capital):
    # Get the denominator value from 'PL BB Results'!$F$13
    df_PL_BB_Build_eligibleIssuer = df_PL_BB_Build[
        df_PL_BB_Build["Is Eligible Issuer"] == "Yes"
    ]
    denominator = df_Obligors_Net_Capital[
        df_Obligors_Net_Capital["Obligors' Net Capital"]
        == "Obligors' Net Capital ((a) + (b))"
    ]["values"].iloc[0]
    df_PL_BB_Build["ONW Adjustments Adj. Contr. % (issuer)"] = df_PL_BB_Build.apply(
        lambda x: calculate_Adj_Contr_percent_issuer_helper(
            x["Issuer"], df_PL_BB_Build_eligibleIssuer, denominator
        ),
        axis=1,
    )
    return df_PL_BB_Build


# U % of FMV Note: Tested but some values vary need to check after update borrowing base need to cash row in the file
def calculate_percent_of_FMV(df_PL_BB_Build, sum_of_FMV):
    df_PL_BB_Build["Investment % of FMV"] = (
        df_PL_BB_Build["Investment FMV"] / sum_of_FMV
    )
    return df_PL_BB_Build


# T Investment FMV/Cost
def calculate_FMV_Cost_helper(FMV, Cost):
    try:
        return FMV / Cost

    except:
        return 0


def calculate_FMV_Cost(df_PL_BB_Build):
    df_PL_BB_Build["Investment FMV/Cost"] = df_PL_BB_Build.apply(
        lambda x: calculate_FMV_Cost_helper(x["Investment FMV"], x["Investment Cost"]),
        axis=1,
    )
    return df_PL_BB_Build


# S Investment FMV/Par
def calculate_FMV_Par_helper(FMV, Par):
    try:
        return FMV / Par
    except:
        return 0


def calculate_FMV_Par(df_PL_BB_Build):
    df_PL_BB_Build["Investment FMV/Par"] = df_PL_BB_Build.apply(
        lambda x: calculate_FMV_Par_helper(x["Investment FMV"], x["Investment Par"]),
        axis=1,
    )
    return df_PL_BB_Build


# AS classification Eligible
def calculate_classification_Eligible_helper(w, x, y, z):
    if w == "No" or x == "No" or y == "No" or z == "No":
        return "Yes"
    else:
        return "No"


def calculate_classification_Eligible(df_PL_BB_Build):
    df_PL_BB_Build["Classification Eligible"] = df_PL_BB_Build.apply(
        lambda x: calculate_classification_Eligible_helper(
            x["Classifications Structured Finance Obligation"],
            x["Classifications Third Party Finance Company"],
            x["Classifications Affiliate Investment"],
            x["Classifications Defaulted / Restructured"],
        ),
        axis=1,
    )

    # df_PL_BB_Build['classification Eligible'] = 'No' if df_PL_BB_Build['Classifications Structured Finance Obligation']=='Yes' or df_PL_BB_Build['Classifications Third Party Finance Company']=='Yes' or df_PL_BB_Build['Classifications Affiliate Investment']=='Yes' or df_PL_BB_Build['Classifications Defaulted / Restructured']=='Yes' else 'Yes'
    return df_PL_BB_Build


# BR Final Eligible
def calculate_Final_Eligible_helper(w, x, y):
    if w == "No" or x == "No" or y == "No":
        return "No"
    else:
        return "Yes"


def calculate_Final_Eligible(df_PL_BB_Build):
    df_PL_BB_Build["Final Eligible"] = df_PL_BB_Build.apply(
        lambda x: calculate_Final_Eligible_helper(
            x["Classification Eligible"],
            x["Test 1 Pass"],
            x["Final Eligibility Override"],
        ),
        axis=1,
    )

    # df_PL_BB_Build['Final Eligible']='No' if df_PL_BB_Build['Classification Eligible']=='No' or df_PL_BB_Build['test_1_Pass']=='No' or df_PL_BB_Build['Final Eligibility Override']=='No' else 'Yes'
    return df_PL_BB_Build


# G Eligible
def calculate_Eligible(df_PL_BB_Build):
    """
    <b>Final Eligible</b> in PL BB Build table is derived from <b>Eligible</b> of PL BB Build table
    """
    df_PL_BB_Build["Eligible"] = df_PL_BB_Build["Final Eligible"]
    return df_PL_BB_Build


# CY Warehouse Second Lien Share
# giving the values 0 Have to crosscheck once again


def calculate_Warehouse_Second_Lien_Share_helper(CJ, AE, BB, inputD121):
    if math.isnan(CJ):
        return "N/A"
    else:
        if CJ > 0 and AE == "Warehouse First Lien" and BB > inputD121:
            return (BB - inputD121) / BB
        else:
            return 0


def calculate_Warehouse_Second_Lien_Share(df_PL_BB_Build, Input_D121):
    df_PL_BB_Build["Warehouse Second Lien Share"] = df_PL_BB_Build.apply(
        lambda x: calculate_Warehouse_Second_Lien_Share_helper(
            x["Concentration Adj. Elig. Amount"],
            x["Classifications Classification for BB"],
            x["Leverage PCOF IV Leverage"],
            Input_D121,
        ),
        axis=1,
    )
    return df_PL_BB_Build


# CZ  Warehouse Second Lien Rate
# Check values once again n/a or 0
def calculate_Warehouse_Second_Lien_Rate_helper(CY, AF, input_df):
    if CY == "N/A":
        return "n/a"
    else:
        if CY == 0:
            return 0
        else:
            if CY > 0:
                if AF == "Unquoted":
                    return input_df["Unquoted"].iloc[0]
                else:
                    if AF == "Quoted":
                        return input_df["Quoted"].iloc[0]
                    else:
                        return "n/a"


def calculate_Warehouse_Second_Lien_Rate(
    df_PL_BB_Build, df_Inputs_Portfolio_LeverageBorrowingBase
):
    df_PL_BB_Build["Warehouse Second Lien Rate"] = df_PL_BB_Build.apply(
        lambda x: calculate_Warehouse_Second_Lien_Rate_helper(
            x["Warehouse Second Lien Share"],
            x["Classifications Quoted / Unquoted"],
            df_Inputs_Portfolio_LeverageBorrowingBase,
        ),
        axis=1,
    )
    return df_PL_BB_Build


# CT First Lien Second Lien Share
def calculate_First_Lien_Second_Lien_Share_helper(CJ, AE, BB, inputD120):
    if CJ == "N/A":
        return "N/A"
    else:
        if CJ > 0 and AE == "First Lien" and float(BB) > float(inputD120):
            return (float(BB) - float(inputD120)) / float(BB)
        else:
            return 0


def calculate_First_Lien_Second_Lien_Share(df_PL_BB_Build, inputD120):
    df_PL_BB_Build["First Lien Second Lien Share"] = df_PL_BB_Build.apply(
        lambda x: calculate_First_Lien_Second_Lien_Share_helper(
            x["Concentration Adj. Elig. Amount"],
            x["Classifications Classification for BB"],
            x["Leverage PCOF IV Leverage"],
            inputD120,
        ),
        axis=1,
    )
    return df_PL_BB_Build


# CV  First Lien Adj. Advance Rate
def calculate_First_Lien_Adj_Advance_Rate_helper(AE, CJ, CR, CT, CU, CY, CZ):
    # print("CT * CU", CT, CU)
    if (CU == 'n/a'):
        return 'n/a'
    if AE == "Warehouse First Lien":
        return (CY * CZ) + ((1 - CY) * CR)
    else:
        if CT != 0:
            return (CT * CU) + ((1 - CT) * CR)
        else:
            return CR


def calculate_First_Lien_Adj_Advance_Rate(df_PL_BB_Build):
    df_PL_BB_Build["First Lien Adj. Advance Rate"] = df_PL_BB_Build.apply(
        lambda x: calculate_First_Lien_Adj_Advance_Rate_helper(
            x["Classifications Classification for BB"],
            x["Concentration Adj. Elig. Amount"],
            x["Revolver Adj. Advance Rate"],
            x["First Lien Second Lien Share"],
            x["First Lien Second Lien Rate"],
            x["Warehouse Second Lien Share"],
            x["Warehouse Second Lien Rate"],
        ),
        axis=1,
    )
    df_PL_BB_Build["First Lien Adj. Advance Rate"] = df_PL_BB_Build[
        "First Lien Adj. Advance Rate"
    ].fillna(0)
    return df_PL_BB_Build


# CW First Lien Contribution
def calculate_First_Lien_Contribution_helper(
    Concentration_Adj_Elig_Amount, First_Lien_Adj_Advance_Rate
):
    try:
        return Concentration_Adj_Elig_Amount * First_Lien_Adj_Advance_Rate
    except:
        return 0


def calculate_First_Lien_Contribution(df_PL_BB_Build):
    df_PL_BB_Build["First Lien Contribution"] = df_PL_BB_Build.apply(
        lambda x: calculate_First_Lien_Contribution_helper(
            x["Concentration Adj. Elig. Amount"], x["First Lien Adj. Advance Rate"]
        ),
        axis=1,
    )
    return df_PL_BB_Build


# CM Concentration Issuer % of ONC
def calculate_Concentration_Issuer_percent_of_ONC(df_PL_BB_Build):
    result = []
    for i in range(0, len(df_PL_BB_Build)):
        try:

            if (
                df_PL_BB_Build["Investment Name"][i]
                == df_PL_BB_Build["Investment Name"].shift(-1)[i]
            ):
                result.append(0)
            else:
                result.append(
                    df_PL_BB_Build[
                        df_PL_BB_Build["Investment Name"]
                        == df_PL_BB_Build["Investment Name"][i]
                    ]["Concentration % of ONC"].sum()
                )
        except Exception as e:
            raise Exception(e)
    df_PL_BB_Build["Concentration Issuer % of ONC"] = result
    return df_PL_BB_Build


# DC ONW Adjustments % of ONC > 10%
# Need to check once because in file given - and column getting 0
def calculate_ONW_Adjustments_percent_of_ONC_greater_10_percent(
    df_PL_BB_Build, input_matrices
):
    df_PL_BB_Build["ONW Adjustments % of ONC > 10%"] = df_PL_BB_Build.apply(
        lambda x: max(
            x["Concentration Issuer % of ONC"] - input_matrices["values"].iloc[0], 0
        ),
        axis=1,
    )
    # df_PL_BB_Build['ONW Adjustments % of ONC > 10%']=max(df_PL_BB_Build['Concentration Issuer % of ONC']-input_matrices['values'].iloc[0],0)
    return df_PL_BB_Build


# DB ONW Adjustments % of ONC > 7.5%
def calculate_ONW_Adjustments_percent_of_ONC_greater_7_point_5_percent_helper(
    Concentration_Issuer_percent_of_ONC, InputD
):
    inputD128 = InputD["values"].iloc[0]
    inputD129 = InputD["values"].iloc[1]
    if max(0, Concentration_Issuer_percent_of_ONC - inputD128) > 0:
        return min(
            inputD129 - inputD128,
            max(0, Concentration_Issuer_percent_of_ONC - inputD128),
        )
    else:
        return 0


def calculate_ONW_Adjustments_percent_of_ONC_greater_7_point_5_percent(
    df_PL_BB_Build, InputD
):
    df_PL_BB_Build["ONW Adjustments % of ONC > 7.5%"] = df_PL_BB_Build.apply(
        lambda x: calculate_ONW_Adjustments_percent_of_ONC_greater_7_point_5_percent_helper(
            x["Concentration Issuer % of ONC"], InputD
        ),
        axis=1,
    )
    return df_PL_BB_Build


# DE ONW Adjustments > 10% ONC Share
def calculate_ONW_Adjustments_greater_10_percent_ONC_Share(
    df_PL_BB_Build, df_Obligors_Net_Capital
):
    PL_BB_Results_factor = df_Obligors_Net_Capital[
        df_Obligors_Net_Capital["Obligors' Net Capital"]
        == "Obligors' Net Capital ((a) + (b))"
    ]["values"].iloc[0]

    # df_PL_BB_Build['ONW Adjustments > 10% ONC Share']=df_PL_BB_Build.apply(lambda x :(x['ONW Adjustments % of ONC > 10%']*PL_BB_Results_factor)/1000000)

    df_PL_BB_Build["ONW Adjustments > 10% ONC Share"] = (
        df_PL_BB_Build["ONW Adjustments % of ONC > 10%"]
        * PL_BB_Results_factor
        / 1000000
    )
    return df_PL_BB_Build


# DD ONW Adjustments > 7.5% ONC Share
def calculate_ONW_Adjustments_greater_7_point_5_percent_ONC_Share(
    df_PL_BB_Build, df_Obligors_Net_Capital
):
    PL_BB_Results_factor = df_Obligors_Net_Capital[
        df_Obligors_Net_Capital["Obligors' Net Capital"]
        == "Obligors' Net Capital ((a) + (b))"
    ]["values"].iloc[0]
    df_PL_BB_Build["ONW Adjustments > 7.5% ONC Share"] = (
        df_PL_BB_Build["ONW Adjustments % of ONC > 7.5%"]
        * PL_BB_Results_factor
        / 1000000
    )
    return df_PL_BB_Build


# DF ONW Adjustments ONC haircut for Elig. Amount
def calculate_ONW_Adjustments_ONC_haircut_for_Elig_Amount(
    df_PL_BB_Build, df_Inputs_Other_Metrics
):
    InputD130 = df_Inputs_Other_Metrics[
        df_Inputs_Other_Metrics["Other Metrics"] == "Threshold 1 Advance Rate"
    ]["values"].iloc[0]
    InputD131 = df_Inputs_Other_Metrics[
        df_Inputs_Other_Metrics["Other Metrics"] == "Threshold 2 Advance Rate"
    ]["values"].iloc[0]
    df_PL_BB_Build["ONW Adjustments ONC haircut for Elig. Amount"] = (
        df_PL_BB_Build["ONW Adjustments > 7.5% ONC Share"] * (1 - InputD130)
    ) + (df_PL_BB_Build["ONW Adjustments > 10% ONC Share"] * (1 - InputD131))
    return df_PL_BB_Build


# DG  ONW Adjustments Adj. Elig. Amount
def calculate_ONW_Adjustments_Adj_Elig_Amount(df_PL_BB_Build):
    df_PL_BB_Build["ONW Adjustments Adj. Elig. Amount"] = (
        df_PL_BB_Build["Concentration Adj. Elig. Amount"]
        - df_PL_BB_Build["ONW Adjustments ONC haircut for Elig. Amount"]
    )
    return df_PL_BB_Build


# DI ONW Adjustments Concentration BB Adj. Contribution
def calculate_ONW_Adjustments_Concentration_BB_Adj_Contribution_helper(
    ONW_Adjustments_greater_7_point_5_percent_ONC_Share,
    First_Lien_Adj_Advance_Rate,
    ONW_Adjustments_greater_10_percent_ONC_Share,
    df_Inputs_Other_Metrics,
):
    try:
        InputD130 = df_Inputs_Other_Metrics[
            df_Inputs_Other_Metrics["Other Metrics"] == "Threshold 1 Advance Rate"
        ]["values"].iloc[0]
        InputD131 = df_Inputs_Other_Metrics[
            df_Inputs_Other_Metrics["Other Metrics"] == "Threshold 2 Advance Rate"
        ]["values"].iloc[0]
        return (
            ONW_Adjustments_greater_7_point_5_percent_ONC_Share
            * InputD130
            * First_Lien_Adj_Advance_Rate
        ) + (ONW_Adjustments_greater_10_percent_ONC_Share * InputD131)
    except:
        return 0


def calculate_ONW_Adjustments_Concentration_BB_Adj_Contribution(
    df_PL_BB_Build, df_Inputs_Other_Metrics
):
    df_PL_BB_Build["ONW Adjustments Concentration BB Adj. Contribution"] = (
        df_PL_BB_Build.apply(
            lambda x: calculate_ONW_Adjustments_Concentration_BB_Adj_Contribution_helper(
                x["ONW Adjustments > 7.5% ONC Share"],
                x["First Lien Adj. Advance Rate"],
                x["ONW Adjustments > 10% ONC Share"],
                df_Inputs_Other_Metrics,
            ),
            axis=1,
        )
    )
    return df_PL_BB_Build


# DL Borrowing Base Adj. Contribution
def calculate_Borrowing_Base_Adj_Contribution_helper(
    Concentration_Adj_Elig_Amount,
    ONW_Adjustments_greater_7_point_5_percent_ONC_Share,
    ONW_Adjustments_greater_10_percent_ONC_Share,
    First_Lien_Adj_Advance_Rate,
    ONW_Adjustments_Concentration_BB_Adj_Contribution,
):
    try:
        if First_Lien_Adj_Advance_Rate == 'n/a':
            return None
        return (
            (
                Concentration_Adj_Elig_Amount
                - ONW_Adjustments_greater_7_point_5_percent_ONC_Share
                - ONW_Adjustments_greater_10_percent_ONC_Share
            )
            * First_Lien_Adj_Advance_Rate
        ) + ONW_Adjustments_Concentration_BB_Adj_Contribution
    except Exception as e:
        raise Exception(e)


def calculate_Borrowing_Base_Adj_Contribution(df_PL_BB_Build):
    df_PL_BB_Build["Borrowing Base Adj. Contribution"] = df_PL_BB_Build.apply(
        lambda x: calculate_Borrowing_Base_Adj_Contribution_helper(
            x["Concentration Adj. Elig. Amount"],
            x["ONW Adjustments > 7.5% ONC Share"],
            x["ONW Adjustments > 10% ONC Share"],
            x["First Lien Adj. Advance Rate"],
            x["ONW Adjustments Concentration BB Adj. Contribution"],
        ),
        axis=1,
    )
    pd.set_option("display.max_rows", None)

    return df_PL_BB_Build


# DK Borrowing Base ONW Adjustment
def calculate_Borrowing_Base_ONW_Adjustment(df_PL_BB_Build):
    df_PL_BB_Build["Borrowing Base ONW Adjustment"] = (
        df_PL_BB_Build["Borrowing Base Adj. Contribution"]
        - df_PL_BB_Build["First Lien Contribution"]
    )

    return df_PL_BB_Build


# DP Borrowing Base
def calculate_Borrowing_Base_helper(
    Borrowing_Base_Adj_Contribution,
    Borrowing_Base_Other_Adjustment,
    Borrowing_Base_Industry_Concentration,
):
    required_cols = [Borrowing_Base_Adj_Contribution, Borrowing_Base_Other_Adjustment, Borrowing_Base_Industry_Concentration]
    try:
        a = np.array(
            [np.nan if x is None else x for x in required_cols]
        )
        return a[~np.isnan(a)].sum()
        # return Borrowing_Base_Adj_Contribution+Borrowing_Base_Other_Adjustment+Borrowing_Base_Industry_Concentration
    except:
        return 0.0


def calculate_Borrowing_Base(df_PL_BB_Build):
    """<b>Borrowing Base</b> in PL BB Build table is derived from values of <b>Borrowing Base Adj. Contribution</b>,
    <b>Borrowing Base Other Adjustment</b> and <b>Borrowing Base Industry Concentration</b> of PL BB Build Table

    <b>Borrowing Base</b>=IFERROR(<b>Borrowing Base Adj. Contribution</b>+<b>Borrowing Base Other Adjustment</b>+<b>Borrowing Base Industry Concentration</b>,"n/a")
    """
    df_PL_BB_Build["Borrowing Base"] = df_PL_BB_Build.apply(
        lambda x: calculate_Borrowing_Base_helper(
            x["Borrowing Base Adj. Contribution"],
            x["Borrowing Base Other Adjustment"],
            x["Borrowing Base Industry Concentration"],
        ),
        axis=1,
    )
    return df_PL_BB_Build


# DQ Borrowing Base % of BB
# Needs to be check once again after corrected base data file
def calculate_Borrowing_Base_percent_of_BB_helper(borrowing_base, sum_borrowing_base):
    try:
        return borrowing_base / sum_borrowing_base
    except:
        return ""


def calculate_Borrowing_Base_percent_of_BB(df_PL_BB_Build):
    """
    <b>Borrowing Base % of BB</b> is derived from PL BB Build table using sum of the <b>Borrowing Base</b> for Eligible Issuers from PL BB Build table.

    <b>Borrowing Base % of BB</b>=  <b>Borrowing Base</b>/sum(<b>Borrowing Base</b>)
    """
    sum_borrowing_base = df_PL_BB_Build[df_PL_BB_Build["Is Eligible Issuer"] == "Yes"][
        "Borrowing Base"
    ].sum()
    df_PL_BB_Build["Borrowing Base % of BB"] = df_PL_BB_Build.apply(
        lambda x: calculate_Borrowing_Base_percent_of_BB_helper(
            x["Borrowing Base"], sum_borrowing_base
        ),
        axis=1,
    )
    return df_PL_BB_Build


# C Eligible Issuers


def calculate_Eligible_Issuers(df_PL_BB_Build):
    """
    <b>Eligible Issuers</b> in PL BB Build table is derived from the values <b>Eligible</b>, <b>Issuer</b> and preceding values of <b>Eligible Issuers</b> of PL BB Build table

    <b>Eligible Issuers</b>[i] = IF(OR(<b>Issuer</b>[i]=<b>Issuer</b>[i-1],<b>Eligible</b>[i]="No",<b>Issuer</b>[i]=0),Eligible Issuers<b>[i-1],Eligible Issuers</b>[i]+1)
    """

    l = len(df_PL_BB_Build[df_PL_BB_Build["Is Eligible Issuer"] == "Yes"])

    df_PL_BB_Build["Eligible Issuers"] = 0  # Initialize the new column with zeros

    df_PL_BB_Build.loc[0, "Eligible Issuers"] = 1  # Set the value of the first row to 1

    for i in range(1, l - 1):
        condition = (
            (df_PL_BB_Build.at[i, "Issuer"] == df_PL_BB_Build.at[i - 1, "Issuer"])
            or (df_PL_BB_Build.at[i, "Eligible"] == "No")
            or (df_PL_BB_Build.at[i, "Issuer"] == 0)
        )

        if condition:
            df_PL_BB_Build.at[i, "Eligible Issuers"] = df_PL_BB_Build.at[i - 1, "Eligible Issuers"]
        else:
            df_PL_BB_Build.at[i, "Eligible Issuers"] = df_PL_BB_Build.at[i - 1, "Eligible Issuers"] + 1


    return df_PL_BB_Build
