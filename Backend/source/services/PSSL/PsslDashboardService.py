import pickle
import copy

from source.services.sheetUniques import sheet_uniques
from source.services.PSSL.PsslBBCalculator import PsslBBCalculator

class PsslDashboardService:
    def get_bb_calculation(self, base_data_file, selected_assets, user_id):
        base_data_dict = pickle.loads(base_data_file.file_data)
        intermediate_calculation_dict = copy.deepcopy(base_data_dict)

        portfolio_df = base_data_dict['Portfolio']
        portfolio_df_copy = portfolio_df.copy(deep=True)
        selected_assets_mask = portfolio_df_copy[sheet_uniques["Portfolio"]].isin(selected_assets)
        portfolio_df_copy = portfolio_df_copy[selected_assets_mask].reset_index(drop=True)
        intermediate_calculation_dict["Portfolio"] = portfolio_df_copy

        pssl_bb_calculator = PsslBBCalculator(base_data_dict, intermediate_calculation_dict)
        pssl_bb_calculator.calculate()
        