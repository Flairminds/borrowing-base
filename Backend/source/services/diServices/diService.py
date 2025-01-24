from azure.core.exceptions import ResourceExistsError
import os
import mmap
from io import BytesIO
import pandas as pd
from datetime import datetime
import pytz
# import azure.functions as func
from sqlalchemy import text
import threading
import numpy as np
from numerize import numerize
from openpyxl import load_workbook
import openpyxl
import pickle
import json
from datetime import datetime

from source.services.commons import commonServices
from source.app_configs import azureConfig
from source.utility.ServiceResponse import ServiceResponse
from source.utility.Log import Log
from models import SourceFiles, Users, db, ExtractedBaseDataInfo, PfltBaseData, PfltBaseDataHistory, PfltBaseDataMapping, PfltSecurityMapping, BaseDataMappingColumnInfo, BaseDataFile, PfltBaseDataOtherInfo
from source.services.diServices import helper_functions
from source.services.diServices import base_data_mapping
from source.services.PFLT.PfltDashboardService import PfltDashboardService

pfltDashboardService = PfltDashboardService()

def upload_src_file_to_az_storage(files, report_date, fund_type):
    if len(files) == 0:
        return ServiceResponse.error(message = "Please select files.", status_code = 400)
    if not fund_type:
        return ServiceResponse.error(message = "Please select Fund.", status_code = 400)
    
    blob_service_client, blob_client = azureConfig.get_az_service_blob_client()
    company_name = "Pennant"
    fund_names = fund_type
    report_date = datetime.strptime(report_date, "%Y-%m-%d").date()

    source_files_list = []
    try:
        for file in files:
            print(file.filename)
            for fund_name in fund_names:
                blob_name = f"{company_name}/{fund_name}/{file.filename}"
                
                # setting SourceFiles object
                file_name = os.path.splitext(file.filename)[0]
                extension = os.path.splitext(file.filename)[1]
                file.seek(0, 2)  # Move to the end of the file
                file_size = file.tell()  # Get the size in bytes
                file.seek(0)
                company_id = 1
                is_validated = False
                is_extracted = False
                uploaded_by = 1
                file_type = None
                if contains_cash(file.filename):
                    file_type = "cashfile"
                if contains_master_comp(file.filename):
                    file_type = "master_comp"

                # upload blob in container
                blob_client.upload_blob(name=blob_name, data=file)
                file_url = blob_client.url + '/' + blob_name
                # add details of files in db
            source_file = SourceFiles(file_name=file_name, extension=extension, report_date=report_date, file_url=file_url, file_size=file_size, company_id=company_id, fund_types=fund_names, is_validated=is_validated, is_extracted=is_extracted, uploaded_by=uploaded_by, file_type=file_type)

            db.session.add(source_file)
            db.session.commit()
                    # source_files.append(source_file)
                # try:
        #         #     db.session.add_all(source_files)
        #         #     db.session.commit()
        #         # except Exception as e:
        #         #     Log.func_error(e=e)
        #         #     return ServiceResponse.error(message="Could not save files to database.", status_code = 500)

        # for file in files:
        #     for fund_name in fund_names:
        #         blob_name = f"{company_name}/{fund_name}/{file.filename}"
                
        #         # setting SourceFiles object
        #         file_name = os.path.splitext(file.filename)[0]
        #         extension = os.path.splitext(file.filename)[1]
        #         file.seek(0, 2)  # Move to the end of the file
        #         file_size = file.tell()  # Get the size in bytes
        #         file.seek(0)
        #         company_id = 1
        #         is_validated = False
        #         is_extracted = False
        #         uploaded_by = 1
        #         file_type = None
        #         if contains_cash(file.filename):
        #             file_type = "cashfile"
        #         if contains_master_comp(file.filename):
        #             file_type = "master_comp"

        #         # upload blob in container
        #         blob_client.upload_blob(name=blob_name, data=file)
        #         file_url = blob_client.url + '/' + blob_name
        #         # add details of files in db
        #         source_file = SourceFile(file_name=file_name, extension=extension, report_date=report_date, file_url=file_url, file_size=file_size, company_id=company_id, is_validated=is_validated, is_extracted=is_extracted, uploaded_by=uploaded_by, file_type=file_type)

        #         db.session.add(source_file)
        #         db.session.commit()
        #         db.session.refresh(source_file)
        #         source_file_fund = SourceFileFund(sf_id=source_file.id, fund_type=fund_name)
        #         db.session.add(source_file_fund)
        #         db.session.commit()
        #         source_files_list.append(source_file)

        # for fund_name in fund_names:
        #     for uploaded_file in source_file:
        #         source_file_fund = SourceFileFund(sf_id=uploaded_file.id, fund_type=fund_name)
        #         db.session.add(source_file_fund)
        #         db.session.commit()
            
        return ServiceResponse.success(message = "Files uploaded successfully")

    except ResourceExistsError as ree:
        Log.func_error(e=ree)
        return ServiceResponse.error(message="Files with same name already exist.", status_code=409)
    except Exception as e:
        Log.func_error(e=e)
        return ServiceResponse.error(message="Could not upload files.", status_code = 500)
    
def get_blob_list(fund_type):
    company_id = 1 # for Penennt

    # If fund type is not provided -> fetching all records 
    source_files_query = db.session.query(
            SourceFiles.id,
            SourceFiles.file_name,
            SourceFiles.extension,
            SourceFiles.uploaded_at,
            SourceFiles.uploaded_by,
            SourceFiles.fund_types,
            SourceFiles.file_type,
            SourceFiles.report_date,
            Users.display_name
        ).join(Users, Users.user_id == SourceFiles.uploaded_by).filter(SourceFiles.is_deleted == False, SourceFiles.company_id == company_id, SourceFiles.is_archived == False)
    
    if fund_type:
        source_files_query = source_files_query.filter(SourceFiles.fund_types.any(fund_type))

    source_files = source_files_query.order_by(SourceFiles.uploaded_at.desc()).all()

    list_table = {
        "columns": [{
            "key": "fund", 
            "label": "Fund",
        }, {
            "key": "file_name", 
            "label": "File Name",
        }, {
            "key": "report_date", 
            "label": "Report Date",
        }, {
            "key": "uploaded_at", 
            "label": "Uploaded at",
        }, {
            "key": "uploaded_by", 
            "label": "Uploaded by",
        }], 
        "data": []
    }

    for source_file in source_files:
        list_table["data"].append({
            "file_id": source_file.id,
            "file_name": source_file.file_name + source_file.extension, 
            "uploaded_at": source_file.uploaded_at.strftime("%Y-%m-%d"),
            "report_date": source_file.report_date.strftime("%Y-%m-%d"),
            "fund": source_file.fund_types,
            "source_file_type": source_file.file_type,
            "uploaded_by": source_file.display_name
        })
        print(source_file.fund_types)
    
    return ServiceResponse.success(data=list_table)

def contains_cash(string):
    return "cash" in string.lower()

def contains_master_comp(string):
    return "master" in string.lower()

def get_data(blob_data, sheet_name, output_file_name, args):
    try:
        # container_client = blob_service_client.get_container_client('on-pepper')
        # blob_client = container_client.get_blob_client(file_path)
        # blob_data = blob_client.download_blob().readall()
        df = pd.read_excel(blob_data, sheet_name=sheet_name)
        for name in args:
            if df.eq(name).any(axis=1).any():
                first_occurrence_index = df.eq(name).any(axis=1).idxmax()
            else:
                first_occurrence_index = None 
            if first_occurrence_index is None:
                continue
            else:
                break
        if first_occurrence_index is None:
            return {"success_status": False, "error": "No such column found", "dataframe": None}
        
        new_df = df.loc[first_occurrence_index + 1:].reset_index(drop=True)
        new_df.columns = df.loc[first_occurrence_index]
        return {"success_status": True, "error": None, "dataframe": new_df}
    except Exception as e:
        return {"success_status": False, "error": str(e), "dataframe": None}

def update_column_names(df, sheet_name, sheet_column_mapper):
    column_level_map = sheet_column_mapper[sheet_name]
    columns = []
    
    for index, column in enumerate(df.columns):
        column_initials = ""
        for heading in list(column_level_map.keys()):
            if index in range(column_level_map[heading][1], column_level_map[heading][2]):
                column_initials = column_initials + "[" + "".join(word[0].upper() for word in heading.split()) + "] "
        column_name = column_initials + str(column)
        columns.append(column_name.strip())

    df.columns = columns
    df = df.round(3)
    return df

def extract(file_sheet_map, sheet_column_mapper, args):
    extrcted_df = {}
    updated_column_df = {}

    for file in file_sheet_map.keys():
        blob_data = file_sheet_map[file]["file"]
        sheets = file_sheet_map[file]["sheets"]
        source_file = file_sheet_map[file]["source_file_obj"]
        if not file_sheet_map[file]["is_extracted"]:
            for sheet in sheets:
                column_level_map = sheet_column_mapper[sheet]
                df_result = get_data(blob_data, sheet, column_level_map, args)
                if df_result["success_status"] is True:
                    extrcted_df[sheet] = df_result["dataframe"]
                    extracted_df = df_result["dataframe"].copy(deep=True)
                    updated_col_df = update_column_names(extracted_df, sheet, sheet_column_mapper)
                    updated_col_df["source_file_id"] = source_file.id
                    updated_column_df[sheet] = updated_col_df
                print(sheet + ' extracted')
    return updated_column_df

def extract_and_store(file_ids, sheet_column_mapper, extracted_base_data_info):
    from app import app
    with app.app_context():
        try:
            engine = db.get_engine()
            start_time = datetime.now()
            company_name = "Pennant"
            fund_name = "PFLT"
            FOLDER_PATH = company_name + '/' + fund_name + '/'
        
            blob_service_client, blob_client = azureConfig.get_az_service_blob_client()

            start_time = datetime.now()

            company_id = None
            report_date = None
            new_source_file = False
            cash_file_details = None
            master_comp_file_details = None
            file_sheet_map = None

            for file_id in file_ids:
                file_details = SourceFiles.query.filter_by(id=file_id).first()
                company_id = file_details.company_id
                report_date = file_details.report_date
                file_name = file_details.file_name + file_details.extension
                file = BytesIO(blob_client.get_blob_client(FOLDER_PATH + file_name).download_blob().readall())
                file_type = file_details.file_type
                if (file_type == 'cashfile'):
                    cash_file_details = file_details
                    file_sheet_map = {
                        "cash": {
                            "file": file,
                            "source_file_obj": file_details,
                            "sheets": ["US Bank Holdings", "Client Holdings"], 
                            "is_extracted": file_details.is_extracted
                        }
                    }
                elif file_type == 'master_comp':
                    master_comp_file_details = file_details
                    file_sheet_map = {
                        "master_comp": {
                            "file": file,
                            "source_file_obj": file_details,
                            "sheets": ["Borrower Stats", "Securities Stats", "PFLT Borrowing Base"],
                            "is_extracted": file_details.is_extracted
                        }
                    }
                if file_details.is_extracted:
                    continue
                args = ['Company', "Security", "CUSIP", "Asset ID", "SOI Name"]
                data_dict = extract(file_sheet_map, sheet_column_mapper, args)
                process_store_status = helper_functions.process_and_store_data(data_dict, file_id, fund_name, engine)
                file_details.is_extracted = True
                db.session.add(file_details)
                db.session.commit()
                new_source_file = True

            # if new_source_file:
            if not cash_file_details or not master_comp_file_details:
                raise Exception('Proper files not selected.')
            base_data_mapping.soi_mapping(engine, extracted_base_data_info, master_comp_file_details, cash_file_details)
            extracted_base_data_info.status = "completed"
            # else:
                # extracted_base_data_info.status = "repeated"
            
            db.session.add(extracted_base_data_info)
            db.session.commit()
            end_time = datetime.now()
            time_difference = (end_time - start_time).total_seconds() * 10**3
            print('successfully stored base data')
        except Exception as e:
            Log.func_error(e)
            extracted_base_data_info.status = "failed"
            extracted_base_data_info.failure_comments = str(e)
            db.session.add(extracted_base_data_info)
            db.session.commit()

def extract_base_data(file_ids):
    base_data_info_id = None
    try:
    # initialization
        borrower_stats_column_level_map = {
            "Current Metrics": (0, 9, 52),
            "At Close Metrics": (0, 52, 79),
            "Fund": (1, 2, 9),
            "Capital Structure": (1, 9, 23),
            "Reporting": (1, 23, 32),
            "For PSCF-Lev & PSSL": (1, 32, 33),
            "L3M / Quarterly": (1, 33, 37),
            "YTD": (1, 37, 41),
            "Current Leverage Stats Output": (1, 41, 52),
            "Comps Other Inputs / Leverage Calcs": (1, 52, 58),
            "Comps - At Close Metrics (Hardcode at close)": (1, 58, 72),
            "Pricing": (1, 72, 79)
        }

        security_stats = {
            "Banks": (0, 3, 9),
            "Security Information": (0, 10, 30),
            "PCOF Specific Metrics": (0, 31, 39),
            "Current": (0, 75, 81),
            "At Close": (0, 81, 91),
            "L3M / Quarterly": (0, 91, 95),
            "YTD": (0, 95, 99)
        }

        SOI_Mapping = {
            "General": (0, 1, 5),
            "For Dropdown": (0, 6, 7)
        }

        sheet_column_mapper = {
            "Borrower Stats": borrower_stats_column_level_map,
            "Securities Stats": security_stats,
            "US Bank Holdings": {},
            "Client Holdings": {},
            "SOI Mapping": SOI_Mapping,
            "PFLT Borrowing Base": {}
        }
        #--------------------------------
        if len(file_ids) == 0:
            return ServiceResponse.error(message='No files selected.')
        ini_file = SourceFiles.query.filter_by(id = file_ids[0]).first()
        report_date = ini_file.report_date
        company_id = ini_file.company_id
        extracted_base_data_info = ExtractedBaseDataInfo(report_date=report_date, fund_type="PFLT", status="in progress", company_id = 1, files = file_ids)
        db.session.add(extracted_base_data_info)
        db.session.commit()
        db.session.refresh(extracted_base_data_info)
        base_data_info_id = extracted_base_data_info.id

        threading.Thread(target=extract_and_store, kwargs={
            'file_ids': file_ids,
            'sheet_column_mapper': sheet_column_mapper,
            'extracted_base_data_info': extracted_base_data_info}
        ).start()

        # extract_and_store(file_ids = file_ids, sheet_column_mapper = sheet_column_mapper, extracted_base_data_info = extracted_base_data_info)

        response_data = {
            "id": extracted_base_data_info.id,
            "report_date": report_date.strftime("%Y-%m-%d"),
            "company_id": company_id
        }
        # put this following code in above function
        return ServiceResponse.success(message="Base Data extraction might take few minutes", data=response_data)
    except Exception as e:
        Log.func_error(e)
        if base_data_info_id:
            extracted_base_data_info = ExtractedBaseDataInfo.query.filter_by(id = base_data_info_id).first()
            extracted_base_data_info.status = 'failed'
            extracted_base_data_info.failure_comments = str(e)
            db.session.add(extracted_base_data_info)
            db.session.commit()
        return ServiceResponse.error(message='Extraction failed')


def get_base_data(info_id):
    # datetime_obj = datetime.strptime(report_date, "%Y-%m-%d")
    base_data = PfltBaseData.query.filter_by(base_data_info_id = info_id).order_by(PfltBaseData.id).all()
    base_data_info = ExtractedBaseDataInfo.query.filter_by(id = info_id).first()
    base_data_mapping = db.session.query(
        PfltBaseDataMapping.bdm_id,
        PfltBaseDataMapping.bd_column_lookup,
        PfltBaseDataMapping.bd_column_name,
        PfltBaseDataMapping.is_editable,
        BaseDataMappingColumnInfo.sequence,
        BaseDataMappingColumnInfo.is_selected
    ).join(PfltBaseDataMapping, PfltBaseDataMapping.bdm_id == BaseDataMappingColumnInfo.bdm_id).order_by(BaseDataMappingColumnInfo.sequence).all()

    engine = db.get_engine()

    with engine.connect() as connection:
        result = connection.execute(text('''
            select count(distinct pbd.obligor_name) as no_of_obligors, 
                    count(distinct pbd.security_name) as no_of_assets, 
                    sum(pbd.total_commitment::float) as total_commitment, 
                    sum(pbd.outstanding_principal::float) as total_outstanding_balance 
            from pflt_base_data pbd 
            where pbd.base_data_info_id = :info_id'''), {'info_id': info_id}).fetchall()

    no_of_obligors, no_of_assets, total_commitment, total_outstanding_balance = result[0]

    temp = []
    # print(base_data[0])
    for b in base_data:
        t = b.__dict__
        del t['_sa_instance_state']
        old_data = PfltBaseDataHistory.query.filter_by(id = b.id).order_by(PfltBaseDataHistory.done_at.desc()).offset(1).limit(1).first()
        t1 = None
        if old_data:
            t1 = old_data.__dict__
        for key in t:
            val = t[key]
            old_value = val
            if t1 and t1[key] != t[key]:
                old_value = t1[key]
            numerized_val = None
            if isinstance(val, (int, float, complex)) and not isinstance(val, bool):
                numerized_val = numerize.numerize(val, 2)
                # t[key] = val
            elif isinstance(val, str):
                if val.replace(".", "").replace("-", "").isnumeric():
                    try:
                        numerized_val = numerize.numerize(float(val), 2)
                    except Exception as e:
                        print(e, val, type(val))
                    # t[key] = val
            t[key] = {
                "meta_info": True,
                "value": val,
                "display_value": numerized_val if numerized_val else val,
                "title": val,
                "data_type": None,
                "unit": None,
                "old_value": old_value
            }
        # t['report_date'] = t['report_date'].strftime("%Y-%m-%d")
        # t['created_at'] = t['created_at'].strftime("%Y-%m-%d")
        temp.append(t)
    # print(temp[0])
    base_data_table = {
        "columns": [{
                "key": column.bd_column_lookup,
                "label": column.bd_column_name,
                "isEditable": column.is_editable,
                "bdm_id": column.bdm_id,
                "is_selected": column.is_selected
            } for column in base_data_mapping],
        "data": temp
    }

    # print(type(base_data_table))
    
    
    # for index, row in base_data.iterrows():
    #     row_data = {}
        
    #     for col, value in row.items():
    #         if value != value:
    #             value = ""
    #         if isinstance(value, (int, float)):
    #                 row_data[col.replace(" ", "_")] = value
    #         elif isinstance(value, datetime):
    #             row_data[col.replace(" ", "_")] = value.strftime("%Y-%m-%d")
    #         else:
    #             row_data[col.replace(" ", "_")] = value
    #     base_data_table["data"].append(row_data)
    result = {
        "base_data_table": base_data_table,
        "report_date": base_data_info.report_date.strftime("%Y-%m-%d"),
        "fund_type": base_data_info.fund_type,
        "card_data": [{
            "No of Obligors": no_of_obligors,
            "No of Assets": no_of_assets,
            "Total Commitment": total_commitment,
            "Total Outstanding Balance": total_outstanding_balance,
        }]
    }
    return ServiceResponse.success(data=result, message="Base Data")

def change_bd_col_seq(updated_sequence):
    try:
        updated_sequence_list = []
        for change in updated_sequence:
            bdm_id = change.get("bdm_id")
            sequence = change.get("sequence")
            base_data_mapping_info = BaseDataMappingColumnInfo.query.filter_by(bdm_id = bdm_id).first()
            base_data_mapping_info.sequence = sequence
            updated_sequence_list.append(base_data_mapping_info)
        
        db.session.add_all(updated_sequence_list)
        db.session.commit()

        return ServiceResponse.success(message = "Base Data Column Sequence Changed Successfully")
    except Exception as e:
        raise Exception(e)
    
def get_base_data_col(fund_type):
    try:
        base_data_columns_data = db.session.query(
            PfltBaseDataMapping.bdm_id,
            PfltBaseDataMapping.bd_column_lookup,
            PfltBaseDataMapping.bd_column_name,
            PfltBaseDataMapping.is_editable,
            BaseDataMappingColumnInfo.sequence,
            BaseDataMappingColumnInfo.is_selected
        ).join(PfltBaseDataMapping, PfltBaseDataMapping.bdm_id == BaseDataMappingColumnInfo.bdm_id).filter(BaseDataMappingColumnInfo.fund_type == fund_type).order_by(BaseDataMappingColumnInfo.sequence).all()
        
        base_data_columns = [{
            "key": column.bd_column_lookup,
            "label": column.bd_column_name,
            "isEditable": column.is_editable,
            "bdm_id": column.bdm_id,
            "is_selected": column.is_selected
        } for column in base_data_columns_data]

        return ServiceResponse.success(data=base_data_columns, message="Base Data Columns")
    except Exception as e:
        Log.func_error(e)
        return ServiceResponse.error(message="Could not get base data columns")
    
def update_bd_col_select(selected_col_ids):
    try:
        # making is_selected as false to all records
        BaseDataMappingColumnInfo.query.update({"is_selected": False})

        default_col_seq = 1
        # modified_by = Users.query.filter_by(id=1).first()
        modified_by = 1
            
        # updating is_selected of selected columns to True with default sequence
        selected_bd_col_info_list = []
        for col_id in selected_col_ids:
            selected_bd_col_info = BaseDataMappingColumnInfo.query.filter_by(bdm_id=col_id).first()
            selected_bd_col_info.sequence = default_col_seq
            default_col_seq = default_col_seq + 1
            selected_bd_col_info.is_selected = True
            selected_bd_col_info.modified_at = datetime.now()
            selected_bd_col_info.modified_by = modified_by
            selected_bd_col_info_list.append(selected_bd_col_info)
        db.session.add_all(selected_bd_col_info_list)
        db.session.commit()

        # updating sequence of unselected columns
        unselected_bd_col_info_list = []
        unselected_bd_cols = BaseDataMappingColumnInfo.query.filter_by(is_selected=False).all()
        for unselected_bd_col in unselected_bd_cols:
            unselected_bd_col.sequence = default_col_seq
            default_col_seq = default_col_seq + 1
            unselected_bd_col_info_list.append(unselected_bd_col)

        db.session.add_all(unselected_bd_col_info_list)
        db.session.commit()

        return ServiceResponse.success(message = "Base Data Column Selection Updated Successfully")

    except Exception as e:
        Log.func_error(e=e)
        db.session.rollback()
        return ServiceResponse.error(message = "Could not Update base data column selection")

def edit_base_data(changes):
    if not changes:
        return ServiceResponse.error(message = "Please provide changes.", status_code = 400)
    for change in changes:
        id = int(change.get("id"))
        for key in change.keys():
            if key != "id":
                value = change.get(key)
                # column = key.replace('_', " ")
                base_data = PfltBaseData.query.filter_by(id=id).first()
                setattr(base_data, key, value)
                db.session.add(base_data)
                db.session.commit()
    return ServiceResponse.success(message = "Basse data edited updated successfully")

def get_base_data_mapping(info_id):
    try:
        engine = db.get_engine()
        with engine.connect() as connection:
            base_data_map = pd.DataFrame(connection.execute(text('''select * from pflt_base_data_mapping''')).fetchall())
            df_dict = base_data_map.to_dict(orient='records')
        return ServiceResponse.success(data=df_dict, message="Base Data Map")
    except Exception as e:
        raise Exception(e)

def get_extracted_base_data_info(company_id, extracted_base_data_info_id, fund_type):
    if extracted_base_data_info_id:
        extracted_base_datas = ExtractedBaseDataInfo.query.filter_by(id = extracted_base_data_info_id).all()
    else:
        extracted_base_datas = ExtractedBaseDataInfo.query.filter_by(company_id = company_id).order_by(ExtractedBaseDataInfo.extraction_date.desc()).all()
    if fund_type:
        extracted_base_datas = ExtractedBaseDataInfo.query.filter_by(company_id = company_id, fund_type=fund_type).order_by(ExtractedBaseDataInfo.extraction_date.desc()).all()
    extraction_result = {
        "columns": [{
            "key": "report_date",
            "label": "Report Date"
        }, {
            "key": "fund",
            "label": "Fund"
        }, {
            "key": "extraction_status",
            "label": "Extraction Status"
        }, {
            "key": "extraction_date",
            "label": "Extraction Date"
        }, {
            "key": "source_files",
            "label": "Source Files"
        }],
        "data": []
    }

    for extracted_base_data in extracted_base_datas:
        source_files = SourceFiles.query.filter(SourceFiles.id.in_(extracted_base_data.files)).all()
        files = ''
        file_details = []
        for file in source_files:
            if files == '':
                files = file.file_name
            else:
                files = files + '; ' + file.file_name
            file_details.append({'file_id': file.id, 'file_name': file.file_name, 'file_type': file.file_type, 'extension': file.extension})
        extraction_result["data"].append({
            "id": extracted_base_data.id,
            "report_date": extracted_base_data.report_date.strftime("%Y-%m-%d"),
            "fund": extracted_base_data.fund_type,
            "extraction_status": extracted_base_data.status,
            "extraction_date": extracted_base_data.extraction_date.strftime("%Y-%m-%d"),
            "source_files": files,
            "source_file_details":  file_details
        })
    
    return ServiceResponse.success(data=extraction_result)

def get_pflt_sec_mapping():
    engine = db.get_engine()
    with engine.connect() as connection:
        pflt_sec_mapping_df = pd.DataFrame(connection.execute(text('select id, soi_name, master_comp_security_name, family_name, security_type, cashfile_security_name from pflt_security_mapping where company_id = 1 order by soi_name ASC')).fetchall())

        unmapped_securities = pd.DataFrame(connection.execute(text('''select distinct "Security/Facility Name" as cashfile_securities from pflt_us_bank_holdings pubh left join pflt_security_mapping psm on psm.cashfile_security_name = pubh."Security/Facility Name" where psm.id is null''')).fetchall())
    
    columns_data = [
        {
            'key': "soi_name",
            'label': "Soi name",
            'isEditable': False
        }, {
            'key': "master_comp_security_name",
            'label': "Master comp security name",
            'isEditable': False
        },  {
            'key': "family_name",
            'label': "Family name",
            'isEditable': True
        }, {
            'key': "security_type",
            'label': "Security type",
            'isEditable': False
        }, {
            'key': "cashfile_security_name",
            'label': "Cash file security name",
            'isEditable': True
        }
    ]
    pflt_sec_mapping_table = {
        "columns": columns_data,
        "data": []
    }
    pflt_sec_mapping_df.columns = pflt_sec_mapping_df.columns.str.replace(" ", "_")
    pflt_sec_mapping_df = pflt_sec_mapping_df.replace({np.nan: None})
    df_dict = pflt_sec_mapping_df.to_dict(orient='records')
    pflt_sec_mapping_table["data"] = df_dict
    pflt_sec_mapping_table["unmapped_securities"] = unmapped_securities.to_dict(orient='records')

    return ServiceResponse.success(data=pflt_sec_mapping_table, message="pflt security mapping")

def edit_pflt_sec_mapping(changes):
    engine = db.get_engine()
    modified_by = 1 # currently hard coding this variable
    for change in changes:
        id = change.get("id")
        for key in change.keys():
            if key != "id":
                value = change.get(key)
                with engine.connect() as connection:
                    connection.execute(text(f"UPDATE pflt_security_mapping SET {key} = :value, modified_by = :modified_by, modified_at = now() WHERE id = :id"), {"value": value, "id":id, 'modified_by': modified_by})
                    connection.commit()
    
    return ServiceResponse.success(message="PFLT security mapping edited successfully")

def add_pflt_sec_mapping(cashfile_security_name, family_name, master_comp_security_name, security_type, soi_name):
    company_id = 1
    modified_by = 1
    timestamp = datetime.now(pytz.UTC)

    pfltSecurityMapping = PfltSecurityMapping(company_id=company_id, soi_name=soi_name, master_comp_security_name=master_comp_security_name, family_name=family_name, security_type=security_type, cashfile_security_name=cashfile_security_name, modified_by=modified_by, modified_at=timestamp)

    db.session.add(pfltSecurityMapping)
    db.session.commit()
    
    return ServiceResponse.success(message="PFLT security mapping added successfully")

def get_source_file_data(file_id, file_type, sheet_name):
    # ["US Bank Holdings", "Client Holdings"] for Cash
    # ["Borrower Stats", "Securities Stats", "PFLT Borrowing Base"] for Master Comp
    if file_type == "cashfile" and sheet_name == None:
        sheet_name = "US Bank Holdings"
    if file_type == "master_comp" and sheet_name == None:
        sheet_name = "Borrower Stats"
    print(sheet_name)
    match sheet_name:
        case "US Bank Holdings":
            table_name = "pflt_us_bank_holdings"
        case "Client Holdings":
            table_name = "pflt_client_holdings"
        case "Borrower Stats":
            table_name = "pflt_borrower_stats"
        case "Securities Stats":
            table_name = "pflt_securities_stats"
        case "PFLT Borrowing Base":
            table_name = "pflt_pflt_borrowing_base"

    source_file_table_data = {}

    engine = db.get_engine()
    with engine.connect() as connection:
        sheet_df = pd.DataFrame(connection.execute(text(f'select * from "{table_name}" where source_file_id = {file_id}')).fetchall())

    colummns = [
        {
            'key': column.replace(' ', '_'), 
            'label': column
        } for column in sheet_df.columns]
    source_file_table_data['columns'] = colummns

    sheet_df.columns = sheet_df.columns.str.replace(" ", "_")
    sheet_df = sheet_df.replace({np.nan: None})
    df_dict = sheet_df.to_dict(orient='records')
    source_file_table_data['data'] = df_dict
    
    return ServiceResponse.success(data=source_file_table_data)


def get_source_file_data_detail(ebd_id, column_key, data_id):
    try:
        engine = db.get_engine()
        with engine.connect() as connection:
            df = pd.DataFrame(connection.execute(text(f'select sf.id, sf.file_type, sf.file_name, sf."extension", pbdm.bd_column_name, pbdm.bd_column_lookup, pbdm.sf_sheet_name, pbdm.sf_column_name, pbdm.sd_ref_table_name, case when pbdm.sf_column_lookup is null then pbdm.sf_column_name else pbdm.sf_column_lookup end as sf_column_lookup, sf_column_categories, formula from extracted_base_data_info ebdi join source_files sf on sf.id in (select unnest(files) from extracted_base_data_info ebdi where ebdi.id = :ebd_id) join pflt_base_data_mapping pbdm on pbdm.sf_file_type = sf.file_type where ebdi.id = :ebd_id and pbdm.bd_column_lookup = :column_key'), {'ebd_id': ebd_id, 'column_key': column_key}).fetchall())
            bd_df = pd.DataFrame(connection.execute(text(f'select * from pflt_base_data where id = :data_id'), {'data_id': data_id}).fetchall())
        
        df = df.replace({np.nan: None})
        df_dict = df.to_dict(orient='records')
        try:
            table_name = df_dict[0]['sd_ref_table_name']
            sd_col_name = df_dict[0]['sf_column_name']
            identifier_col_name = None
            if table_name == 'pflt_client_holdings':
                identifier_col_name = 'ch."Issuer/Borrower Name"'
            elif table_name == 'pflt_us_bank_holdings':
                identifier_col_name = 'usbh."Issuer/Borrower Name"'
            elif table_name == 'pflt_securities_stats':
                identifier_col_name = 'ss."Security"'
            elif table_name == 'pflt_borrower_stats':
                identifier_col_name = 'bs."Company"'
            elif table_name == 'pflt_pflt_borrowing_base':
                identifier_col_name = 'pbb."Security"'
            sd_df_dict = None
            if identifier_col_name is not None:
                if df_dict[0]['sf_column_categories'] is not None:
                    sd_col_name = df_dict[0]['sf_column_categories'][0] + " " + sd_col_name
                with engine.connect() as connection:
                    sd_df = pd.DataFrame(connection.execute(text(f'''select distinct {identifier_col_name}, "{sd_col_name}" from pflt_us_bank_holdings usbh
                    left join pflt_client_holdings ch on ch."Issuer/Borrower Name" = usbh."Issuer/Borrower Name" and ch."Current Par Amount (Issue Currency) - Settled" = usbh."Current Par Amount (Issue Currency) - Settled"
                    left join pflt_security_mapping sm on sm.cashfile_security_name = usbh."Security/Facility Name"
                    left join pflt_securities_stats ss on ss."Security" = sm.master_comp_security_name
                    left join pflt_pflt_borrowing_base pbb on pbb."Security" = ss."Security"
                    left join pflt_borrower_stats bs on bs."Company" = ss."Family Name" where usbh."Issuer/Borrower Name" = :obligor_name and ss."Security" = :security_name and (usbh.source_file_id = :sf_id or ch.source_file_id = :sf_id or ss.source_file_id = :sf_id or pbb.source_file_id = :sf_id or bs.source_file_id = :sf_id)'''), {'obligor_name': bd_df['obligor_name'][0], 'security_name': bd_df['security_name'][0], 'sf_id': df_dict[0]['id']}).fetchall())
                sd_df_dict = sd_df.to_dict(orient='records')
        except Exception as e:
            print(e)
        result = {
            'mapping_data': df_dict[0],
            'source_data': sd_df_dict
		}
        if len(df_dict) == 0:
            return ServiceResponse.error(message='No data found.', status_code=404)
        if len(df_dict) > 1:
            return ServiceResponse.error(message='Multiple records found.', status_code=409)
        return ServiceResponse.success(data=result)
    except Exception as e:
        raise Exception(e)

def trigger_bb_calculation(bdi_id):
    try:
        engine = db.get_engine()
        with engine.connect() as connection:
            df = pd.DataFrame(connection.execute(text(f'select * from pflt_base_data where base_data_info_id = :ebd_id'), {'ebd_id': bdi_id}).fetchall())
            df2 = pd.DataFrame(connection.execute(text(f'select bd_column_name, bd_column_lookup from pflt_base_data_mapping where bd_column_lookup is not null')).fetchall())
            # haircut_config = pd.DataFrame(connection.execute(text(f'select haircut_level, obligor_tier, "position", value from pflt_haircut_config')).fetchall())
            industry_list = pd.DataFrame(connection.execute(text(f'select industry_no as "Industry No", industry_name as "Industry" from pflt_industry_list')).fetchall())
        df = df.replace({np.nan: None})
        report_date = df['report_date'][0].strftime("%Y-%m-%d")
        df = df.drop('report_date', axis=1)
        df = df.drop('created_at', axis=1)
        df = df.drop('base_data_info_id', axis=1)
        df = df.drop('id', axis=1)
        df = df.drop('company_id', axis=1)
        df = df.drop('created_by', axis=1)
        df = df.drop('modified_by', axis=1)
        df = df.drop('modified_at', axis=1)
        # df['report_date'] = df['report_date'].astype(str)
        # df['created_at'] = df['created_at'].astype(str)
        
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.title = "Loan List"
        file_name = "PFLT Base data - " + report_date + ".xlsx"
        wb.save(file_name)

        path1 = 'PFLT Base data.xlsx'
        path2 = file_name
        wb1 = openpyxl.load_workbook(filename=path1)
        for index, sheet in enumerate(wb1.worksheets):
            ws1 = wb1.worksheets[index]

            wb2 = openpyxl.load_workbook(filename=path2)
            ws2 = wb2.create_sheet(ws1.title)
            for row in ws1:
                for cell in row:
                    ws2[cell.coordinate].value = cell.value
            wb2.save(path2)
        
        rename_df_col = {}
        for index, row in df2.iterrows():
            rename_df_col[row['bd_column_lookup']] = row['bd_column_name']
        df.rename(columns=rename_df_col, inplace=True)
        # print(df.dtypes)
        # for c in df.columns:
            # print(c, df[c].dtype)

        # df["Initial TTM EBITDA"] = df["Initial TTM EBITDA"].astype(float)
        # df["Current TTM EBITDA"] = df["Current TTM EBITDA"].astype(float)
        # df["Current Fixed Charge Coverage Ratio"] = df["Current Fixed Charge Coverage Ratio"].astype(float)
        # df["Initial Fixed Charge Coverage Ratio"] = df["Current Fixed Charge Coverage Ratio"].astype(float)

        # df["Spread incl. PIK and PIK'able"].fillna(0, inplace=True)
        # df["PIK / PIK'able For Floating Rate Loans"].fillna(0, inplace=True)
        # df["PIK / PIK'able For Fixed Rate Loans"].fillna(0, inplace=True)
        # df["Base Rate"].fillna(0, inplace=True)

        xl_df_map = {}
        xl_df_map['Loan List'] = df

        book = load_workbook(file_name)
        writer = pd.ExcelWriter(file_name, engine="openpyxl")
        writer.book = book
        df.to_excel(writer, sheet_name="Loan List", index=False, header=True)
        writer.save()


        data = {'INPUTS': ['Determination Date', 'Minimum Equity Amount Floor'], '': ['', ''], 'Values': ['9-30-24', '30000000']}
        data = pd.DataFrame.from_dict(data)
        xl_df_map['Inputs'] = data

        # book = load_workbook(file_name)
        # writer = pd.ExcelWriter(file_name, engine="openpyxl")
        # writer.book = book
        # data.to_excel(writer, sheet_name="Inputs", index=False, header=True)
        # writer.save()

        data = {'Currency': ['USD', 'CAD', 'AUD', 'EUR'], 'Exchange Rate': ['1.000000', '0.739350', '0.691310', '1.113500']}
        data = pd.DataFrame.from_dict(data)
        xl_df_map['Exchange Rates'] = data

        # book = load_workbook(file_name)
        # writer = pd.ExcelWriter(file_name, engine="openpyxl")
        # writer.book = book
        # data.to_excel(writer, sheet_name="Exchange Rates", index=False, header=True)
        # writer.save()

        data = {'Currency': ['USD', 'CAD', 'AUD', 'EUR'], 'Exchange Rates': [1.000000, 0.739350, 0.691310, 1.113500], 'Cash - Current & PreBorrowing': [50958522.16, 265552.25, 0, 0], 'Borrowing': ['0', '', '', ''], 'Additional Expences 1': [0, 0, 0, 0], 'Additional Expences 2': [0, 0, 0, 0], 'Additional Expences 3': [0, 0, 0, 0]}
        data = pd.DataFrame.from_dict(data)
        xl_df_map['Cash Balance Projections'] = data

        # book = load_workbook(file_name)
        # writer = pd.ExcelWriter(file_name, engine="openpyxl")
        # writer.book = book
        # data.to_excel(writer, sheet_name="Cash Balance Projections", index=False, header=True)
        # writer.save()

        data = {'Currency': ['USD', 'CAD', 'AUD', 'EUR'], 'Current Credit Facility Balance': [442400000, 2000000, 0, 0]}
        data = pd.DataFrame.from_dict(data)
        xl_df_map['Credit Balance Projection'] = data

        # book = load_workbook(file_name)
        # writer = pd.ExcelWriter(file_name, engine="openpyxl")
        # writer.book = book
        # data.to_excel(writer, sheet_name="Credit Balance Projection", index=False, header=True)
        # writer.save()

        data = {'Haircut': ['', 'SD/EBITDA', 'TD/EBITDA', 'UD/EBITDA'], '20% Conc. Limit': ['Tier 1 Obligor', 5, 7, 6], 'Unnamed: 2': ['Tier 2 Obligor', 4.25, 6, 5.25], 'Unnamed: 3': ['Tier 3 Obligor', 3.75, 5, 4.5], 'Level 1 - 10% Haircut': ['Tier 1 Obligor', 5.5, 7.5, 6.5], 'Unnamed: 5': ['Tier 2 Obligor', 4.75, 6.5, 5.75], 'Unnamed: 6': ['Tier 3 Obligor', 4.25, 5.5, 5], 'Level 2 - 20% Haircut': ['Tier 1 Obligor', 5.5, 7.5, 6.5], 'Unnamed: 8': ['Tier 2 Obligor', 4.75, 6.5, 5.75], 'Unnamed: 9': ['Tier 3 Obligor', 4.25, 5.5, 5], 'Level 3 - 35% Haircut': ['Tier 1 Obligor', 5.5, 7.5, 6.5], 'Unnamed: 11': ['Tier 2 Obligor', 4.75, 6.5, 5.75], 'Unnamed: 12': ['Tier 3 Obligor', 4.25, 5.5, 5], 'Level 4 - Max Eligibility - 50% Haircut': ['Tier 1 Obligor', 5.5, 7.5, 6.5], 'Unnamed: 14': ['Tier 2 Obligor', 4.75, 6.5, 5.75], 'Unnamed: 15': ['Tier 3 Obligor', 4.25, 5.5, 5]}
        data = pd.DataFrame.from_dict(data)
        xl_df_map['Haircut'] = data

        # book = load_workbook(file_name)
        # writer = pd.ExcelWriter(file_name, engine="openpyxl")
        # writer.book = book
        # data.to_excel(writer, sheet_name="Haircut", index=False, header=True)
        # writer.save()

        # # data = {'Currency': ['USD', 'CAD', 'AUD', 'EUR'], 'Current Credit Facility Balance': ['442400000', '2000000', '0', '0']}
        # # data = pd.DataFrame.from_dict(data)
        xl_df_map['Industry'] = industry_list

        # book = load_workbook(file_name)
        # writer = pd.ExcelWriter(file_name, engine="openpyxl")
        # writer.book = book
        # industry_list.to_excel(writer, sheet_name="Industry", index=False, header=True)
        # writer.save()
        # print(industry_list)

        # print(xl_df_map)

        # df.to_excel("output.xlsx")

        xl_df_map = pd.read_excel(file_name, sheet_name=['Loan List', 'Inputs', 'Exchange Rates', 'Cash Balance Projections', 'Credit Balance Projection', 'Haircut', 'Industry'])
        pickled_xl_sheet_df_map = pickle.dumps(xl_df_map)

        included_excluded_assets_map = pfltDashboardService.pflt_included_excluded_assets(xl_df_map)

        # datetime object containing current date and time
        now = datetime.now()
        
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        base_data_file = BaseDataFile(
            user_id=1,
            closing_date=report_date,
            fund_type='PFLT',
            file_data=pickled_xl_sheet_df_map,
            file_name='Generated Data ' + dt_string,
            included_excluded_assets_map=json.dumps(included_excluded_assets_map),
        )

        db.session.add(base_data_file)
        db.session.commit()

        base_data_file = commonServices.get_base_data_file(
            base_data_file_id=base_data_file.id
        )
        # if base_data_file.fund_type == "PCOF":
            # return pcofDashboardService.calculate_bb(
            #     base_data_file, selected_assets, user_id
            # )
        # else:
        selected_assets = included_excluded_assets_map['included_assets']
        wb2.close()
        writer.close()
        os.remove(file_name)
        return pfltDashboardService.calculate_bb(base_data_file, selected_assets, 1)

    except Exception as e:
        print(e)

def get_archived_file_list():

    source_files = db.session.query(SourceFiles).filter(SourceFiles.is_archived == True).order_by(SourceFiles.uploaded_at.desc()).all()
    
    list_table = {
        "columns": [{
            "key": "fund", 
            "label": "Fund",
        }, {
            "key": "file_name", 
            "label": "File Name",
        }, {
            "key": "report_date", 
            "label": "Report Date",
        }, {
            "key": "uploaded_at", 
            "label": "Uploaded at",
        }, {
            "key": "uploaded_by", 
            "label": "Uploaded by",
        }], 
        "data": []
    }

    for source_file in source_files:
        list_table["data"].append({
            "file_id": source_file.id,
            "file_name": source_file.file_name + source_file.extension, 
            "uploaded_at": source_file.uploaded_at.strftime("%Y-%m-%d"),
            "report_date": source_file.report_date.strftime("%Y-%m-%d"),
            "fund": source_file.fund_types,
            "source_file_type": source_file.file_type,
        })
        print(source_file.fund_types)
    
    return ServiceResponse.success(data=list_table)

def add_file_to_archive(list_of_ids):
    try:
        for file_id in list_of_ids:
            source_file = SourceFiles.query.filter_by(id=file_id).first()

            if source_file:
                source_file.is_archived = True

            db.session.add(source_file)
            db.session.commit()
              
        return ServiceResponse.success(message = "Files uploaded successfully")

    except Exception as e:
        Log.func_error(e=e)
        return ServiceResponse.error(message="Could not upload files.", status_code = 500)    
def add_pflt_base_data_other_info(extraction_info_id, determination_date, minimum_equity_amount_floor, other_data):
    try:
        other_info_list = []
    
        for value in other_data:
            other_info_list.append ({
                "currency": value.get("currency"),
                "exchange_rates": value.get("exchange_rates"),
                "cash_current_and_preborrowing": value.get("cash_current_and_preborrowing"),
                "borrowing": value.get("borrowing"),
                "additional_expenses_1": value.get("additional_expenses_1"),
                "additional_expenses_2": value.get("additional_expenses_2"),
                "additional_expenses_3": value.get("additional_expenses_3"),
                "current_credit_facility_balance": value.get("current_credit_facility_balance")
            })

            pflt_base_data_other_info =  PfltBaseDataOtherInfo(
                extraction_info_id = extraction_info_id,
                determination_date = determination_date,
                minimum_equity_amount_floor = minimum_equity_amount_floor,
                other_info_list = other_info_list
            )
            db.session.add(pflt_base_data_other_info)
            db.session.commit()

        return ServiceResponse.success(message="Data added sucessfully")
        
    except Exception as e:
        Log.func_error(e)
        return ServiceResponse.error(message="Failed to add")
