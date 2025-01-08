from azure.core.exceptions import ResourceExistsError
import os
import mmap
from io import BytesIO
import pandas as pd
from datetime import datetime
import azure.functions as func
from sqlalchemy import text
import threading
import numpy as np

from source.app_configs import azureConfig
from source.utility.ServiceResponse import ServiceResponse
from source.utility.Log import Log
from models import SourceFiles, Users, db, ExtractedBaseDataInfo
from source.services.diServices import helper_functions
from source.services.diServices import base_data_mapping
from source.services.PFLT.PfltDashboardService import PfltDashboardService

def upload_src_file_to_az_storage(files, report_date):
    if len(files) == 0:
        return ServiceResponse.error(message = "Please select files.", status_code = 400)
    
    blob_service_client, blob_client = azureConfig.get_az_service_blob_client()
    company_name = "Pennant"
    fund_name = "PFLT"
    report_date = datetime.strptime(report_date, "%Y-%m-%d").date()

    source_files = []
    try:
        for file in files:
            print(file.filename)
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
                file_type = "Cash"
            if contains_master_comp(file.filename):
                file_type = "Master Comp"

            # upload blob in container
            blob_client.upload_blob(name=blob_name, data=file)
            file_url = blob_client.url + '/' + blob_name
            # add details of files in db
            source_file = SourceFiles(file_name=file_name, extension=extension, report_date=report_date, file_url=file_url, file_size=file_size, company_id=company_id, fund_type=fund_name, is_validated=is_validated, is_extracted=is_extracted, uploaded_by=uploaded_by, file_type=file_type)

            db.session.add(source_file)
            db.session.commit()
                # source_files.append(source_file)
            # try:
            #     db.session.add_all(source_files)
            #     db.session.commit()
            # except Exception as e:
            #     Log.func_error(e=e)
            #     return ServiceResponse.error(message="Could not save files to database.", status_code = 500)
            
        return ServiceResponse.success(message = "Files uploaded successfully")

    except ResourceExistsError as ree:
        Log.func_error(e=ree)
        return ServiceResponse.error(message="Files with same name already exist.", status_code=409)
    except Exception as e:
        Log.func_error(e=e)
        return ServiceResponse.error(message="Could not upload files.", status_code = 500)
    
def get_blob_list():
    company_id = 1 # for Penennt
    fund_type = "PFLT"
    source_files = db.session.query(
            SourceFiles.id,
            SourceFiles.file_name,
            SourceFiles.extension,
            SourceFiles.uploaded_at,
            SourceFiles.uploaded_by,
            SourceFiles.fund_type,
            SourceFiles.file_type,
            SourceFiles.report_date,
            Users.display_name
        ).join(Users, Users.user_id == SourceFiles.uploaded_by).filter(SourceFiles.is_deleted == False, SourceFiles.company_id == company_id, SourceFiles.fund_type == fund_type).order_by(SourceFiles.uploaded_at.desc()).all()
    # SourceFiles.query.join(Users).filter_by(is_deleted=False, company_id=company_id, fund_type=fund_type).order_by(SourceFiles.uploaded_at.desc()).all()
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
            "fund": source_file.fund_type,
            "source_file_type": source_file.file_type,
            "uploaded_by": source_file.display_name
        })
    
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
                if (file_type == 'Cash'):
                    cash_file_details = file_details
                    file_sheet_map = {
                        "cash": {
                            "file": file,
                            "source_file_obj": file_details,
                            "sheets": ["US Bank Holdings", "Client Holdings"], 
                            "is_extracted": file_details.is_extracted
                        }
                    }
                elif file_type == 'Master Comp':
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
            extracted_base_data_info.comments = str(e)
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
            extracted_base_data_info.comments = str(e)
            db.session.add(extracted_base_data_info)
            db.session.commit()
        return ServiceResponse.error(message='Extraction failed')


def get_base_data(info_id):
    # datetime_obj = datetime.strptime(report_date, "%Y-%m-%d")
    engine = db.get_engine()
    with engine.connect() as connection:
        base_data = pd.DataFrame(connection.execute(text('''select
        "Obligor Name",
        "Security",
        "Security Name",
        "Purchase Date (Date Loan contributed to the facility)",
        "Total Commitment (Issue Currency)",
        "Outstanding Principal Balance (Issue Currency)",
        "Defaulted Collateral Loan / Material Mod (Y/N)",
        "Credit Improved Loan (Y/N)",
        "Purchase Price",
        "Stretch Senior Loan (Y/N)",
        "Loan Type (Term / Delayed Draw / Revolver)",
        "Current Moody's Rating",
        "Current S&P Rating",
        "Initial Fixed Charge Coverage Ratio",
        "Date of Default",
        "Market Value",
        "Current Fixed Charge Coverage Ratio",
        "Current Interest Coverage Ratio",
        "Initial Debt to Capitalization Ratio",
        "Initial Senior Debt/EBITDA",
        "Initial Total Debt/EBITDA",
        "Current Senior Debt/EBITDA",
        "Current Total Debt/EBITDA",
        "Initial TTM EBITDA",
        "Current TTM EBITDA",
        "Current As of Date For Leverage and EBITDA",
        "Maturity Date",
        "Fixed Rate (Y/N)",
        "Coupon incl. PIK and PIK'able (if Fixed)",
        "Floor Obligation (Y/N)",
        "Floor",
        "Spread incl. PIK and PIK'able",
        "Base Rate",
        "For Revolvers/Delayed Draw, commitment or other unused fee",
        "PIK / PIK'able For Floating Rate Loans",
        "PIK / PIK'able For Fixed Rate Loans",
        "Interest Paid",
        "Obligor Industry",
        "Currency (USD / CAD / AUD / EUR)",
        "Obligor Country",
        "DIP Loan (Y/N)",
        "Warrants to Purchase Equity (Y/N)",
        "Parti-cipation (Y/N)",
        "Convertible to Equity (Y/N)",
        "Equity Security (Y/N)",
        "At Acquisition - Subject to offer or called for redemption (Y/N)",
        "Margin Stock (Y/N)",
        "Subject to withholding tax (Y/N)",
        "At Acquisition - Defaulted Collateral Loan",
        "Zero Coupon Obligation (Y/N)",
        "Covenant Lite (Y/N)",
        "Structured Finance Obligation, finance lease or chattel paper (Y/N)",
        "Material Non-Credit Related Risk (Y/N)",
        "Primarily Secured by Real Estate, Construction Loan or Project Finance Loan (Y/N)",
        "Interest Only Security (Y/N)",
        "Satisfies all Other Eligibility Criteria (Y/N)",
        "Excess Concentration Amount (HARD CODE on Last Day of Reinvestment Period)" from base_data where base_data_info_id = :info_id'''), {"info_id": info_id}).fetchall())

    base_data_info = ExtractedBaseDataInfo.query.filter_by(id = info_id).first()
    base_data_table = {
        "columns": [{"key": column.replace(" ", "_"), "label": column} for column in base_data.columns],
        "data": []
    }
    
    
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
    base_data.columns = base_data.columns.str.replace(" ", "_")
    base_data = base_data.replace({np.nan: None})
    df_dict = base_data.to_dict(orient='records')
    base_data_table["data"] = df_dict
    result = {
        "base_data_table": base_data_table,
        "report_date": base_data_info.report_date.strftime("%Y-%m-%d"),
        "fund_type": base_data_info.fund_type
    }
    return ServiceResponse.success(data=result, message="Base Data")

def get_base_data_mapping(info_id):
    try:
        engine = db.get_engine()
        with engine.connect() as connection:
            base_data_map = pd.DataFrame(connection.execute(text('''select * from base_data_mapping''')).fetchall())
            df_dict = base_data_map.to_dict(orient='records')
        return ServiceResponse.success(data=df_dict, message="Base Data Map")
    except Exception as e:
        raise Exception(e)

def get_extracted_base_data_info(company_id, extracted_base_data_info_id):
    if extracted_base_data_info_id:
        extracted_base_datas = ExtractedBaseDataInfo.query.filter_by(id = extracted_base_data_info_id).all()
    else:
        extracted_base_datas = ExtractedBaseDataInfo.query.filter_by(company_id = company_id).order_by(ExtractedBaseDataInfo.extraction_date.desc()).all()
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
            'label': "Soi name"
        }, {
            'key': "master_comp_security_name",
            'label': "Master comp security name"
        },  {
            'key': "family_name",
            'label': "Family name"
        }, {
            'key': "security_type",
            'label': "Security type"
        }, {
            'key': "cashfile_security_name",
            'label': "Cash file security name"
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

def get_source_file_data(file_id, file_type, sheet_name):
    # ["US Bank Holdings", "Client Holdings"] for Cash
    # ["Borrower Stats", "Securities Stats", "PFLT Borrowing Base"] for Master Comp
    if file_type == "Cash" and sheet_name == None:
        sheet_name = "US Bank Holdings"
    if file_type == "Master Comp" and sheet_name == None:
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
    