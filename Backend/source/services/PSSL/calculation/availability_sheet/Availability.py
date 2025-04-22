class Availability:
    def __init__(self, calculator_info):
        self.calculator_info = calculator_info

    def pro_forma_advances_outstanding(self):
        # =L54-L55+L56
        availability_df = self.calculator_info.intermediate_calculation_dict['Availability']

        availability_df["Pro Forma Advances Outstanding"] = (availability_df.loc[availability_df['Terms'] == 'Current Advances Outstanding', 'Values'].values[0] + availability_df.loc[availability_df['Terms'] == 'Advances Repaid', 'Values'].values[0] + availability_df.loc[availability_df['Terms'] == 'Advances Requested', 'Values'].values[0])
    
        self.calculator_info.intermediate_calculation_dict['Availability'] = availability_df

    def calculate_availability(self):
        self.pro_forma_advances_outstanding() # 'L57'
        