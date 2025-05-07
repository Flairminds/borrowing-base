from source.services.BBCalculator.BBCalculator import BorrowingBaseCalculator
from source.services.PSSL.calculation.portfolio_sheet.PorfolioCalculator import PortfolioCalculator
from source.services.PSSL.calculation.vae_sheet.VaeCalculator import VaeCalculator
from source.services.PSSL.calculation.PsslResponseGenerator import PsslResponseGenerator
from source.services.PSSL.calculation.availability_sheet.Availability import Availability
from source.services.PSSL.calculation.concentrations_limits_sheet.ConcentrationLimits import ConcentrationLimits
class PsslBBCalculator(BorrowingBaseCalculator):
    def __init__(self, base_data_dict, intermediate_calculation_dict, base_data_file):
        super().__init__(base_data_dict, intermediate_calculation_dict, base_data_file, fund_name="PSSL")
        

    
    def calculate(self):
        vae_calculator = VaeCalculator(self)
        vae_calculator.calculate_vae()
        portfolio_calculator = PortfolioCalculator(self)
        portfolio_calculator.calculate_portfolio()
        # conc_limits = ConcentrationLimits(self)
        # conc_limits.calculate_concentration()
        availability_calculator = Availability(self)
        availability_calculator.calculate_availability()

    def generate_response(self):
        pssl_response_generator = PsslResponseGenerator(self)
        response = pssl_response_generator.generate_response()
        return response
