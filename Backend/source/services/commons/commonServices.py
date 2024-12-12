from models import BaseDataFile
import numpy as np
import pandas as pd
from source.utility.ServiceResponse import ServiceResponse

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


def get_raw_value(updated_value, col_type):
    try:
        if col_type == np.float64:
            if updated_value != "":
                if type(updated_value) == str:
                    updated_value = updated_value.replace(",", "")
                    updated_value = float(updated_value)
            else:
                updated_value = None
        if col_type == np.int64:
            if updated_value != "":
                if type(updated_value) == str:
                    updated_value = updated_value.replace(",", "")
                    updated_value = int(updated_value)
            else:
                updated_value = None
        elif col_type == "<M8[ns]":  # Handling datetime
            if updated_value != "":
                if type(updated_value) != str:
                    if find_is_NaT(updated_value):
                        updated_value = ""
                    else:
                        updated_value = pd.to_datetime(
                            updated_value, errors="coerce"
                        ).strftime("%Y-%m-%d")
            else:
                updated_value = None
        if col_type == object:
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
        return ServiceResponse.error(message=f"Error in get_raw_value: {e}")


def get_row_index(sheet_df, row_name):
    try:
        row_index = sheet_df[sheet_df[sheet_df.columns[0]] == row_name].index[0]
        return row_index
    except IndexError as ie:
        return -1
    
def find_is_NaT(previous_value):
    try:
        if pd.isna(previous_value):
            return True
    except Exception as e:
        return False


def get_updated_value(updated_value):
    if isinstance(updated_value, str):
        try:
            if updated_value.endswith("%"):
                updated_value = updated_value[:-1]
                updated_value = float(updated_value) / 100
        except ValueError:
            pass
    return updated_value

