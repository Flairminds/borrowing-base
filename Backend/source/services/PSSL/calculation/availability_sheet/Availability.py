class Availability:
    def __init__(self, calculator_info):
        self.calculator_info = calculator_info

    def pro_forma_advances_outstanding(self):
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

    # def excess_conc_amount(self):
    #     availability_df = self.calculator_info.intermediate_calculation_dict['Availability']
    #     portfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']

    #     exess_columns = ["First Lien Last Out, Second Lien Loan not in Top Three Obligors Excess", "Top 3 Excess"]
        

    def calculate_availability(self):
        self.get_adjusted_borrowing_value() # 'L33'
        self.pro_forma_advances_outstanding() # 'L57'
        # self.excess_conc_amount()
        