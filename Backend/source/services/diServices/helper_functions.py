import pandas as pd
from sqlalchemy import text
from models import db
from source.utility.ServiceResponse import ServiceResponse
from datetime import datetime
from datetime import datetime

def truncate_and_rename_columns(df):
    """
    Truncate column names to 63 characters and ensure uniqueness.
    """
    max_length = 63
    new_columns = []
    seen = set()
    
    for col in df.columns:
        # Truncate to max_length
        truncated_col = col[:max_length]
        
        # Ensure uniqueness
        unique_col = truncated_col
        counter = 1
        while unique_col in seen:
            unique_col = f"{truncated_col[:max_length - len(str(counter)) - 1]}_{counter}"
            counter += 1
        
        seen.add(unique_col)
        new_columns.append(unique_col)
    
    df.columns = new_columns
    return df

def process_and_store_data(data_dict, file_id, fund_name, engine):
    """Process each DataFrame and store it in the database."""
    for sheet_name, df in data_dict.items():
        print(f"Processing sheet: {sheet_name}")
        
        # Log duplicates for debugging
        # duplicates = df.columns[df.columns.duplicated()].tolist()
        # if duplicates:
        #     print(f"Duplicate columns in sheet {sheet_name}: {duplicates}")
        
        try:
            # Truncate and rename columns
            df = truncate_and_rename_columns(df)
            table_name = 'sf_sheet' + '_' + sheet_name.lower().replace(" ", "_")
            # Store in the database
            with engine.connect() as connection:
                data = pd.DataFrame(connection.execute(text(f'select * from {table_name} where source_file_id = :source_file_id limit 1'), {'source_file_id': file_id}).fetchall())
                if len(data) > 0:
                    continue
            with engine.connect() as connection:
                columns = connection.execute(text(f'''SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = :table_name'''), {'table_name': table_name}).fetchall()
            columns_list = []
            for column in columns:
                columns_list.append(column.column_name)
            drop_columns = []
            for column in df.columns:
                if column not in columns_list:
                    drop_columns.append(column)
            df=df.drop(columns=drop_columns)
            df.to_sql(table_name, con=engine, if_exists='append', index=False, method='multi')
            if table_name == 'sf_sheet_soi_mapping':
                # delete non-unique records from soi mapping
                with engine.connect() as connection:
                    data = connection.execute(text(f'DELETE FROM sf_sheet_soi_mapping a USING (SELECT MAX(ctid) as ctid, "SOI Name", "Security Name", "Security Type" FROM sf_sheet_soi_mapping GROUP BY ("SOI Name", "Security Name", "Security Type") HAVING COUNT(*) > 1) b WHERE (a."SOI Name" = b."SOI Name" AND a."Security Name" = b."Security Name" AND a."Security Type" = b."Security Type" AND a.ctid <> b.ctid) or a."Security Name" is null'))
                    connection.commit()
            print(f"Successfully stored sheet: {sheet_name}")
        except Exception as e:
            print(f"Failed to store sheet {sheet_name}")
            raise Exception(e)
            
def update_security_mapping(engine):
    try:
        with engine.connect() as connection:
            connection.execute(text(f'insert into pflt_security_mapping (company_id, soi_name, master_comp_security_name, family_name, security_type) select 1, "SOI Name", "Security Name", "Family Name", "Security Type" from sf_sheet_soi_mapping on conflict do nothing'))
            connection.commit()
        print("updated security mapping")
    except Exception as e:
        print(f"Failed to update security mapping")
        raise Exception(e)
    
def store_sheet_data(data_dict):
    engine = db.get_engine()

    """Process each DataFrame and store it in the database."""
    try:
        for sheet_name, df in data_dict.items():
            print(f"Processing sheet: {sheet_name}")

            df = truncate_and_rename_columns(df)
            if (sheet_name == "Market and Book Value Position_"):
                table_name = "sf_sheet_marketbook_1"
            else:
                table_name = 'sf_sheet' + '_' + sheet_name.lower().replace(" ", "_")

            with engine.connect() as connection:
                columns = connection.execute(text(f'''SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = :table_name'''), {'table_name': table_name}).fetchall()
            columns_list = []
            for column in columns:
                columns_list.append(column.column_name)
            drop_columns = []
            for column in df.columns:
                if column not in columns_list:
                    drop_columns.append(column)
            df=df.drop(columns=drop_columns)
            df.to_sql(table_name, con=engine, if_exists='append', index=False, method='multi')
            print(f"Successfully stored sheet: {sheet_name}")
                
        return ServiceResponse.success()
    except Exception as e:
        print(str(e))
        return ServiceResponse.error()
    

def check_data_type(value, data_type, exceptions=[]):
    data_type = data_type.lower()
    type_mapping = {
        'string': str,
        'float': float,
        'integer': int,
        'datetime': datetime
    }
    if value != value:
        return True
    check = isinstance(value, type_mapping[data_type])
    if data_type == 'float':
        if isinstance(value, int):
            check = True
    if value in exceptions:
        return True
    return check


def check_value_data_type(value, data_type):
    data_type = data_type.lower()
    if value != value:
        return True

    if value == "":
        return True
    

    try:
        if data_type == 'string':
            return isinstance(value, str)

        elif data_type == 'integer':
            if isinstance(value, int):
                return True
            return str(value).isdigit()

        elif data_type == 'float':
            float_val = float(value)
            return True

        elif data_type == 'datetime':
            if isinstance(value, datetime):
                return True
            datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ')
            return True

    except (ValueError, TypeError):
        return False

    return False 