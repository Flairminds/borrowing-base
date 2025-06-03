from models import BaseDataFile, WhatIfAnalysis, ModifiedBaseDataFile, db
from source.utility.ServiceResponse import ServiceResponse

import numpy as np
import pandas as pd
from datetime import datetime

from source.utility.ServiceResponse import ServiceResponse
from models import ModifiedBaseDataFile, BaseDataFile

def get_base_data_file(**kwargs):
    if "base_data_file_id" in kwargs.keys():
        base_data_file_id = kwargs["base_data_file_id"]
        base_data_file = BaseDataFile.query.filter_by(id=base_data_file_id).first()
    else:
        user_id = kwargs["user_id"]
        if "closing_date" not in kwargs.keys():
            base_data_file = (
                BaseDataFile.query.filter_by(user_id=user_id)
                .order_by(BaseDataFile.closing_date.desc())
                .first()
            )
        else:
            closing_date = kwargs["closing_date"]
            base_data_file = BaseDataFile.query.filter_by(
                closing_date=closing_date, user_id=user_id
            ).first()
    return base_data_file

def get_fundType_of_wia(what_if_analysis_id, what_if_analysis_type):

    if what_if_analysis_type == "Update asset":
        fund_type = (
            db.session
            .query(BaseDataFile.fund_type)
            .join(ModifiedBaseDataFile, ModifiedBaseDataFile.base_data_file_id == BaseDataFile.id)
            .filter(ModifiedBaseDataFile.id == what_if_analysis_id, ModifiedBaseDataFile.simulation_type == what_if_analysis_type)
            .first()
        )
    else:
        fund_type = (
            db.session
            .query(BaseDataFile.fund_type)
            .join(WhatIfAnalysis, WhatIfAnalysis.base_data_file_id == BaseDataFile.id)
            .filter(WhatIfAnalysis.id == what_if_analysis_id, WhatIfAnalysis.simulation_type == what_if_analysis_type)
            .first()
        )

    if not fund_type:
        return ServiceResponse.error(message="What if analysis with given data not found")
    
    fund_type = fund_type[0]

    return ServiceResponse.success(data=fund_type, message="Base data file fund for WIA fetched")

def get_raw_value(updated_value, col_type):
  
    try:
        match col_type:
            case np.int64:
                if type(updated_value) == str:
                    if updated_value != "":
                        updated_value = float(updated_value.replace(",", ""))
                    else:
                        updated_value = None    
                else:
                    if updated_value != updated_value:
                        updated_value = 0
                    updated_value = int(updated_value)

            case np.float64:
                if type(updated_value) == str:
                    if updated_value != "":
                        updated_value = float(updated_value.replace(",", ""))
                    else:
                        updated_value = None   
                else:
                    updated_value = float(updated_value)

            case "<M8[ns]":
                if type(updated_value) == str:
                    if find_is_NaT(updated_value):
                        updated_value = None
                    else:
                        updated_value = pd.to_datetime(updated_value, format="%Y-%m-%d", errors="coerce")
                elif type(updated_value) == pd._libs.tslibs.nattype.NaTType:
                    updated_value = updated_value
                else:
                    updated_value = datetime.strptime(updated_value, "%Y-%m-%d").date()
            
            case object:
                try:
                    if not pd.isna(updated_value):
                        if updated_value != "":
                            updated_value = float(updated_value.replace(",", ""))
                        else:
                            updated_value = None
                    else:
                        updated_value = ""
                except ValueError:
                    updated_value = updated_value

        
        return updated_value
    
    except Exception as e:
        raise Exception(e)


def get_row_index(sheet_df, row_name, sheet_uniques_name):
    try:
        row_index = sheet_df[sheet_df[sheet_uniques_name] == row_name].index[0]
        return row_index
    except IndexError as ie:
        return -1
    
def find_is_NaT(previous_value):
    try:
        if pd.isna(previous_value):
            return True
    except Exception as e:
        return False


def get_updated_value(prev_value, updated_value):
    if isinstance(updated_value, str) and isinstance(prev_value, str):
        try:
            if  prev_value.endswith("%") or updated_value.endswith("%"):
                updated_value = updated_value.replace("%", "")
                updated_value = float(updated_value) / 100
        except ValueError:
            pass
    return updated_value

def validate_request_data(data):
    modified_base_data_file_id = data.get("modified_base_data_file_id")
    if not modified_base_data_file_id:
        return ServiceResponse.error(message="modified_base_data_file_id is required")

    modified_base_data_file = ModifiedBaseDataFile.query.filter_by(id=modified_base_data_file_id).first()

    if not modified_base_data_file:
        return ServiceResponse.error(message="No modified_base_data_file found")
    
    return ServiceResponse.success(data = modified_base_data_file)

def get_xl_df_map(excel_file):
    xl_df_map = pd.read_excel(excel_file, sheet_name=None)
    return xl_df_map