class LeverageRatiosPermittedTtmEbitda:
    def __init__(self, calculator_info):
        self.calculator_info = calculator_info

    def initial_net_senior(self):
        # =(CT11-CS11)/CR11
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Initial Net Senior"] = portfolio_df.apply(
            lambda row: (row["Initial Gross Senior Debt"] - row["Initial Unrestricted Cash"]) / row["Permitted TTM EBITDA (USD)"],
            axis=1
        )
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def initial_net_total(self):
        # =(CU11-CS11)/CR11
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Initial Net Total"] = portfolio_df.apply(
            lambda row: (row["Initial Gross Total Debt"] - row["Initial Unrestricted Cash"]) / row["Permitted TTM EBITDA (USD)"],
            axis=1
        )
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def vae_net_senior(self):
        # =ARRAY_CONSTRAIN(ARRAYFORMULA(IFERROR(INDEX(VAE,MATCH(G11&MAX(IF(VAE!$C$5:$C$116=G11,IF(VAE!$F$5:$F$116<=Availability!$F$12,VAE!$F$5:$F$116))),VAE!$C$5:$C$116&VAE!$F$5:$F$116,0),MATCH("Net Senior Leverage",VAE!$H$4:$R$4,0)),DD11)), 1, 1)
        

        def vae_net_senior_helper(row):
            g_val = row["Borrower"]
            dd_val = row["Initial Net Senior"]
            
            filtered = vae_df[(vae_df["Obligor"] == g_val) & (vae_df["Date of VAE Decision"] <= cutoff)]
            
            if not filtered.empty:
                max_row = filtered.loc[filtered["Date of VAE Decision"].idxmax()]
                return max_row.get("Net Senior Leverage", dd_val)
            else:
                return dd_val
        
        availability_df = self.calculator_info.intermediate_calculation_dict['Availability']
        vae_df = self.calculator_info.intermediate_calculation_dict['VAE']
        cutoff = availability_df.query("Terms == 'Measurement Date:'")["Values"].iloc[0]
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["VAE Net Senior"] = portfolio_df.apply(vae_net_senior_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df


    
    def vae_net_total(self):
        # =ARRAY_CONSTRAIN(ARRAYFORMULA(IFERROR(INDEX(VAE,MATCH(G11&MAX(IF(VAE!$C$5:$C$116=G11,IF(VAE!$F$5:$F$116<=Availability!$F$12,VAE!$F$5:$F$116))),VAE!$C$5:$C$116&VAE!$F$5:$F$116,0),MATCH("Net Total Leverage",VAE!$H$4:$R$4,0)),DE11)), 1, 1)
        
        def vae_net_total_helper(row):
            g_val = row["Borrower"]
            de_val = row["Initial Net Total"]
            
            filtered = vae_df[(vae_df["Obligor"] == g_val) & (vae_df["Date of VAE Decision"] <= cutoff)]
            
            if not filtered.empty:
                max_row = filtered.loc[filtered["Date of VAE Decision"].idxmax()]
                return max_row.get("Net Total Leverage", de_val)
            else:
                return de_val
        
        availability_df = self.calculator_info.intermediate_calculation_dict['Availability']
        vae_df = self.calculator_info.intermediate_calculation_dict['VAE']
        cutoff = availability_df.query("Terms == 'Measurement Date:'")["Values"].iloc[0]
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["VAE Net Total"] = portfolio_df.apply(vae_net_total_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df
    
    def current_net_senior(self):
        # =(DB11-DA11)/CZ11
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        portfolio_df["Current Net Senior"] = (portfolio_df["Current Gross Senior Debt"] - portfolio_df["Current Unrestricted Cash"]) / portfolio_df["Permitted TTM EBITDA (USD) at relevant test period"]
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def current_net_total(self):
        # =(DC11-DA11)/CZ11
        
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        # portfolio_df["Current Net Total"] = portfolio_df.apply(lambda row: (row["Current Gross Total Debt"] - row["Current Unrestricted Cash"]) / row["Permitted TTM EBITDA (USD) at relevant test period"])
        portfolio_df["Current Net Total"] = (portfolio_df["Current Gross Total Debt"] - portfolio_df["Current Unrestricted Cash"]) / portfolio_df["Permitted TTM EBITDA (USD) at relevant test period"]
        self.calculator_info.intermediate_calculation_dict['Portfolio'] = portfolio_df

    def calculate_LRPTE(self):
        self.initial_net_senior() # column 'DD'
        self.initial_net_total() # column 'DE'
        self.vae_net_senior() # column 'DF'
        self.vae_net_total() # column 'DG'
        self.current_net_senior() # column 'DH'
        self.current_net_total() # column 'DI'