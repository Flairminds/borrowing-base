import pickle
import copy

from models import db
from source.services.sheetUniques import sheet_uniques
from source.services.PSSL.PsslBBCalculator import PsslBBCalculator

class PsslCalculationInitiator:
    def get_bb_calculation(sef, base_data_file, selected_assets, user_id):
        base_data_dict = pickle.loads(base_data_file.file_data)
        intermediate_calculation_dict = copy.deepcopy(base_data_dict)

        portfolio_df = base_data_dict['Portfolio']
        portfolio_df_copy = portfolio_df.copy(deep=True)
        selected_assets_mask = portfolio_df_copy[sheet_uniques["Portfolio"]].isin(selected_assets)
        portfolio_df_copy = portfolio_df_copy[selected_assets_mask].reset_index(drop=True)
        intermediate_calculation_dict["Portfolio"] = portfolio_df_copy

        pssl_bb_calculator = PsslBBCalculator(base_data_dict, intermediate_calculation_dict, base_data_file)
        pssl_bb_calculator.calculate()
        response = pssl_bb_calculator.generate_response()
        pickled_res = pickle.dumps(response)

        intermediate_calculation = pssl_bb_calculator.intermediate_calculation_dict
        pickled_intermediate_calculation = pickle.dumps(intermediate_calculation)

        base_data_file.intermediate_calculation = pickled_intermediate_calculation
        base_data_file.response = pickled_res

        db.session.add(base_data_file)
        db.session.commit()

        return response