import pickle
import copy
import json
from flask import jsonify

from models import db
from source.services.PFLT.calculation.pflt_borrowing_base import (
    PFLTBorrowingBase as PBC,
)
from source.services.PFLT.pflt_utility.constants import sheet_uniques


class PfltBBCalculator:
    def get_bb_calculation(self, base_data_file, selected_assets, user_id):
        xl_sheet_df_map = pickle.loads(base_data_file.file_data)
        PFLT_xl_sheet_df_map = copy.deepcopy(xl_sheet_df_map)
        loan_list_df = PFLT_xl_sheet_df_map["Loan List"]

        included_excluded_assets_map = {}
        excluded_assets = list(
            set(loan_list_df[sheet_uniques["Loan List"]].tolist())
            - set(selected_assets)
        )
        included_excluded_assets_map["included_assets"] = selected_assets
        included_excluded_assets_map["excluded_assets"] = excluded_assets

        selected_assets_mask = loan_list_df[sheet_uniques["Loan List"]].isin(
            selected_assets
        )

        loan_list_df = loan_list_df[selected_assets_mask].reset_index(drop=True)
        PFLT_xl_sheet_df_map["Loan List"] = loan_list_df
        pbc = PBC(file_df=PFLT_xl_sheet_df_map)
        pbc.calculate()

        # save into the session
        # session["PFLT_file_df"] = pbc.file_df
        intermediate_calculation = pbc.file_df
        # intermediate_calculations
        pickled_intermediate_calculation = pickle.dumps(intermediate_calculation)
        base_data_file.intermediate_calculation = pickled_intermediate_calculation

        # generate response
        response_data = pbc.generate_response()
        # upsert pickled_response_data
        pickled_response_data = pickle.dumps(response_data)
        base_data_file.response = pickled_response_data

        json_include_exclude_map = json.dumps(included_excluded_assets_map)
        base_data_file.included_excluded_assets_map = json_include_exclude_map
        response_data["closing_date"] = base_data_file.closing_date.strftime("%Y-%m-%d")

        response_data["fund_type"] = base_data_file.fund_type
        # update base_data_file object
        db.session.add(base_data_file)
        db.session.commit()
        return response_data
