import pandas as pd

class Availability:
    def __init__(self, calculator_info):
        self.calculator_info = calculator_info

    def get_pro_forma_advances_outstanding(self):
        # =L54-L55+L56
        availability_df = self.calculator_info.intermediate_calculation_dict['Availability']
        pro_forma_advances_outstanding_value = (availability_df.loc[availability_df['Terms'] == 'Current Advances Outstanding', 'Values'].values[0] + availability_df.loc[availability_df['Terms'] == 'Advances Repaid', 'Values'].values[0] + availability_df.loc[availability_df['Terms'] == 'Advances Requested', 'Values'].values[0])
        pro_forma_advances_outstanding_row = {"Terms": "Pro Forma Advances Outstanding", "Values": pro_forma_advances_outstanding_value}
        availability_df = availability_df.append(pro_forma_advances_outstanding_row, ignore_index=True)
    
        self.calculator_info.intermediate_calculation_dict['Availability'] = availability_df

    def get_adjusted_borrowing_value(self):
        availability_df = self.calculator_info.intermediate_calculation_dict['Availability']
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        total_bb = portfolio_df["Adjusted Borrowing Value"].sum()
        adjusted_borrowing_value_row = {"Terms": "Adjusted Borrowing Value", "Values": total_bb}

        availability_df = availability_df.append(adjusted_borrowing_value_row, ignore_index=True)
        self.calculator_info.intermediate_calculation_dict['Availability'] = availability_df

    def get_excess_conc_amount(self):
        availability_df = self.calculator_info.intermediate_calculation_dict['Availability']
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']

        excess_columns = [
            "First Lien Last Out, Second Lien Loan not in Top Three Obligors Excess", 
            "Top 3 Excess",
            "Largest Industry Excess",
            "Second Largest Industry Excess",
            "Third Largest Industry Excess",
            "Other Industries Excess",
            "EBITDA Less Than $10MM Excess",
            "DIP Loans Excess",
            "DDTL and Revolving Loans Excess",
            "Pay Less Frequently than Quarterly Excess",
            "Approved Foreign Currency Excess",
            "Approved Foreign Country Excess",
            "Cov-Lite Excess"
        ]

        excess_column_sum = portfolio_df[excess_columns].sum().sum()

        excess_concentration_amount_row = {"Terms": "Excess Concentration Amount", "Values": excess_column_sum}

        availability_df = availability_df.append(excess_concentration_amount_row, ignore_index=True)
        self.calculator_info.intermediate_calculation_dict['Availability'] = availability_df

    # L49
    def get_foreign_currency_adjusted_borrowing_value(self):
        # SUMIF(Portfolio!$BT$11:$BT$90,"<>USD",Portfolio!$W$11:$W$90)
        availability_df = self.calculator_info.intermediate_calculation_dict['Availability']
        portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        foreign_currency_adjusted_borrowing_value = portfolio_df.loc[portfolio_df['Approved Currency'] != 'USD', 'Adjusted Borrowing Value'].sum()

        foreign_currency_adjusted_borrowing_row = {"Terms": "Foreign Currency Adjusted Borrowing Value", "Values": foreign_currency_adjusted_borrowing_value}
        availability_df = availability_df.append(foreign_currency_adjusted_borrowing_row, ignore_index=True)
        self.calculator_info.intermediate_calculation_dict['Availability'] = availability_df

    # L35 =  0.03 * L51
    def get_approved_foreign_currency_reserve(self):
        availability_df = self.calculator_info.intermediate_calculation_dict['Availability']
        # L51 = L49 - L50
        foreign_currency_adjusted_borrowing_value = availability_df.loc[availability_df['Terms'] == 'Foreign Currency Adjusted Borrowing Value', 'Values'].values[0]
        foreign_currency_hedged_by_borrower = availability_df.loc[availability_df['Terms'] == 'Foreign Currency hedged by Borrower', 'Values'].values[0]
        unhedged_foreign_currency_value = 0.03 * (float(foreign_currency_adjusted_borrowing_value) - float(foreign_currency_hedged_by_borrower))
        
        unhedged_foreign_currency_row = {"Terms": "Approved Foreign Currency Reserve", "Values": unhedged_foreign_currency_value}
        availability_df = availability_df.append(unhedged_foreign_currency_row, ignore_index=True)
        self.calculator_info.intermediate_calculation_dict['Availability'] = availability_df

    def get_borrowing_base(self):
        # L36 = L33 - L34 - L35
        availability_df = self.calculator_info.intermediate_calculation_dict['Availability']
        def get_term_value(term_name):
            result = availability_df.loc[availability_df['Terms'] == term_name, 'Values']
            return float(result.values[0]) if not result.empty and pd.notna(result.values[0]) else 0.0

        adjusted_borrowing_value = get_term_value('Adjusted Borrowing Value')
        adjusted_borrowing_value_of_eligible_loans = get_term_value('Adjusted Borrowing Value of Eligible Loans')
        foreign_currency_adjusted_borrowing_value = get_term_value('Foreign Currency Adjusted Borrowing Value')

        borrowing_base_value = adjusted_borrowing_value - adjusted_borrowing_value_of_eligible_loans - foreign_currency_adjusted_borrowing_value

        borrowing_base_row = {
            "Terms": "Borrowing Base",
            "Values": borrowing_base_value
        }

        availability_df = availability_df.append(borrowing_base_row, ignore_index=True)
        self.calculator_info.intermediate_calculation_dict['Availability'] = availability_df


    def calculate_availability(self):
        self.get_adjusted_borrowing_value() # 'L33'
        self.get_pro_forma_advances_outstanding() # 'L57'
        self.get_foreign_currency_adjusted_borrowing_value() # 'L49'
        self.get_excess_conc_amount() # 'L34'
        self.get_approved_foreign_currency_reserve() # 'L35'
        self.get_borrowing_base() # 'L36'