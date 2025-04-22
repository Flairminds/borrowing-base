import pandas as pd
import numpy as np

class RevolverValidationCheckAndBorrower :
    def __init__(self, calculator_info):
        self.calculator_info = calculator_info

    def rcf_exposure_priority_pari_abl(self):
        # =SUM(IFERROR(SUMIFS($K$11:$K$90,$I$11:$I$90,"Cash Flow Priority Revolver",$G$11:$G$90,G11)/COUNTIFS($G$11:$G$90,G11,$I$11:$I$90,"Cash Flow Priority Revolver"),0),IFERROR(SUMIFS($K$11:$K$90,$I$11:$I$90,"Cash Flow Pari Passu Revolver",$G$11:$G$90,G11)/COUNTIFS($G$11:$G$90,G11,$I$11:$I$90,"Cash Flow Pari Passu Revolver"),0),IFERROR(SUMIFS($K$11:$K$90,$I$11:$I$90,"ABL - Working Capital Facility",$G$11:$G$90,G11)/COUNTIFS($G$11:$G$90,G11,$I$11:$I$90,"ABL - Working Capital Facility"),0))

        def rcf_exposure_priority_pari_abl_helper(row):
            g_value = row['Borrower']
    
            def safe_avg(facility_type):
                filtered = portfolio_df[(portfolio_df['Borrower'] == g_value) & (portfolio_df['RCF Exposure Type'] == facility_type)]
                if filtered.empty:
                    return 0
                return filtered['RCF Outstanding Amount'].sum() / len(filtered)
            return safe_avg("Cash Flow Priority Revolver") + safe_avg("Cash Flow Pari Passu Revolver") + safe_avg("ABL - Working Capital Facility")
            

        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["RCF Exposure (Priority,Pari,ABL)"] = portfolio_df.apply(rcf_exposure_priority_pari_abl_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def rfc_exposure_priority_abl(self):
        # =SUM(IFERROR(SUMIFS($K$11:$K$90,$I$11:$I$90,"Cash Flow Priority Revolver",$G$11:$G$90,G11)/COUNTIFS($G$11:$G$90,G11,$I$11:$I$90,"Cash Flow Priority Revolver"),0),IFERROR(SUMIFS($K$11:$K$90,$I$11:$I$90,"ABL - Working Capital Facility",$G$11:$G$90,G11)/COUNTIFS($G$11:$G$90,G11,$I$11:$I$90,"ABL - Working Capital Facility"),0))
        def rfc_exposure_priority_abl_helper(row):
            g_val = row['Borrower']
    
            def safe_avg(facility_type):
                filtered = portfolio_df[(portfolio_df['Borrower'] == g_val) & (portfolio_df['RCF Exposure Type'] == facility_type)]
                count = len(filtered)
                if count == 0:
                    return 0
                return filtered['RCF Outstanding Amount'].sum() / count

            return safe_avg("Cash Flow Priority Revolver") + safe_avg("ABL - Working Capital Facility")

        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["RCF Exposure (Priority,ABL)"] = portfolio_df.apply(rfc_exposure_priority_abl_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def first_lien_working_capital_faciltiy_greater_1_25_ebitda(self):
        # =IF(OR(H11<>"First Lien",AND(H11="First Lien",OR(I11="Cash Flow Pari Passu Revolver",I11="None"))),"No",IF(AND(I11="Cash Flow Priority Revolver",OR(ISBLANK(J11),ISBLANK(K11),OR(ISBLANK(L11),(Availability!$F$12-L11)>32),M11>CY11,(J11/CR11)>1.25)),"Yes",IF(AND(I11="ABL - Working Capital Facility",OR(ISBLANK(J11),ISBLANK(K11),ISBLANK(L11),N11>CY11,(J11/CR11)>1.25)),"Yes","No")))

        def first_lien_working_capital_faciltiy_greater_1_25_ebitda_helper(row):
            if row["Loan Type"] != "First Lien" or (row["Loan Type"] == "First Lien" and row["RCF Exposure Type"] in ["Cash Flow Pari Passu Revolver", "None"]):
                return "No"

            if row["RCF Exposure Type"] == "Cash Flow Priority Revolver":
                if (
                    pd.isna(row["RCF Commitment Amount"]) or
                    pd.isna(row["RCF Outstanding Amount"]) or
                    pd.isna(row["RCF Update Date"]) or
                    ((cutoff - row["RCF Update Date"]).days > 32 if not pd.isna(row["RCF Update Date"]) else True) or
                    (row["RCF Exposure (Priority,Pari,ABL)"] > row["Permitted TTM EBITDA in Local Currency at relevant test period"] if not pd.isna(row["RCF Exposure (Priority,Pari,ABL)"]) and not pd.isna(row["Permitted TTM EBITDA in Local Currency at relevant test period"]) else True) or
                    (row["RCF Commitment Amount"] / row["Permitted TTM EBITDA (USD)"] > 1.25 if not pd.isna(row["RCF Commitment Amount"]) and not pd.isna(row["Permitted TTM EBITDA (USD)"]) and row["Permitted TTM EBITDA (USD)"] != 0 else True)
                ):
                    return "Yes"
                else:
                    return "No"

            if row["RCF Exposure Type"] == "ABL - Working Capital Facility":
                if (
                    pd.isna(row["RCF Commitment Amount"]) or
                    pd.isna(row["RCF Outstanding Amount"]) or
                    pd.isna(row["RCF Update Date"]) or
                    (row["RCF Exposure (Priority,ABL)"] > row["Permitted TTM EBITDA in Local Currency at relevant test period"] if not pd.isna(row["RCF Exposure (Priority,ABL)"]) and not pd.isna(row["Permitted TTM EBITDA in Local Currency at relevant test period"]) else True) or
                    (row["RCF Commitment Amount"] / row["Permitted TTM EBITDA (USD)"] > 1.25 if not pd.isna(row["RCF Commitment Amount"]) and not pd.isna(row["Permitted TTM EBITDA (USD)"]) and row["Permitted TTM EBITDA (USD)"] != 0 else True)
                ):
                    return "Yes"
                else:
                    return "No"

            return "No"

        availability_df = self.calculator_info.intermediate_calculation_dict['Availability']
        cutoff = availability_df.query("Terms == 'Measurement Date:'")["Values"].iloc[0]
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["First Lien & Working Capital Faciltiy > 1.25x EBITDA"] = portfolio_df.apply(first_lien_working_capital_faciltiy_greater_1_25_ebitda_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df


    def recurring_revenue(self):
        # =IF(H11<>"Recurring Revenue","na",IF(OR(I11="None",I11="Cash Flow Pari Passu Revolver"),"na",IF(AND(OR(I11="ABL - Working Capital Facility",I11="Cash Flow Priority Revolver"),OR(ISBLANK(J11),(J11/CR11)>1)),"Yes","No")))

        def recurring_revenue_helper(row):
            if row["Loan Type"] != "Recurring Revenue":
                return "na"
            elif row["RCF Exposure Type"] in ["None", "Cash Flow Pari Passu Revolver"]:
                return "na"
            elif row["RCF Exposure Type"] in ["ABL - Working Capital Facility", "Cash Flow Priority Revolver"]:
                if pd.isna(row["RCF Commitment Amount"]) or (row["Permitted TTM EBITDA (USD)"] != 0 and row["RCF Commitment Amount"] / row["Permitted TTM EBITDA (USD)"] > 1):
                    return "Yes"
                else:
                    return "No"
            else:
                return "No"

        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Recurring Revenue"] = portfolio_df.apply(recurring_revenue_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df
    
    def pass_fail_rfc_test(self):
        # =IF(AND(OR(H11="First Lien",H11="Recurring Revenue"),OR(O11="Yes",P11="Yes")),"Fail","Pass")
        
        def pass_fail_rfc_test_helper(row):
            if row["Loan Type"] in ["First Lien", "Recurring Revenue"] and row["First Lien & Working Capital Faciltiy > 1.25x EBITDA"] == "Yes" or row["Recurring Revenue"] == "Yes":
                return "Fail"
            return "Pass"
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Pass/Fail RCF Test"] = portfolio_df.apply(pass_fail_rfc_test_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def calculated_loan_type(self):
        # =IF(AND(H11="First Lien",Q11="Fail"),"Last Out",IF(AND(H11="Recurring Revenue",Q11="Fail"),"Ineligible",H11))
        def calculated_loan_type_helper(row):
            if row["Loan Type"] == "First Lien" and row["Pass/Fail RCF Test"] == "Fail":
                return "Last Out"
            elif row["Loan Type"] == "Recurring Revenue" and row["Pass/Fail RCF Test"] == "Fail":
                return "Ineligible"
            else:
                return row["Loan Type"]
        
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Calculated Loan Type"] = portfolio_df.apply(calculated_loan_type_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df
    
    def calculated_loan_type_post_aa_discretion(self):
        # =IF(AND(OR(H11="First Lien",H11="Recurring Revenue"),Q11="Fail",S11="Yes"),H11,R11)

        def calculated_loan_type_post_aa_discretion_helper(row):
            if row["Loan Type"] in ["First Lien", "Recurring Revenue"] and row["Pass/Fail RCF Test"] == "Fail" and row["Admin Agent Approval (RCF)"] == "Yes":
                return row["Loan Type"]
            else:
                return row["Calculated Loan Type"]
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Calculated Loan Type post AA Discretion"] = portfolio_df.apply(calculated_loan_type_post_aa_discretion_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def borrower_outstanding_principal_balance_usd(self):
        # =ARRAY_CONSTRAIN(ARRAYFORMULA(IFERROR(VLOOKUP(INDEX(Portfolio!BT:BT,MATCH(G11,Portfolio!G:G,0),0),Availability!$B$68:$L$72,11,0)*X11,"-")), 1, 1)

        def borrower_outstanding_principal_balance_usd_helper(row):
            currency = row['Approved Currency']
            borrower_outstanding_principal_balance = row['Borrower Outstanding Principal Balance']
            exchange_rate = exchange_rate_map.get(currency)
            return exchange_rate * borrower_outstanding_principal_balance if exchange_rate is not None else "-"
        
        exchange_rate_map = self.calculator_info.intermediate_calculation_dict['exchange_rate_map']
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Borrower Outstanding Principal Balance (USD)"] = portfolio_df.apply(borrower_outstanding_principal_balance_usd_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    
    def borrower_facility_commitment_usd(self):
        # =ARRAY_CONSTRAIN(ARRAYFORMULA(IFERROR(VLOOKUP(INDEX(Portfolio!BT:BT,MATCH(G11,Portfolio!G:G,0),0),Availability!$B$68:$L$72,11,0)*Y11,"-")), 1, 1)
        def borrower_facility_commitment_usd_helper(row):
            currency = row['Approved Currency']
            borrower_facility_commitment = row['Borrower Facility Commitment']
            exchange_rate = exchange_rate_map.get(currency)
            return exchange_rate * borrower_facility_commitment if exchange_rate is not None else "-"

        exchange_rate_map = self.calculator_info.intermediate_calculation_dict['exchange_rate_map']
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Borrower Facility Commitment (USD)"] = portfolio_df.apply(borrower_facility_commitment_usd_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df
    
    def borrowing_unfunded_amount_usd(self):
        # =AG11-AF11

        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Borrowing Unfunded Amount (USD)"] = portfolio_df["Borrower Facility Commitment (USD)"] - portfolio_df["Borrower Outstanding Principal Balance (USD)"]
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df
      
    

    def calculate_RVCBB(self):
        self.rcf_exposure_priority_pari_abl() # column 'M'
        self.rfc_exposure_priority_abl() # column 'N'
        self.first_lien_working_capital_faciltiy_greater_1_25_ebitda() # column 'O'
        self.recurring_revenue() # column 'P'
        self.pass_fail_rfc_test() # column 'Q'
        self.calculated_loan_type() # column 'R'
        self.calculated_loan_type_post_aa_discretion() # column 'T'
        self.borrower_outstanding_principal_balance_usd() #column 'AF'
        self.borrower_facility_commitment_usd() # column 'AG'
        self.borrowing_unfunded_amount_usd() # column 'AH'
        


        