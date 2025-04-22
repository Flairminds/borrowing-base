class BorrowingBaseCalculator:
    def __init__(self, base_data_dict, intermediate_calculation_dict, base_data_file, fund_name):
            self.base_data_dict = base_data_dict
            self.intermediate_calculation_dict = intermediate_calculation_dict
            self.fund_name = fund_name
            self.base_data_file = base_data_file


    def calculate(self):
        print(f"Calculation for {self.fund_name} fund is not available")

    def generate_response(self):
        print(f"Response generation for {self.fund_name} fund is not available")