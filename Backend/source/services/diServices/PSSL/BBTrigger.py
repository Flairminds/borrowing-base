import pandas as pd
from datetime import datetime
import pickle
import json
from sqlalchemy import text

from models import db, BaseDataFile
from source.services.PSSL.pssl_calculation_initiator import PsslCalculationInitiator
from source.utility.ServiceResponse import ServiceResponse
from models import db, ExtractedBaseDataInfo
from source.utility.Log import Log
pssl_calculation_initiator = PsslCalculationInitiator()

def trigger_pssl_bb(bdi_id):
    try:
        engine = db.get_engine()
        extracted_base_data_info = ExtractedBaseDataInfo.query.filter_by(id=bdi_id).first()
        with engine.connect() as connection:
            base_data_df = pd.DataFrame(connection.execute(text(f"select * from pssl_base_data where base_data_info_id = :ebd_id"), {'ebd_id': bdi_id}).fetchall())
            base_data_mapping_df = pd.DataFrame(connection.execute(text("""select bd_sheet_name, bd_column_name, bd_column_lookup from base_data_mapping bdm where fund_type = 'PSSL' and bd_sheet_name = 'Portfolio'""")))

        rename_df_col = {}
        for index, row in base_data_mapping_df.iterrows():
            rename_df_col[row['bd_column_lookup']] = row['bd_column_name']
        base_data_df.rename(columns=rename_df_col, inplace=True)

        base_data_df["Admin Agent Approval (RCF)"] = "No"
        base_data_df["Admin Agent Add-Back Discretion"] = "N"
        base_data_df["Admin Agent Approved Add-Backs"] = 0
        base_data_df["Date of Financial Delivery VAE"] = None
        base_data_df["Date Financials Provided to Ally"] = None
        base_data_df["Current Cash Interest Expense"] = 1
        # datatype of following columns should get handled in query itself
        base_data_df["RCF Update Date"] = pd.to_datetime(base_data_df["RCF Update Date"])
        base_data_df['Borrower Outstanding Principal Balance'] = pd.to_numeric(base_data_df['Borrower Outstanding Principal Balance'], errors='coerce')

        path1 = 'PSSL_Base_Data.xlsx'
        base_data_dict = pd.read_excel(path1, sheet_name=None)
        base_data_dict["Portfolio"] = base_data_df

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
            included_excluded_assets_map=included_excluded_assets_map,
            extracted_base_data_info_id = bdi_id
        )
        db.session.add(base_data_file)
        db.session.commit()
        db.session.refresh(base_data_file)

        bb_response = pssl_calculation_initiator.get_bb_calculation(base_data_file, selected_assets=included_assets, user_id=user_id)

        base_data_file.response = pickle.dumps(bb_response)

        return ServiceResponse.success(message="Successfully processed calculation.", data=bb_response)
    except Exception as e:
        Log.func_error(e=e)
        return ServiceResponse.error(message="Calculation failed.")