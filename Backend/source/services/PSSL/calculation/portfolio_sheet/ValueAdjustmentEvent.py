import numpy as np
import pandas as pd

class ValueAdjustmentEvent:
    def __init__(self, calculator_info):
        self.calculator_info = calculator_info

    def cash_interest_coverage_ratio_test(self):
        # =IF(AND(DV11/DU11<0.85,DV11<1.5),"Yes","No")
        def cash_interest_coverage_ratio_test_helper(row):
            try:
                if (row["Current Interest Coverage Ratio"] / row["VAE Interest Coverage"] < 0.85) and (row["Current Interest Coverage Ratio"] < 1.5):
                    return "Yes"
                else:
                    return "No"
            except Exception as e:
                return "No"
                     
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Cash Interest Coverage Ratio Test"] = portfolio_df.apply(cash_interest_coverage_ratio_test_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def net_senior_leverage_ratio_test(self):
        # =IF(OR(H11="First Lien",H11="Last Out"),IF(AND((DH11-DF11)>0.5,DH11>4),"Yes","No"),"No")

        def condition1(row):
            if row["Loan Type"]=="First Lien" and row["Loan Type"]=="Last Out":
                return True
            else:
                return False
            
        def condition2(row):
            if ((row["Current Net Senior"] - row["VAE Net Senior"]) > 0.5) and (row["Current Net Senior"] > 4):
                return True
            else:
                False

        def net_senior_leverage_ratio_test_helper(row):
            # if () or ():
            if condition1(row) or condition2(row):
                return "Yes"
            else:
                return "No"
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Net Senior Leverage Ratio Test"] = portfolio_df.apply(net_senior_leverage_ratio_test_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    
    def net_total_leverage_test(self):
        # =IF(H11="Second Lien",IF(AND((DI11-DG11)>0.5,DI11>4),"Yes","No"),"No")
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Net Total Leverage Test"] = portfolio_df.apply(
            lambda row: "Yes" if row["Loan Type"] == "Second Lien" and (row["Current Net Total"] - row["VAE Net Total"] > 0.5) and (row["Current Net Total"] > 4) else "No",
            axis=1
        )
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df
    

    def recurring_revenue_multiple(self):
        # =IF(G11="Recurring Revenue",IF(AND((DN11-DM11)>0.25,DN11>1),"Yes","No"),"No")
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Recurring Revenue Multiple"] = portfolio_df.apply(
            lambda row: "Yes" if row["Loan Type"] == "Recurring Revenue" and (row["Current Multiple"] - row["VAE Multiple"] > 0.25) and (row["Current Multiple"] > 1) else "No",
            axis=1
        )
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def liquidity_credit_quality_deterioration(self):
        # =IF(G11="Recurring Revenue",IF((DQ11/DP11)<=0.85,"Yes","No"),"No")
        
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Liquidity Credit Quality Deterioration"] = portfolio_df.apply(
            lambda row: "Yes" if row["Loan Type"] == "Recurring Revenue" and row["VAE Liquidity"] not in [0, None, np.nan] and (row["Current Liquidity"] / row["VAE Liquidity"] <= 0.85) else "No",
            axis=1
        )
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def day_count(self):
        # =IF(AND(EL11="Yes",EN11="Yes"),DAYS(EO11,EM11),IF(EL11="Yes",DAYS(Availability!$F$12,Portfolio!EM11),""))

        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        availability_df = self.calculator_info.intermediate_calculation_dict['Availability']
        cutoff = availability_df.query("Terms == 'Measurement Date:'")["Values"].iloc[0]

        portfolio_df["Day Count"] = portfolio_df.apply(
            lambda row: (row["Date Financials Provided to Ally"] - row["Date of Financial Delivery VAE"]).days if row["Reporting Failure Event"] == "Yes" and row["Finanicals Since Received?"] == "Yes"
            else (cutoff - row["Date of Financial Delivery VAE"]).days if row["Reporting Failure Event"] == "Yes"
            else np.nan,
            axis=1
        )
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def advance_rate_class(self):
        # =IF(CZ11<10000000,"< $10MM",IF(CZ11<50000000,"≥ $10MM and < $50MM",IF(AND(CF11="Yes",CG11="Yes"),"≥ $50MM & B- or better","≥ $50MM & Unrated")))
    
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        
        portfolio_df["Advance Rate Class"] = portfolio_df.apply(
            lambda row: "< $10MM" if row["Permitted TTM EBITDA (USD) at relevant test period"] < 10000000
            else "≥ $10MM and < $50MM" if row["Permitted TTM EBITDA (USD) at relevant test period"] < 50000000
            else "≥ $50MM & B- or better" if row["Rated B- or Better"] == "Yes" and row["Two Market Quotes"] == "Yes"
            else "≥ $50MM & Unrated",
            axis=1
        )
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df
    

    def calculate_vae(self):
        self.cash_interest_coverage_ratio_test() # column 'DW'
        self.net_senior_leverage_ratio_test() # column 'DX'
        self.net_total_leverage_test() # column 'DY'
        self.recurring_revenue_multiple() # column 'DZ'
        self.liquidity_credit_quality_deterioration() # column 'EA'
        self.day_count() # column 'EP'
        self.advance_rate_class() # column 'ER'
