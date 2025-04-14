import pandas as pd
from datetime import datetime
import pickle
import json

from models import BaseDataFile
from source.services.PSSL.PsslDashboardService import PsslDashboardService

pssl_dashboard_service = PsslDashboardService()

def trigger_pssl_bb(bdi_id):
    path1 = 'PSSL_Base_Data.xlsx'
    base_data_dict = pd.read_excel(path1, sheet_name=None)

    user_id = 1, 
    file_name = path1, 
    closing_date = datetime.today()
    fund_type='PSSL', 
    pickled_base_data = pickle.dumps(base_data_dict)
    file_data = pickled_base_data
    # intermediate_calculation = pickled_base_data   # initially setting initermediate calculation as base data

    included_assets = base_data_dict['Portfolio']['Borrower'].tolist()
    excluded_assets = []
    included_excluded_assets_dict = {
        'included_assets': included_assets,
        'excluded_assets': excluded_assets
    }
    included_excluded_assets_map = json.dumps(included_excluded_assets_dict)

    base_data_file = BaseDataFile(
        user_id=user_id, 
        file_name=file_name, 
        closing_date=closing_date,
        fund_type=fund_type, 
        file_data=pickled_base_data,
        included_excluded_assets_map=included_excluded_assets_map
    )

    response = pssl_dashboard_service.get_bb_calculation(base_data_file, selected_assets=included_assets, user_id=user_id)
