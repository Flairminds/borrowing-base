import pickle
import copy
import json
from models import db

from source.services.PFLT.calculation.pflt_borrowing_base import (
    PFLTBorrowingBase as PBC,
)
from source.services.PFLT.WIA import responseGenerator

class UpdateAssetAnalyst():

    @staticmethod
    def update_assset(base_data_file, modified_base_data_file):
        initial_base_data = pickle.loads(base_data_file.file_data)
        loan_list_df = initial_base_data["Loan List"].copy(deep=True)

        included_assets = json.loads(base_data_file.included_excluded_assets_map)["included_assets"]
        loan_list_df = loan_list_df[loan_list_df["Security Name"].isin(included_assets)]
        # initial_loan_list_df = loan_list_df.copy(deep=True)
        initial_base_data["Loan List"] = loan_list_df

        new_base_data = copy.deepcopy(initial_base_data)

        modified_data =  pickle.loads(modified_base_data_file.modified_data)

        for sheet in modified_data.keys():
            new_base_data[sheet] = modified_data[sheet]

        # intermediate_calculation = pickle.loads(base_data_file.intermediate_calculation)
        intermediate_metrics_data = {"initial_intermediate_metrics": None}

        pbc = PBC(file_df=new_base_data)
        pbc.calculate()

        intermediate_metrics_data["modified_intermediate_metrics"] = None

        initial_xl_df_map = pickle.loads(base_data_file.intermediate_calculation)

        calculated_xl_df_map = pbc.file_df
        response_data = responseGenerator.generateResponse(
            initial_xl_df_map, calculated_xl_df_map
        )

        modified_base_data_file.response = response_data
        modified_base_data_file.intermediate_metrics_data = intermediate_metrics_data

        db.session.add(modified_base_data_file)
        db.session.commit()
        db.session.refresh(modified_base_data_file)

        return response_data
