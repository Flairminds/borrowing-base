import pandas as pd

from source.services import fundSetupService

class ConcentrationLimits:
    def __init__(self, calculator_info):
        self.calculator_info = calculator_info
        self.setup_conce_limit_df()

    def setup_conce_limit_df(self):
        service_response = fundSetupService.get_concentration_tests(fund_name='PSSL')
        concentration_tests_data = service_response.get("data")
        concentration_limit_df = pd.DataFrame(concentration_tests_data)
        self.calculator_info.intermediate_calculation_dict['Concentration Limits'] = concentration_limit_df


    def applicable_limit(self):
        # =MAX(H40*M$33,I40)

        def applicable_limit(row):
            limit_percentage = row["limit_percentage"] if row["limit_percentage"] != '' else 0
            min_limit = row["min_limit"] if not (row["min_limit"] != row["min_limit"]) else 0
            return max([limit_percentage * total_bb, min_limit])

        concentration_limit_df = self.calculator_info.intermediate_calculation_dict['Concentration Limits']
        porfolio_df = self.calculator_info.intermediate_calculation_dict['Portfolio']
        total_bb = porfolio_df["Adjusted Borrowing Value"].sum()
        concentration_limit_df["Applicable Limit"] = concentration_limit_df.apply(applicable_limit, axis=1)
        self.calculator_info.intermediate_calculation_dict['Concentration Limits'] = concentration_limit_df


    def calculate_concentration(self):
        self.applicable_limit() # concentration tests column 'J'