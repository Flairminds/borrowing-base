from source.services.BBCalculator.BBCalculator import BorrowingBaseCalculator
from source.services.PSSL.calculation.portfolio_sheet.PorfolioCalculator import PortfolioCalculator
from source.services.PSSL.calculation.vae_sheet.VaeCalculator import VaeCalculator

class PsslBBCalculator(BorrowingBaseCalculator):
    def __init__(self, base_data_dict, intermediate_calculation_dict):
        super().__init__(base_data_dict, intermediate_calculation_dict)

    
    def calculate(self):
        vae_calculator = VaeCalculator(self)
        vae_calculator.calculate_vae()
        portfolio_calculator = PortfolioCalculator(self)
        portfolio_calculator.calculate_portfolio()
