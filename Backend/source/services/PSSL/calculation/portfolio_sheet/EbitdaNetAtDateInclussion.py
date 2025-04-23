import numpy as np
import pandas as pd

class EbitdaNetAtDateInclussion:
    def __init__(self, calculator_info):
        self.calculator_info = calculator_info

    def add_back_cap_percent(self):
        # =IF((CI11-CJ11)<0,"N/A",IF(CJ11=0,0,CJ11/(CI11-CJ11)))
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Add-Back Cap (%)"] = portfolio_df.apply(
            lambda row: "N/A" if (row["Initial TTM Adjusted EBITDA"] - row["Add-Backs"]) < 0 else (0 if row["Add-Backs"] == 0 else row["Add-Backs"] / (row["Initial TTM Adjusted EBITDA"] - row["Add-Backs"])), axis=1
        )
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def capped_add_back_percent(self):
        # =IF(CI11-CJ11<0,"na",IF(AND(CF11="Yes",CI11-CJ11>=50000000),"Uncapped",35%))
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Capped Add-Back %"] = portfolio_df.apply(
            lambda row: "na" if (row["Initial TTM Adjusted EBITDA"] - row["Add-Backs"]) < 0
            else (np.nan if row["Rated B- or Better"] == "Yes" and (row["Initial TTM Adjusted EBITDA"] - row["Add-Backs"]) >= 50000000
                else 0.35),
            axis=1
        )
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def excess_add_backs(self):
        # =IF((CI11-CJ11)<0,CJ11,IF(CK11>CL11,(CJ11-(CI11-CJ11)*CL11),0))
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Excess Add-Backs"] = portfolio_df.apply(
            lambda row: row["Add-Backs"] if (row["Initial TTM Adjusted EBITDA"] - row["Add-Backs"]) < 0
                else (row["Add-Backs"] - (row["Initial TTM Adjusted EBITDA"] - row["Add-Backs"]) * row["Capped Add-Back %"] if row["Add-Back Cap (%)"] > row["Capped Add-Back %"] else 0),
            axis=1
        )
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def permitted_ttm_ebitda_in_local_currency(self):
        # =CI11-CM11+CO11
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Permitted TTM EBITDA in Local Currency"] = portfolio_df["Initial TTM Adjusted EBITDA"] - portfolio_df["Excess Add-Backs"] + portfolio_df["Admin Agent Approved Add-Backs"]
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def ebitda_haircut(self):
        # =MAX(0,(1-CP11/CI11))
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["EBITDA Haircut"] = portfolio_df.apply(
            lambda row: max(0, 1 - row["Permitted TTM EBITDA in Local Currency"] / row["Initial TTM Adjusted EBITDA"]) if row["Initial TTM Adjusted EBITDA"] != 0 else 0,
            axis=1
        )
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def permitted_ttm_ebitda_usd(self):
        # =ARRAY_CONSTRAIN(ARRAYFORMULA(IFERROR(VLOOKUP(INDEX(Portfolio!BT:BT,MATCH(G11,Portfolio!G:G,0),0),Availability!$B$68:$L$72,11,0)*CP11,"-")), 1, 1)
        exchange_rate_map = self.calculator_info.intermediate_calculation_dict['exchange_rate_map']
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Permitted TTM EBITDA (USD)"] = portfolio_df.apply(
            lambda row: exchange_rate_map.get(row["Approved Currency"], np.nan) * row["Permitted TTM EBITDA in Local Currency"] if pd.notna(exchange_rate_map.get(row["Approved Currency"], np.nan)) else np.nan,
            axis=1
        )
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    
    def initial_unrestricted_cash(self):
        # =ARRAY_CONSTRAIN(ARRAYFORMULA(IFERROR(VLOOKUP(INDEX(Portfolio!BT:BT,MATCH(G11,Portfolio!G:G,0),0),Availability!$B$68:$L$72,11,0)*Z11,"-")), 1, 1)
        
        def initial_unrestricted_cash_helper(row):
            if exchange_rate_map.get(row["Approved Currency"]) == None:
                exchange_rate_map.get(row["Approved Currency"], 0.0) * row["Initial Unrestricted Cash (Local Currency)"]
            else:
                return 0
        exchange_rate_map = self.calculator_info.intermediate_calculation_dict['exchange_rate_map']
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        # portfolio_df["Initial Unrestricted Cash (Local Currency)"].fillna(0)
        portfolio_df[['Initial Unrestricted Cash (Local Currency)', 'Approved Currency']] = portfolio_df[['Initial Unrestricted Cash (Local Currency)', 'Approved Currency']].fillna(value=0.0)
        portfolio_df["Initial Unrestricted Cash"] = portfolio_df.apply(initial_unrestricted_cash_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df


    def initial_gross_senior_debt(self):
        # =ARRAY_CONSTRAIN(ARRAYFORMULA(IFERROR(VLOOKUP(INDEX(Portfolio!BT:BT,MATCH(G11,Portfolio!G:G,0),0),Availability!$B$68:$L$72,11,0)*AA11,"-")), 1, 1)
        exchange_rate_map = self.calculator_info.intermediate_calculation_dict['exchange_rate_map']
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Initial Gross Senior Debt"] = portfolio_df.apply(
            lambda row: exchange_rate_map.get(row["Approved Currency"], np.nan) * row["Initial Gross Senior Debt (Local Currency)"] if pd.notna(exchange_rate_map.get(row["Approved Currency"], np.nan)) else np.nan,
            axis=1
        )
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def initial_gross_total_debt(self):
        # =ARRAY_CONSTRAIN(ARRAYFORMULA(IFERROR(VLOOKUP(INDEX(Portfolio!BT:BT,MATCH(G11,Portfolio!G:G,0),0),Availability!$B$68:$L$72,11,0)*AB11,"-")), 1, 1)
        exchange_rate_map = self.calculator_info.intermediate_calculation_dict['exchange_rate_map']
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Initial Gross Total Debt"] = portfolio_df.apply(
            lambda row: exchange_rate_map.get(row["Approved Currency"], np.nan) * row["Initial Gross Total Debt (Local Currency)"] if pd.notna(exchange_rate_map.get(row["Approved Currency"], np.nan)) else np.nan,
            axis=1
        )
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df
        
    def calculate_ENADI(self):
        self.add_back_cap_percent() # column 'CK'
        self.capped_add_back_percent() # column 'CL'
        self.excess_add_backs() # column 'CM'
        self.permitted_ttm_ebitda_in_local_currency() # column 'CP'
        self.ebitda_haircut() # column 'CQ'
        self.permitted_ttm_ebitda_usd()  # column 'CR'
        self.initial_unrestricted_cash() # column 'CS'
        self.initial_gross_senior_debt() # column 'CT'
        self.initial_gross_total_debt() # column 'CU'