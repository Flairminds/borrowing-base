import pandas as pd
import numpy as np


class EbitdaNetDebtRelevantTestPeriod:
    def __init__(self, calculator_info):
        self.calculator_info = calculator_info

    def inclusion_ebitda_haircut(self):
        # =IF(COUNTIFS(VAE!C:C,G11,VAE!D:D,"(a) Credit Quality Deterioration Event")>=1,0,CQ11)
        def inclusion_ebitda_haircut_helper(row):
            count = vae_df[(vae_df["Obligor"] == row["Borrower"]) & (vae_df["Event Type"] == "(a) Credit Quality Deterioration Event")].shape[0]
            return 0 if count >= 1 else row["EBITDA Haircut"]
        
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        vae_df = self.calculator_info.intermediate_calculation_dict['VAE']
        portfolio_df["Inclusion EBITDA Haircut"] = portfolio_df.apply(inclusion_ebitda_haircut_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def permitted_ttm_ebitda_in_local_currency_at_relevant_test_period(self):
        # =(1-CX11)*CW11
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df[["Inclusion EBITDA Haircut", "Adjusted TTM EBITDA"]] = portfolio_df[["Inclusion EBITDA Haircut", "Adjusted TTM EBITDA"]].fillna(0.0)
        portfolio_df["Permitted TTM EBITDA in Local Currency at relevant test period"] = portfolio_df.apply(
            lambda row: ((1 - row["Inclusion EBITDA Haircut"]) * row["Adjusted TTM EBITDA"]), 
            axis=1
        )
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def permitted_ttm_ebitda_usd_at_relevant_test_period(self):
        # =ARRAY_CONSTRAIN(ARRAYFORMULA(IFERROR(VLOOKUP(INDEX(Portfolio!BT:BT,MATCH(G11,Portfolio!G:G,0),0),Availability!$B$68:$L$72,11,0)*CY11,"-")), 1, 1)

        def permitted_ttm_ebitda_usd_at_relevant_test_period_helper(row):
            exchange_rate = exchange_rate_map.get(row["Approved Currency"])
            if exchange_rate:
                return exchange_rate * row["Permitted TTM EBITDA in Local Currency at relevant test period"]
            else:
                return np.nan
    
        exchange_rate_map = self.calculator_info.intermediate_calculation_dict['exchange_rate_map']
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Permitted TTM EBITDA (USD) at relevant test period"] = portfolio_df.apply(permitted_ttm_ebitda_usd_at_relevant_test_period_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def current_unrestricted_cash(self):
        # =ARRAY_CONSTRAIN(ARRAYFORMULA(IFERROR(VLOOKUP(INDEX(Portfolio!BT:BT,MATCH(G11,Portfolio!G:G,0),0),Availability!$B$68:$L$72,11,0)*AC11,"-")), 1, 1)
        
        exchange_rate_map = self.calculator_info.intermediate_calculation_dict['exchange_rate_map']
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Current Unrestricted Cash"] = portfolio_df.apply(
            lambda row: exchange_rate_map.get(row["Approved Currency"], np.nan) * row["Current Unrestricted Cash (Local Currency)"] if pd.notna(exchange_rate_map.get(row["Approved Currency"], np.nan)) else np.nan,
            axis=1
        )
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def current_gross_senior_debt(self):
        # =ARRAY_CONSTRAIN(ARRAYFORMULA(IFERROR(VLOOKUP(INDEX(Portfolio!BT:BT,MATCH(G11,Portfolio!G:G,0),0),Availability!$B$68:$L$72,11,0)*AD11,"-")), 1, 1)
        exchange_rate_map = self.calculator_info.intermediate_calculation_dict['exchange_rate_map']
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Current Gross Senior Debt"] = portfolio_df.apply(
            lambda row: exchange_rate_map.get(row["Approved Currency"], np.nan) * row["Current Gross Senior Debt (Local Currency)"] if pd.notna(exchange_rate_map.get(row["Approved Currency"], np.nan)) else np.nan,
            axis=1
        )
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def current_gross_total_debt(self):
        # =ARRAY_CONSTRAIN(ARRAYFORMULA(IFERROR(VLOOKUP(INDEX(Portfolio!BT:BT,MATCH(G11,Portfolio!G:G,0),0),Availability!$B$68:$L$72,11,0)*AE11,"-")), 1, 1)
        
        exchange_rate_map = self.calculator_info.intermediate_calculation_dict['exchange_rate_map']
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Current Gross Total Debt"] = portfolio_df.apply(
            lambda row: exchange_rate_map.get(row["Approved Currency"], np.nan) * row["Current Gross Total Debt (Local Currency)"] if pd.notna(exchange_rate_map.get(row["Approved Currency"], np.nan)) else np.nan,
            axis=1
        )
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def claculate_ENDRTP(self):
        self.inclusion_ebitda_haircut() # column 'CX'
        self.permitted_ttm_ebitda_in_local_currency_at_relevant_test_period() # column 'CY'
        self.permitted_ttm_ebitda_usd_at_relevant_test_period() # column 'CZ'
        self.current_unrestricted_cash() # column 'DA'
        self.current_gross_senior_debt() # column 'DB'
        self.current_gross_total_debt() # column 'DC'
