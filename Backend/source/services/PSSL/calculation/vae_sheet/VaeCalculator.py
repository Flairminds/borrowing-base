import numpy as np

class VaeCalculator:
    def __init__(self, calculator_info):
        self.calculator_info = calculator_info

    def is_nan(self, value):
        return value != value

    def net_senior_leverage(self):
        # =IFERROR((I5-K5)/H5,"-")

        def net_senior_leverage_helper(row):
            try:
                senior_debt = row["Senior Debt"]
                if self.is_nan(senior_debt):
                    senior_debt = 0
                unrestricted_cash = row["Unrestricted Cash"]
                if self.is_nan(unrestricted_cash):
                    unrestricted_cash = 0
                ttm_ebitda = row["TTM EBITDA"]
                if self.is_nan(ttm_ebitda):
                    ttm_ebitda = 0
                net_senior_leverage_value = (senior_debt - unrestricted_cash) / ttm_ebitda
                return net_senior_leverage_value
            except Exception as e:
                return np.nan
        
        vae_df = self.calculator_info.intermediate_calculation_dict['VAE']
        vae_df["Net Senior Leverage"] = vae_df.apply(net_senior_leverage_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['VAE'] = vae_df


    def net_total_leverage(self):
        # =IFERROR((J5-K5)/H5,"-")
        
        def net_total_leverage_helper(row):
            try:
                total_debt = row["Total Debt"]
                if self.is_nan(total_debt):
                    total_debt = 0
                unrestricted_cash = row["Unrestricted Cash"]
                if self.is_nan(unrestricted_cash):
                    unrestricted_cash = 0
                ttm_ebitda = row["TTM EBITDA"]
                if self.is_nan(ttm_ebitda):
                    ttm_ebitda = 0
                net_total_leverage_value = (total_debt - unrestricted_cash) / ttm_ebitda
                return net_total_leverage_value
            except Exception as e:
                return np.nan
        
        vae_df = self.calculator_info.intermediate_calculation_dict['VAE']
        vae_df["Net Total Leverage"] = vae_df.apply(net_total_leverage_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['VAE'] = vae_df

    def debt_to_recurring_revenue_ratio(self):
        # =IFERROR((H5)/O5,"-")

        def debt_to_recurring_revenue_ratio_helper(row):
            try:
                ttm_ebitda = row["TTM EBITDA"]
                if self.is_nan(ttm_ebitda):
                    ttm_ebitda = 0
                recurring_revenue = row["Recurring Revenue"]
                if self.is_nan(recurring_revenue):
                    recurring_revenue = 0
                debt_to_recurring_revenue_ratio_value = ttm_ebitda / recurring_revenue
                return debt_to_recurring_revenue_ratio_value
            except Exception as e:
                return np.nan
        
        vae_df = self.calculator_info.intermediate_calculation_dict['VAE']
        vae_df["Debt-to-Recurring Revenue Ratio"] = vae_df.apply(debt_to_recurring_revenue_ratio_helper, axis=1)
        self.calculator_info.intermediate_calculation_dict['VAE'] = vae_df
        
    
    def calculate_vae(self):
        self.net_senior_leverage() # column 'L'
        self.net_total_leverage() # coluumn 'M'
        self.debt_to_recurring_revenue_ratio() # column 'P'
        print('calculation of sheet VAE is completed')