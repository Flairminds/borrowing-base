import numpy as np
import pandas as pd

class RecurringRevenueInterestCoverage:
    def __init__(self, calculator_info):
        self.calculator_info = calculator_info

    def initial_multiple(self):
        # =IF(H11<>"Recurring Revenue","n/a",CU11/DJ11)

        # def initial_multiple_helper(row):
        #     if row["Loan Type"] != "Recurring Revenue":
        #         return np.nan
        #     initial_multiple_value = row["Initial Gross Total Debt"]/ row["Initial Annualized Recurring Revenue"]
        #     return initial_multiple_value

        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Initial Multiple"] = portfolio_df.apply(lambda row: np.nan if row["Loan Type"] != "Recurring Revenue" else row["Initial Gross Total Debt"]/ row["Initial Annualized Recurring Revenue"], axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df
        
    
    def vae_multiple(self):
        # =ARRAY_CONSTRAIN(ARRAYFORMULA(IFERROR(IF(H11<>"Recurring Revenue","n/a",INDEX(VAE,MATCH(G11&MAX(IF(VAE!$C$5:$C$116=G11,IF(VAE!$F$5:$F$116<=Availability!$F$12,VAE!$F$5:$F$116))),VAE!$C$5:$C$116&VAE!$F$5:$F$116,0),MATCH("Debt-to-Recurring Revenue Ratio",VAE!$H$4:$R$4,0))),DL11)), 1, 1)

        def vae_multiple_helper(row):
            if row["Loan Type"] != "Recurring Revenue":
                return np.nan
            
            borrower = row["Borrower"]
            initial_multiple = row["Initial Multiple"]
            
            filtered = vae_df[(vae_df["Obligor"] == borrower) & (vae_df["Date of VAE Decision"] <= cutoff)]

            if not filtered.empty:
                max_row = filtered.loc[filtered["Date of VAE Decision"].idxmax()]
                return max_row.get("Debt-to-Recurring Revenue Ratio", initial_multiple)
            else:
                return initial_multiple

        availability_df = self.calculator_info.intermediate_calculation_dict['Availability']
        vae_df = self.calculator_info.intermediate_calculation_dict['VAE']
        cutoff = availability_df.query("Terms == 'Measurement Date:'")["Values"].iloc[0]
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["VAE Multiple"] = portfolio_df.apply(vae_multiple_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df
        
    
    def current_multiple(self):
        # =IF(H11<>"Recurring Revenue","n/a",CU11/DK11)
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Current Multiple"] = portfolio_df.apply(lambda row: np.nan if row["Loan Type"] != "Recurring Revenue" else row["Initial Gross Total Debt"] / row["Annualized Recurring Revenue"], axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df
        
    
    def vae_liquidity(self):
        # =ARRAY_CONSTRAIN(ARRAYFORMULA(IFERROR(IF(H11<>"Recurring Revenue","n/a",INDEX(VAE,MATCH(G11&MAX(IF(VAE!$C$5:$C$116=G11,IF(VAE!$F$5:$F$116<=Availability!$F$12,VAE!$F$5:$F$116))),VAE!$C$5:$C$116&VAE!$F$5:$F$116,0),MATCH("Liquidity",VAE!$H$4:$R$4,0))),DO11)), 1, 1)

        def vae_liquidity_helper(row):
            if row["Loan Type"] != "Recurring Revenue":
                return np.nan
            
            borrower = row["Borrower"]
            initial_liquidity = row["Initial Liquidity"]
            
            filtered = vae_df[(vae_df["Obligor"] == borrower) & (vae_df["Date of VAE Decision"] <= cutoff)]

            if not filtered.empty:
                max_row = filtered.loc[filtered["Date of VAE Decision"].idxmax()]
                return max_row.get("Debt-to-Recurring Revenue Ratio", initial_liquidity)
            else:
                return initial_liquidity

        availability_df = self.calculator_info.intermediate_calculation_dict['Availability']
        vae_df = self.calculator_info.intermediate_calculation_dict['VAE']
        cutoff = availability_df.query("Terms == 'Measurement Date:'")["Values"].iloc[0]
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["VAE Liquidity"] = portfolio_df.apply(vae_liquidity_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df
        
    def initial_interest_coverage_ratio(self):
        # =CP11/DR11
        
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df[["Permitted TTM EBITDA in Local Currency"]] = portfolio_df[["Permitted TTM EBITDA in Local Currency"]].fillna(0)
        portfolio_df[["Initial Cash Interest Expense"]] = portfolio_df[["Initial Cash Interest Expense"]].fillna(1)
        portfolio_df["Initial Interest Coverage Ratio"] = portfolio_df.apply(lambda row: row["Permitted TTM EBITDA in Local Currency"] / row["Initial Cash Interest Expense"], axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    
    def vae_interest_coverage(self):
        # =ARRAY_CONSTRAIN(ARRAYFORMULA(IFERROR(INDEX(VAE,MATCH(G11&MAX(IF(VAE!$C$5:$C$116=G11,IF(VAE!$F$5:$F$116<=Availability!$F$12,VAE!$F$5:$F$116))),VAE!$C$5:$C$116&VAE!$F$5:$F$116,0),MATCH("Interest Coverage",VAE!$H$4:$R$4,0)),DT11)), 1, 1)

        def vae_interest_coverage_helper(row):
            borrower = row["Borrower"]
            initial_interest_coverage_ratio = row["Initial Interest Coverage Ratio"]
            
            filtered = vae_df[(vae_df["Obligor"] == borrower) & (vae_df["Date of VAE Decision"] <= cutoff)]

            if not filtered.empty:
                max_row = filtered.loc[filtered["Date of VAE Decision"].idxmax()]
                return max_row.get("Interest Coverage", initial_interest_coverage_ratio)
            else:
                return initial_interest_coverage_ratio

        availability_df = self.calculator_info.intermediate_calculation_dict['Availability']
        vae_df = self.calculator_info.intermediate_calculation_dict['VAE']
        cutoff = availability_df.query("Terms == 'Measurement Date:'")["Values"].iloc[0]
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["VAE Interest Coverage"] = portfolio_df.apply(vae_interest_coverage_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df
    
    def current_interest_coverage_ratio(self):
        # =CZ11/DS11
        
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Current Interest Coverage Ratio"] = portfolio_df.apply(lambda row: np.nan if pd.isnull(row["Current Cash Interest Expense"]) or row["Current Cash Interest Expense"] == 0 else row["Permitted TTM EBITDA (USD) at relevant test period"] / row["Current Cash Interest Expense"], axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df


    def calculate_RRIC(self):
        self.initial_multiple() # column 'DL'
        self.vae_multiple() # column 'DM' 
        self.current_multiple() # column 'DN' 
        self.vae_liquidity() # column 'DP'
        self.initial_interest_coverage_ratio() # column 'DT'
        self.vae_interest_coverage() # column 'DU'
        self.current_interest_coverage_ratio()  # column 'DV'

