from azure.core.exceptions import ResourceExistsError
import os
import mmap
from io import BytesIO
import pandas as pd
from datetime import datetime
import azure.functions as func
from sqlalchemy import text

from source.app_configs import azureConfig
from source.utility.ServiceResponse import ServiceResponse
from source.utility.Log import Log
from models import SourceFiles, db
from source.services.diServices import helper_functions
from source.services.diServices import base_data_mapping

def upload_src_file_to_az_storage(files, report_date):
    if len(files) == 0:
        return ServiceResponse.error(message = "Please select files.", status_code = 400)
    
    blob_service_client, blob_client = azureConfig.get_az_service_blob_client()
    company_name = "Penennt"
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
            file_url = "file_url"
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
    source_files = SourceFiles.query.filter_by(is_deleted=False, company_id=company_id, fund_type=fund_type).order_by(SourceFiles.uploaded_at.desc()).all()
    list_table = {
        "columns": [{
            "key": "file_name", 
            "label": "File Name",
        }, {
            "key": "uploaded_at", 
            "label": "Uploaded at",
        }, {
            "key": "fund", 
            "label": "Fund",
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
            "fund": source_file.fund_type,
            "source_file_type": source_file.file_type
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
        columns.append(column_name)

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
    return updated_column_df

def extract_base_data(cash_file_id, master_comp_file_id):

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
        "Borrower Stats (Quarterly)": borrower_stats_column_level_map,
        "Securities Stats": security_stats,
        "US Bank Holdings": {},
        "Client Holdings": {},
        "SOI Mapping": SOI_Mapping,
        "PFLT Borrowing Base": {}
    }
    #--------------------------------

    if not cash_file_id or not master_comp_file_id:
        return ServiceResponse.error(message="Cash file and master company file ids are required.", status_code=400)
    
    FOLDER_PATH = "Penennt/PFLT/"
    
    blob_service_client, blob_client = azureConfig.get_az_service_blob_client()

    cash_file_details = SourceFiles.query.filter_by(id=cash_file_id).first()
    master_comp_file_details = SourceFiles.query.filter_by(id=master_comp_file_id).first()

    if master_comp_file_details.is_extracted and cash_file_details.is_extracted:
        return ServiceResponse.error(message="Data already extracted for the given files.")

    cash_file_name = cash_file_details.file_name + cash_file_details.extension
    master_comp_file_name = master_comp_file_details.file_name + master_comp_file_details.extension

    cash_file = BytesIO(blob_client.get_blob_client(FOLDER_PATH + cash_file_name).download_blob().readall())
    
    master_comp_file = BytesIO(blob_client.get_blob_client(FOLDER_PATH + master_comp_file_name).download_blob().readall())

    file_sheet_map = {
        "master_comp": {
            "file": master_comp_file,
            "source_file_obj": master_comp_file_details,
            "sheets": ["Borrower Stats (Quarterly)", "Securities Stats", "PFLT Borrowing Base"],
            "is_extracted": master_comp_file_details.is_extracted
        },
        "cash": {
            "file": cash_file,
            "source_file_obj": cash_file_details,
            "sheets": ["US Bank Holdings", "Client Holdings"], 
            "is_extracted": master_comp_file_details.is_extracted
        }
    }
    args = ['Company', "Security", "CUSIP", "Asset ID", "SOI Name"]


    azure_func_app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

    # put this following code in above function
    start_time = datetime.now()
    data_dict = extract(file_sheet_map, sheet_column_mapper, args)
    engine = db.get_engine()
    process_store_status = helper_functions.process_and_store_data(data_dict, engine)
    # if not process_store_status:
    #     return ServiceResponse.error(message="Error processing and storing data.", status_code=500)
    base_data_mapping.soi_mapping(engine, master_comp_file_details.company_id, master_comp_file_details.report_date)
    
    cash_file_details.is_extracted =True
    master_comp_file_details.is_extracted = True

    db.session.add(cash_file_details)
    db.session.add(master_comp_file_details)
    db.session.commit()

    end_time = datetime.now()
    time_difference = (end_time - start_time).total_seconds() * 10**3

    response_data = {
        "report_date": master_comp_file_details.report_date.strftime("%Y-%m-%d"),
        "company_id": master_comp_file_details.company_id
    }
    return ServiceResponse.success(message="Base data extracted successfully", data=response_data)


def get_base_data(report_date, company_id):
    datetime_obj = datetime.strptime(report_date, "%Y-%m-%d")
    engine = db.get_engine()
    with engine.connect() as connection:
        base_data = pd.DataFrame(connection.execute(text('''select distinct
	usbh."Issuer/Borrower Name" as "Obligor Name",
	usbh."Security/Facility Name" as "Security",
	ss."Security" as "Security Name",
	null as "Purchase Date (Date Loan contributed to the facility)",
	sum(ch."Par Amount (Deal Currency)"::float) as "Total Commitment (Issue Currency)",
	sum(ch."Principal Balance (Deal Currency)"::float) as "Outstanding Principal Balance (Issue Currency)",
	case when pbb."Defaulted Collateral Loan at Acquisition" = 0 then 'N' when pbb."Defaulted Collateral Loan at Acquisition" = 1 then 'Y' else null end as "Defaulted Collateral Loan / Material Mod (Y/N)",
	case when pbb."Credit Improved Loan" = 0 then 'N' when pbb."Credit Improved Loan" = 1 then 'Y' else null end as "Credit Improved Loan (Y/N)",
	usbh."Original Purchase Price" as "Purchase Price",
	pbb."Stretch Senior (Y/N)" as "Stretch Senior Loan (Y/N)",
	ch."Issue Name" as "Loan Type (Term / Delayed Draw / Revolver)",
	ch."Deal Issue (Derived) Rating - Moody's" as "Current Moody's Rating",
	ch."Deal Issue (Derived) Rating - S&P" as "Current S&P Rating",
	bs."[ACM] [C-ACM(AC] Closing Fixed Charge Coverage Ratio" as "Initial Fixed Charge Coverage Ratio",
	null as "Date of Default",
	null as "Market Value",
	bs."[ACM] [C-ACM(AC] Closing Fixed Charge Coverage Ratio" as "Current Fixed Charge Coverage Ratio",
	bs."[CM] [CLSO] 1st Lien Net Debt / EBITDA" as "Current Interest Coverage Ratio",
	bs."[ACM] [C-ACM(AC] Closing Debt to Capitalization" as "Initial Debt to Capitalization Ratio",
	bs."[ACM] [C-ACM(AC] 1st Lien Net Debt / EBITDA" as "Initial Senior Debt/EBITDA",
	bs."[ACM] [C-ACM(AC] HoldCo Net Debt / EBITDA" as "Initial Total Debt/EBITDA",
	pbb."Senior Debt"::float / pbb."LTM EBITDA"::float as "Current Senior Debt/EBITDA",
	pbb."Total Debt"::float / pbb."LTM EBITDA"::float as "Current Total Debt/EBITDA",
	pbb."Closing LTM EBITDA" as "Initial TTM EBITDA",
	pbb."Current LTM EBITDA" as "Current TTM EBITDA",
	ch."As Of Date" as "Current As of Date For Leverage and EBITDA",
	usbh."Maturity Date" as "Maturity Date",
	case
		when ss."[SI] Type of Rate" like 'Fixed Rate%' then 'Y'
		else 'N'
	end as "Fixed Rate (Y/N)",
	null as "Coupon incl. PIK and PIK'able (if Fixed)",
	case
		when ss."[SI] LIBOR Floor" is not null then 'Y'
		else 'N'
	end as "Floor Obligation (Y/N)",
	case
		when ss."[SI] LIBOR Floor" != 'NM' then ss."[SI] LIBOR Floor"::float
		else null
	end as "Floor",
	case
		when ss."[SI] Cash Spread to LIBOR" != 'NM' and ss."[SI] Cash Spread to LIBOR" is not null then ss."[SI] Cash Spread to LIBOR"::float + coalesce(ss."[SI] PIK Coupon"::float, 0)::float
		else null
	end as "Spread incl. PIK and PIK'able",
	null as "Base Rate",
	null as "For Revolvers/Delayed Draw, commitment or other unused fee",
	null as "PIK / PIK'able For Floating Rate Loans",
	null as "PIK / PIK'able For Fixed Rate Loans",
	null as "Interest Paid",
	bs."[ACM] [COI/LC] S&P Industry" as "Obligor Industry",
	ss."[SI] Currency" as "Currency (USD / CAD / AUD / EUR)",
	ss."[SI] Obligor Country" as "Obligor Country",
	case when pbb."DIP Loans" = 0 then 'N' when pbb."DIP Loans" = 1 then 'Y' else null end as "DIP Loan (Y/N)",
	case when pbb."Obligations w/ Warrants attached" = 0 then 'N' when pbb."Obligations w/ Warrants attached" = 1 then 'Y' else null end as "Warrants to Purchase Equity (Y/N)",
	case when pbb."Participations" = 0 then 'N' when pbb."Participations" = 1 then 'Y' else null end as "Parti-cipation (Y/N)",
	case when pbb."Convertible into Equity" = 0 then 'N' when pbb."Convertible into Equity" = 1 then 'Y' else null end as "Convertible to Equity (Y/N)",
	pbb."Equity Security" as "Equity Security (Y/N)",
	pbb."Subject of an Offer or Called for Redemption" as "At Acquisition - Subject to offer or called for redemption (Y/N)",
	pbb."Margin Stock" as "Margin Stock (Y/N)",
	pbb."Subject to Withholding Tax" as "Subject to withholding tax (Y/N)",
	pbb."Defaulted Collateral Loan at Acquisition" as "At Acquisition - Defaulted Collateral Loan",
	pbb."Zero Coupon Obligation" as "Zero Coupon Obligation (Y/N)",
	pbb."Covenant Lite" as "Covenant Lite (Y/N)",
	pbb."Structured Finance Obligation / finance lease" as "Structured Finance Obligation, finance lease or chattel paper (Y/N)",
	pbb."Material Non-Credit Related Risk" as "Material Non-Credit Related Risk (Y/N)",
	pbb."Primarily Secured by Real Estate" as "Primarily Secured by Real Estate, Construction Loan or Project Finance Loan (Y/N)",
	pbb."Interest Only Security" as "Interest Only Security (Y/N)",
	pbb."Satisfies Other Criteria(1)" as "Satisfies all Other Eligibility Criteria (Y/N)",
	null as "Excess Concentration Amount (HARD CODE on Last Day of Reinvestment Period)"
from "US Bank Holdings" usbh
left join "Client Holdings" ch on ch."Issuer/Borrower Name" = usbh."Issuer/Borrower Name"
	and ch."Current Par Amount (Issue Currency) - Settled" = usbh."Current Par Amount (Issue Currency) - Settled"
left join "SOI Mapping" sm on sm."Cashfile Security Name" = usbh."Security/Facility Name"
left join "Securities Stats" ss on ss."Security" = sm."Master_Comp Security Name"
left join "PFLT Borrowing Base" pbb on pbb."Security" = ss."Security"
left join "Borrower Stats (Quarterly)" bs on bs."Company" = ss."Family Name"
group by usbh."Issuer/Borrower Name", usbh."Security/Facility Name", pbb."Defaulted Collateral Loan at Acquisition",
	ss."Security", pbb."Credit Improved Loan", usbh."Original Purchase Price", pbb."Stretch Senior (Y/N)", ch."Issue Name",
	ch."Deal Issue (Derived) Rating - Moody's", ch."Deal Issue (Derived) Rating - S&P", bs."[ACM] [C-ACM(AC] Closing Fixed Charge Coverage Ratio",
	bs."[ACM] [C-ACM(AC] Closing Debt to Capitalization", pbb."Senior Debt", pbb."LTM EBITDA", pbb."Total Debt",
	pbb."Closing LTM EBITDA", pbb."Current LTM EBITDA", ch."As Of Date", usbh."Maturity Date", ss."[SI] Type of Rate",
	ss."[SI] LIBOR Floor", bs."[ACM] [COI/LC] S&P Industry", ss."[SI] Currency", ss."[SI] Obligor Country",
	pbb."DIP Loans", pbb."Obligations w/ Warrants attached", pbb."Participations", pbb."Convertible into Equity",
	pbb."Equity Security", pbb."Subject of an Offer or Called for Redemption", pbb."Margin Stock", pbb."Subject to Withholding Tax", pbb."Zero Coupon Obligation",
	pbb."Covenant Lite", pbb."Structured Finance Obligation / finance lease", pbb."Material Non-Credit Related Risk", pbb."Primarily Secured by Real Estate",
	pbb."Interest Only Security", pbb."Satisfies Other Criteria(1)", bs."[ACM] [C-ACM(AC] Closing Fixed Charge Coverage Ratio", bs."[ACM] [C-ACM(AC] 1st Lien Net Debt / EBITDA",
	bs."[CM] [CLSO] 1st Lien Net Debt / EBITDA", bs."[ACM] [C-ACM(AC] HoldCo Net Debt / EBITDA", ss."[SI] Cash Spread to LIBOR", ss."[SI] PIK Coupon"
order by usbh."Security/Facility Name"''')).fetchall())

    base_data_table = {
        "columns": [{"key": column.replace(" ", "_"), "label": column} for column in base_data.columns],
        "data": []
    }
    
    
    for index, row in base_data.iterrows():
        row_data = {}
        
        for col, value in row.items():
            if value != value:
                value = ""
            if isinstance(value, (int, float)):
                    row_data[col.replace(" ", "_")] = value
            elif isinstance(value, datetime):
                row_data[col.replace(" ", "_")] = value.strftime("%Y-%m-%d")
            else:
                row_data[col.replace(" ", "_")] = value
        base_data_table["data"].append(row_data)
    
    return ServiceResponse.success(data=base_data_table, message="Base Data")