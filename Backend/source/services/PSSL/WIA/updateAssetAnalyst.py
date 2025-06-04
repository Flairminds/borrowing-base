import pickle
import json
import copy

from source.services.PSSL.PsslBBCalculator import PsslBBCalculator
from source.services.PSSL.WIA.ResponseGenerator import PsslWiaResponseGenerator

from source.utility.ServiceResponse import ServiceResponse
from models import db 

class UpdateAssetAnalyst():

    @staticmethod
    def update_assset(base_data_file, modified_base_data_file):
        try:
            initial_base_data = pickle.loads(base_data_file.file_data)
            initial_intermediate_calculation = pickle.loads(base_data_file.intermediate_calculation)
            portfolio_df = initial_base_data["Portfolio"].copy(deep=True)
            included_assets = json.loads(base_data_file.included_excluded_assets_map)["included_assets"]
            portfolio_df = portfolio_df[portfolio_df["Borrower"].isin(included_assets)]
            initial_base_data["Portfolio"] = portfolio_df
            new_base_data = copy.deepcopy(initial_base_data)

            modified_data =  pickle.loads(modified_base_data_file.modified_data)

            for sheet in modified_data.keys():
                new_base_data[sheet] = modified_data[sheet]

            intermediate_metrics_data = {"initial_intermediate_metrics": None}

            pssl_bb_calculator = PsslBBCalculator(base_data_dict=initial_base_data, intermediate_calculation_dict=new_base_data, base_data_file=base_data_file)
            pssl_bb_calculator.calculate()
            calculated_intermediate_calculation = pssl_bb_calculator.intermediate_calculation_dict
            
            pssl_wia_res_generator = PsslWiaResponseGenerator(initial_xl_df_map=initial_intermediate_calculation, calculated_xl_df_map=calculated_intermediate_calculation)
            response_data = pssl_wia_res_generator.generate_response()

            modified_base_data_file.response = response_data
            modified_base_data_file.intermediate_metrics_data = intermediate_metrics_data
            modified_base_data_file.intermediate_calculation = pickle.dumps(calculated_intermediate_calculation)

            db.session.add(modified_base_data_file)
            db.session.commit()
            db.session.refresh(modified_base_data_file)

            return ServiceResponse.success(data=response_data)

        except Exception as e:
            raise Exception(e)