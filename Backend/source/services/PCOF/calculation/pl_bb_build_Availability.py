# D18=IF('[1]PL BB Results'!G18>=8,"Yes","No")
def Portfolio_greater_than_8_Eligible_Issuers(avail, df_PL_BB_Build):
    """<b>Portfolio > 8 Eligible Issuers?</b> in Availability table is derived from the value of <b>Actual</b> where <b>Concentration Tests</b> is  "Min. Eligible Issuers" as provided in PL BB Results
    <br>
    <br>
    <b>Portfolio > 8 Eligible Issuers?</b> = IF('[PL BB Results]Min. Eligible Issuers<b>Actual</b>>=8,"Yes","No")
    <br>
    """
    # match_index = results[
    #     results["Concentration Tests"] == "Min. Eligible Issuers (#)"
    # ].index[0]
    # function_which_return_G18_from_PLBBResult = results["Actual"].iloc[match_index]
    function_which_return_G18_from_PLBBResult = df_PL_BB_Build["Eligible Issuers"].sum()
    if function_which_return_G18_from_PLBBResult >= 8:
        new_dict = {"A": "Portfolio > 8 Eligible Issuers?", "B": "Yes"}
        avail.loc[len(avail)] = new_dict
    else:
        new_dict = {"A": "Portfolio > 8 Eligible Issuers?", "B": "No"}
        avail.loc[len(avail)] = new_dict
    return avail


# D19=(('PL BB Build'!CJ35)-SUMIF('PL BB Build'!$AE$7:$AE$34,"Warehouse First Lien",'PL BB Build'!$CJ$7:$CJ$34))
def Portfolio_FMV_of_Portfolio(avail, pl_bb_build, results):
    """
    <b>FMV of Portfolio</b> in Availability table is derived from values corresponding to terms
    <b>Is Eligible Issuer</b>, <b>Concentration Adj. Elig. Amount</b> and <b>Classifications Classification for BB</b> from PL BB Build table
    <br>
    <br>
    <b>FMV of Portfolio</b> = (SUM(<b>Concentration Adj. Elig. Amount</b>))-SUMIF(<b>Classifications Classification for BB</b>,"Warehouse First Lien",<b>Concentration Adj. Elig. Amount</b>))
    """

    value = pl_bb_build[pl_bb_build["Is Eligible Issuer"] == "Yes"][
        "Concentration Adj. Elig. Amount"
    ].sum()
    classification_of_bb = pl_bb_build[
        pl_bb_build["Classifications Classification for BB"] == "Warehouse First Lien"
    ]["Concentration Adj. Elig. Amount"].sum()

    new_dict = {"A": "FMV of Portfolio", "B": value - classification_of_bb}
    avail.loc[len(avail)] = new_dict
    return avail


# D21=IF(D18="Yes",'[1]PL BB Build'!DP35,0)
def Portfolio_Portfolio_Leverage_Borrowing_Base_calculated(avail, pl_bb_build, results):
    """<b>Portfolio Leverage Borrowing Base (as calculated)</b> in Availability table is derived from values corresponding to terms
    <b>Is Eligible Issuer</b> and <b>Borrowing Base</b> from PL BB Build table and <b>Portfolio > 8 Eligible Issuers</b> from Availability table
       <br>
       <br>
        <b>Portfolio Leverage Borrowing Base (as calculated)</b> = IF(Portfolio > 8 Eligible Issuers="Yes",<b>Borrowing Base</b>,0)
    """
    match_index = avail[avail["A"] == "Portfolio > 8 Eligible Issuers?"].index[0]
    Portfolio_greater_than_8_Eligible_Issuer_value = avail["B"].iloc[match_index]
    if Portfolio_greater_than_8_Eligible_Issuer_value == "Yes":

        value = pl_bb_build[pl_bb_build["Is Eligible Issuer"] == "Yes"][
            "Borrowing Base"
        ].sum()

        new_dict = {
            "A": "Portfolio Leverage Borrowing Base (as calculated)",
            "B": value,
        }
        avail.loc[len(avail)] = new_dict
    else:
        new_dict = {"A": "Portfolio Leverage Borrowing Base (as calculated)", "B": 0}
        avail.loc[len(avail)] = new_dict
    return avail


# D20=IFERROR(D21/D19,"N/A")
def Portfolio_Effective_Advance_Rate_on_FMV_of_Portfolio(avail, pl_bb_build, results):
    """<b>Effective Advance Rate on FMV of Portfolio</b> in Availability table is derived from two values corresponding to terms <b>FMV of Portfolio</b> and <b>Portfolio Leverage Borrowing Base (as calculated)</b> from Availability table
    <br>
    <br>
    <b>Effective Advance Rate on FMV of Portfolio</b> = <b>Portfolio Leverage Borrowing Base (as calculated)</b>/<b>FMV of Portfolio</b>
    """

    match_index_fmv = avail[avail["A"] == "FMV of Portfolio"].index[0]
    FMV_of_Portfolio = avail["B"].iloc[match_index_fmv]
    match_index_lbb = avail[
        avail["A"] == "Portfolio Leverage Borrowing Base (as calculated)"
    ].index[0]
    Portfolio_Leverage_Borrowing_Base = avail["B"].iloc[match_index_lbb]

    try:
        value = Portfolio_Leverage_Borrowing_Base / FMV_of_Portfolio
        new_dict = {"A": "Effective Advance Rate on FMV of Portfolio", "B": value}
        avail.loc[len(avail)] = new_dict

    except:
        new_dict = {"A": "Effective Advance Rate on FMV of Portfolio", "B": 0}
        avail.loc[len(avail)] = new_dict
    return avail


# D22=IF('PL BB Results'!$G$28>Inputs!$D$11,Inputs!$D$11,Inputs!$D$12)
# inputs contain pricing table import that
def Portfolio_Maximum_Advance_Rate_on_PL_Borrowing_Base(df_pl_bb_build, pricing, avail):
    """<b>Maximum Advance Rate on PL Borrowing Base</b> in Availability table is derived from the value of <b>Actual</b> where <b>Concentration Tests</b>
     is <b>Min. Cash, First Lien, and Cov-Lite</b> in Results table, value of <b>Percent</b> where <b>Pricing</b> is <b>Lower Effective A/R</b> and
     <b>Min. First Lien / Last Out Contribution to PL BB for 65% Effective A/R</b> as provided in Results table
    <br>
    <br>
    <b>Maximum Advance Rate on PL Borrowing Base</b> = IF(<b>Min. Cash, First Lien, and Cov-Lite</b>><b>Min. First Lien / Last Out Contribution to PL BB for 65% Effective A/R</b>,<b>Min. First Lien / Last Out Contribution to PL BB for 65% Effective A/R</b>,<b>Lower Effective A/R</b>)
    """
    # match_index_FC = results[
    #     results["Concentration Tests"] == "Min. Cash, First Lien, and Cov-Lite"
    # ].index[0]
    # function_which_return_G28_from_PLBBResult = results["Actual"].iloc[match_index_FC]

    required_pl_bb_build = df_pl_bb_build[
        ["Classification Adj. Adjusted Type", "Borrowing Base"]
    ]
    required_pl_bb_build = required_pl_bb_build[
        required_pl_bb_build["Classification Adj. Adjusted Type"].isin(
            ["Cash", "First Lien", "Cov-Lite", "Warehouse First Lien"]
        )
    ]
    sum_of_bb = required_pl_bb_build["Borrowing Base"].sum()
    required_pl_bb_build["percentage of BB"] = (
        required_pl_bb_build["Borrowing Base"] / sum_of_bb
    )
    function_which_return_G28_from_PLBBResult = required_pl_bb_build[
        "percentage of BB"
    ].sum()

    match_index_mf = pricing[
        pricing["Pricing"]
        == r"Min. First Lien / Last Out Contribution to PL BB for 65% Effective A/R"
    ].index[0]
    contribution_for_65_effective = pricing["percent"].iloc[match_index_mf]
    match_index_d12 = pricing[pricing["Pricing"] == "Lower Effective A/R"].index[0]
    lower_effective_ar = pricing["percent"].iloc[match_index_d12]
    if function_which_return_G28_from_PLBBResult > contribution_for_65_effective:
        new_dict = {
            "A": "Maximum Advance Rate on PL Borrowing Base",
            "B": contribution_for_65_effective,
        }
        avail.loc[len(avail)] = new_dict

    else:
        new_dict = {
            "A": "Maximum Advance Rate on PL Borrowing Base",
            "B": lower_effective_ar,
        }
        avail.loc[len(avail)] = new_dict
    return avail


# D23==MIN(D21,((D19*D22)+SUMIF('PL BB Build'!$AE$7:$AE$34,"Warehouse First Lien",'PL BB Build'!$DP$7:$DP$34)))
def Portfolio_Portfolio_Leverage_Borrowing_Base(avail, results, pl_bb_build, pricing):
    """<b>Portfolio Leverage Borrowing Base</b> in Availability table is derived from three values corresponding to terms
    <b>FMV of Portfolio</b>, <b>Portfolio Leverage Borrowing Base (as calculated)</b> and <b>Maximum Advance Rate on PL Borrowing Base</b>
     from Availability table and two values corresponding to terms <b>Classifications Classification for BB</b> and <b>Borrowing Base</b>
     from PL BB Build table
    <br>
    <br>
    <b>Portfolio Leverage Borrowing Base</b> = MIN(<b>Portfolio Leverage Borrowing Base (as calculated)</b>,((<b>FMV of Portfolio</b>*<b>Maximum Advance Rate on PL Borrowing Base</b>)+SUMIF(<b>Classifications Classification for BB</b>,"Warehouse First Lien",<b>Borrowing Base</b>)))
    """

    # D19
    match_index_fmv = avail[avail["A"] == "FMV of Portfolio"].index[0]
    FMV_of_Portfolio = avail["B"].iloc[match_index_fmv]
    # D21
    match_index_lbb = avail[
        avail["A"] == "Portfolio Leverage Borrowing Base (as calculated)"
    ].index[0]
    Portfolio_Leverage_Borrowing_Base = avail["B"].iloc[match_index_lbb]
    # D22
    match_index_rbb = avail[
        avail["A"] == "Maximum Advance Rate on PL Borrowing Base"
    ].index[0]
    max_adv_rate = avail["B"].iloc[match_index_rbb]
    d19_mul_d22 = FMV_of_Portfolio * max_adv_rate
    sumif = pl_bb_build[
        pl_bb_build["Classifications Classification for BB"] == "Warehouse First Lien"
    ]["Borrowing Base"].sum()
    check = d19_mul_d22 + sumif
    new_dict = {
        "A": "Portfolio Leverage Borrowing Base",
        "B": min([Portfolio_Leverage_Borrowing_Base, check]),
    }
    avail.loc[len(avail)] = new_dict
    return avail

    # Months since Revolving Closing Date


def calculate_Months_since_Revolving_Closing_Date(avail):
    """<b>Months since Revolving closing Date</b> in Availability table is derived from two values corresponding to terms <b>Revolving Closing Date</b> and <b>Date of determination</b> from Availability table
    <br>
    <br>
    <b>Months since Revolving closing Date</b> = DATEDIF(<b>Revolving Closing Date</b>,<b>Date of determination</b>,"m")
    """

    start_idx = avail[avail["A"] == "Revolving Closing Date"].index[0]
    start = avail["B"].iloc[start_idx]

    end_idx = avail[avail["A"] == "Date of determination:"].index[0]
    end = avail["B"].iloc[end_idx]

    diff_days = (end - start).days
    diff_mon = (end.year - start.year) * 12 + (end.month - start.month)
    if end.day < start.day:
        diff_mon -= 1
    diff_year = end.year - start.year

    new_row = {"A": "Months since Revolving closing Date", "B": diff_mon}
    avail.loc[len(avail)] = new_row

    return avail


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# Q69 Calulculation
# =Q38+Q66+Q68
def calculate_Total_All_Investors_Borrowing_Base(subscription):
    """<b>Total Borrowing Base-All Investors</b> in Availability table is derived from value of <b>Total
    Eligible Committments Borrowing Base</b> from Subscription Table
    """
    sum1 = calculate_total_eligible_committments_Borrowing_Base(subscription)
    sum2 = 0  # take from suscription sheet/
    sum3 = 0  # take from suscription sheet

    return sum1 + sum2 + sum3


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# Q38 Calculation
# =Q20+Q36
def calculate_total_eligible_committments_Borrowing_Base(subscription):
    """<b>Total Eligible Committments Borrowing Base</b> is derived from total sum of Borrowing Base values where
    <b>Designation</b> is <b>Institutional Investors</b> and <b>High Net Worth Investors</b> in table named Subscription
    """
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
    """<b>Subscription Borrowing Base</b> in Availability table is derived from two values corresponding to terms <b>Commitment Period (3 years from Final Closing Date, as defined in LPA)</b> and <b>Total All Investors - Borrowing Base</b> from Availability and Sbscription table respectively
    <br>
    <br>
    <b>Subscription Borrowing Base</b> = IF(<b>Commitment Period (3 years from Final Closing Date, as defined in LPA)</b>="Yes",<b>Total All Investors Borrowing Base</b>,0)
    <br>

    """

    subscript = calculate_Total_All_Investors_Borrowing_Base(subscription)

    idx = avail[
        avail["A"]
        == "Commitment Period (3 years from Final Closing Date, as defined in LPA)"
    ].index[0]
    commit_period = avail["B"].iloc[idx]

    if commit_period == "Yes":
        val = subscript

    else:
        val = 0

    new_row = {"A": "Subscription Borrowing Base", "B": val}
    avail.loc[len(avail)] = new_row
    return avail


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# A
# D15 = D14/13
def calculate_Effective_Advance_Rate_on_Total_Uncalled_Capital(avail, subscription):
    """<b>Effective Advance Rate on Total Uncalled Capital</b> in Availability table is derived from two values corresponding to terms <b>Subscription Borrowing Base</b> and <b>Uncalled Capital Commitments</b> from Availability table
    <br>
    <br>
    <b>Effective Advance Rate on Total Uncalled Capital</b> = <b>Subscription Borrowing Base<b>/<b>Uncalled Capital Commitments</b>
    """

    try:
        # avail =  calculate_subscription_Borrowing_Base(avail, subscription)
        idx = avail[avail["A"] == "Subscription Borrowing Base"].index[0]
        num = avail["B"].iloc[idx]

        idx_den = avail[avail["A"] == "Uncalled Capital Commitments"].index[0]
        den = avail["B"].iloc[idx_den]

        val = num / den
    except:
        val = "N/A"

    new_row = {"A": "Effective Advance Rate on Total Uncalled Capital", "B": val}
    avail.loc[len(avail)] = new_row

    return avail


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# Avaialibility
# D29 = D14+D23
def calculate_A_Total_Borrowing_Base(avail, subscription):
    """<b>Total Borrowing Base</b> in Availability table is derived from two values corresponding to terms <b>Subscription Borrowing Base</b> and <b>Portfolio Leverage Borrowing Base</b> from Availability table
    <br>
    <b>Total Borrowing Base</b> = <b>Subscription Borrowing Base</b> - <b>Portfolio Leverage Borrowing Base</b>
    """

    sub_idx = avail[avail["A"] == "Subscription Borrowing Base"].index[0]
    subscript = avail["B"].iloc[sub_idx]

    por_lev_idx = avail[avail["A"] == "Portfolio Leverage Borrowing Base"].index[0]
    por_lev = avail["B"].iloc[por_lev_idx]
    # por_lev = 26014023
    val = subscript + por_lev

    new_row = {"A": "Total Borrowing Base", "B": val}
    avail.loc[len(avail)] = new_row

    return avail


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# D34 = i32
def calculate_Outstandings(avail):
    """<b>Outstandings</b> in Availability table is derived from the value corresponding to term <b>Loans (USD)</b> from Availability table
    <br>
    <br>
     <b>Outstandings</b> = <b>Loans (USD)</b>
    """

    idx = avail[avail["A"] == "Loans (USD)"].index[0]
    val = avail["B"].iloc[idx]

    new_row = {"A": "Outstandings", "B": val}
    avail.loc[len(avail)] = new_row

    return avail


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# #Avaialability
# #D33 = min(D29,D31)
# def calculate_lesser_of_a_b(avail,subscription):
#     # avail = calculate_A_Total_Borrowing_Base(avail,subscription)
#     """<b>Lesser of (a) and (b)<b> in Availability table is derived from two values corresponding to terms <b>Total Borrowing Base<b> and <b>Facility Size<b> from Availability table

#         <b>Lesser of (a) and (b)<b> = min(<b>Total Borrowing Base<b>,<b>Facility Size<b>)

#     <b>Gross BB Utilization<b> in Availability table is derived from two values corresponding to terms <b>Total Borrowing Base<b> and <b>Outstandings<b> from Availability table

#         <b>Gross BB Utilization<b> = <b>Outstandings<b>/<b>Total Borrowing Base<b>

#     <b>Facility Utilization<b> in Availability table is derived from two values corresponding to terms <b>Outstandings<b> and <b>Facility Size<b> from Availability table

#         <b>Facility Utilization<b> = <b>Outstandings<b>/<b>Total Borrowing Base<b>
#     """


#     idx_tot = avail[avail['A']=='Total Borrowing Base'].index[0]
#     total = avail['B'].iloc[idx_tot]

#     idx_fac = avail[avail['A']=='(b) Facility Size'].index[0]
#     fac_size = avail['B'].iloc[idx_fac]

#     idx_out = avail[avail['A']=='Outstandings'].index[0]
#     out_stand = avail['B'].iloc[idx_out]

#     val1 = min(total,fac_size)
#     new_row1 = {'A': 'Lesser of (a) and (b)', 'B':val1}
#     avail.loc[len(avail)]=new_row1

#     val2 = out_stand/total
#     new_row2 = {'A': 'Gross BB Utilization', 'B':val2}
#     avail.loc[len(avail)]=new_row2

#     val3 = out_stand/fac_size
#     new_row3 = {'A': 'Facility Utilization', 'B':val3}
#     avail.loc[len(avail)]=new_row3


#     return avail
# -------------------------------------------------------------------------------------------------------------------------------------
# Avaialability
# D33 = min(D29,D31)
def calculate_lesser_of_a_b(avail, subscription):
    # avail = calculate_A_Total_Borrowing_Base(avail,subscription)
    """<b>Lesser of (a) and (b)</b> in Availability table is derived from two values corresponding to terms <b>Total Borrowing Base</b> and <b>Facility Size</b> from Availability table
    <br>
    <br>
    <b>Lesser of (a) and (b)</b> = min(<b>Total Borrowing Base</b>,<b>Facility Size</b>)
    """

    idx_tot = avail[avail["A"] == "Total Borrowing Base"].index[0]
    total = avail["B"].iloc[idx_tot]

    idx_fac = avail[avail["A"] == "(b) Facility Size"].index[0]
    fac_size = avail["B"].iloc[idx_fac]

    val1 = min(total, fac_size)
    new_row1 = {"A": "Lesser of (a) and (b)", "B": val1}
    avail.loc[len(avail)] = new_row1

    return avail


# -------------------------------------------------------------------------------------------------------------------------------------
# Avaialability
# D38 = D34/D29
def calculate_Gross_BB_Utilization(avail, subscription):
    """<b>Gross BB Utilization</b> in Availability table is derived from two values corresponding to terms <b>Total Borrowing Base</b> and <b>Outstandings</b> from Availability table
    <br>
    <br>
    <b>Gross BB Utilization</b> = <b>Outstandings</b>/<b>Total Borrowing Base</b>"""

    idx_tot = avail[avail["A"] == "Total Borrowing Base"].index[0]
    total = avail["B"].iloc[idx_tot]

    idx_out = avail[avail["A"] == "Outstandings"].index[0]
    out_stand = avail["B"].iloc[idx_out]

    val2 = out_stand / total
    new_row2 = {"A": "Gross BB Utilization", "B": val2}
    avail.loc[len(avail)] = new_row2

    return avail


# -------------------------------------------------------------------------------------------------------------------------------------
# Avaialability
# D39 = D34/D31
def calculate_Facility_Utilization(avail, subscription):
    """<b>Facility Utilization</b> in Availability table is derived from two values corresponding to terms <b>Outstandings</b> and <b>Facility Size</b> from Availability table
    <br>
    <br>
    <b>Facility Utilization</b> = <b>Outstandings</b>/<b>Total Borrowing Base</b>
    """
    idx_fac = avail[avail["A"] == "(b) Facility Size"].index[0]
    fac_size = avail["B"].iloc[idx_fac]

    idx_out = avail[avail["A"] == "Outstandings"].index[0]
    out_stand = avail["B"].iloc[idx_out]

    val3 = out_stand / fac_size
    new_row3 = {"A": "Facility Utilization", "B": val3}
    avail.loc[len(avail)] = new_row3

    return avail


# -------------------------------------------------------------------------------------------------------------------------------------
# d35 =D33-D34
def calculate_A_Net_Debt_A(avail, subscription):
    """<b>Net Debt Availbility</b> in Availability table is derived from two values corresponding to terms <b>Lesser of (a) and (b)</b> and <b>Outstandings</b> from Availability table
    <br>
    <br>
    <b>Net Debt Availbility</b> = <b>Lesser of (a) and (b)</b> - <b>Outstandings</b>
    """

    idx1 = avail[avail["A"] == "Lesser of (a) and (b)"].index[0]
    val1 = avail["B"].iloc[idx1]

    idx2 = avail[avail["A"] == "Outstandings"].index[0]
    val2 = avail["B"].iloc[idx2]

    val = val1 - val2

    new_row = {"A": "Net Debt Availbility", "B": val}
    avail.loc[len(avail)] = new_row

    return avail


def calculate_Uncalled_Capital_Commitments_availability(avail, subscription_df):
    """<b>Uncalled Capital Commitments</b> in Availability table is derived from total sum of values corresponding to term <b>Uncalled Capital</b> from Subscription table
    <br>
    <br>
    <b>Uncalled Capital Commitments</b> = SUM(Uncalled Capital)
    """
    total_allInvestors = subscription_df["Uncalled Capital"].sum()
    new_dict = {"A": "Uncalled Capital Commitments", "B": total_allInvestors}
    avail.loc[len(avail)] = new_dict
    return avail
