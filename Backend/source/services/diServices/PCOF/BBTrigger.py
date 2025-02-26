import os
import pandas as pd
import numpy as np
import datetime
from sqlalchemy import text
import openpyxl
import pickle

from models import db, BaseDataFile, ExtractedBaseDataInfo

from source.utility.ServiceResponse import ServiceResponse
from source.services.PCOF.calculation.functionsCall import calculation_for_build
from source.services.PCOF.PcofDashboardService import PcofDashboardService

pcofDashboardService = PcofDashboardService()

def trigger_pcof_bb(bdi_id):
    try:
        engine = db.get_engine()
        extracted_base_data_info = ExtractedBaseDataInfo.query.filter_by(id=bdi_id).first()
        with engine.connect() as connection:
            base_data_df = pd.DataFrame(connection.execute(text(f'select * from pcof_base_data where base_data_info_id = :ebd_id'), {'ebd_id': bdi_id}).fetchall())
            base_data_mapping_df = pd.DataFrame(connection.execute(text("""select bd_sheet_name, bd_column_name, bd_column_lookup from base_data_mapping bdm where fund_type = 'PCOF'""")))

            base_data_df = base_data_df.replace({np.nan: None})
            report_date = base_data_df['report_date'][0].strftime("%Y-%m-%d")
            base_data_df = base_data_df.drop('report_date', axis=1)
            base_data_df = base_data_df.drop('created_at', axis=1)
            base_data_df = base_data_df.drop('base_data_info_id', axis=1)
            base_data_df = base_data_df.drop('id', axis=1)
            base_data_df = base_data_df.drop('company_id', axis=1)
            base_data_df = base_data_df.drop('created_by', axis=1)
            base_data_df = base_data_df.drop('modified_by', axis=1)
            base_data_df = base_data_df.drop('modified_at', axis=1)

        # base_data_df["Investment Internal Valuation"] = np.nan # complete column is empty
        # base_data_df["Rates PIK"] = np.nan # complete column is empty
        # base_data_df["Classifications Warehouse Asset Inclusion Date"] = np.nan # complete column is empty
        # base_data_df["Leverage Attachment Point"] = np.nan # complete column is empty
        # base_data_df["Final Eligibility Override"] = np.nan # complete column is empty
        # base_data_df["Final Comment"] = np.nan # complete column is empty
        # base_data_df["Concentration Comment"] = np.nan # complete column is empty
        # base_data_df["Borrowing Base Other Adjustment"] = np.nan # complete column is empty
        # base_data_df["Borrowing Base Industry Concentration"] = np.nan # complete column is empty
        # base_data_df["Borrowing Base Comment"] = np.nan # complete column is empty

        # base_data_df["Is Eligible Issuer"] = 'Yes'

        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.title = "PL BB Build"
        file_name = "PCOF Base data - " + report_date + ".xlsx"
        wb.save(file_name)

        path1 = 'PCOF Base data.xlsx'
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
        for index, row in base_data_mapping_df.iterrows():
            rename_df_col[row['bd_column_lookup']] = row['bd_column_name']
        base_data_df.rename(columns=rename_df_col, inplace=True)

        xl_df_map = {}
        xl_df_map['PL BB Build'] = base_data_df

        book = openpyxl.load_workbook(file_name)
        writer = pd.ExcelWriter(file_name, engine="openpyxl")
        writer.book = book
        base_data_df.to_excel(writer, sheet_name="PL BB Build", index=False, header=True)
        writer.save()

        availability_borrower_data = [
            {"A": "Borrower:", "B": "PennantPark Credit Opportunities Fund IV"},
            {"A": "Date of determination:", "B": datetime.datetime(2024, 12, 31, 0, 0, 0)},
            {"A": "Revolving Closing Date", "B": datetime.datetime(2022, 12, 19, 0, 0, 0)},
            {"A": "Commitment Period (3 years from Final Closing Date, as defined in LPA):", "B": "Yes"},
            {"A": "(b) Facility Size:", "B":  240000000},
            {"A": "Loans (USD)", "B":  None},
            {"A": "Loans (CAD)", "B":  None}
        ]
        df_Availability_Borrower = pd.DataFrame(availability_borrower_data)

        subscription_bb_data = [
            {
                "Investor": "Kemper Corporation",
                "Master/Feeder": None,
                "Ultimate Investor Parent": None,
                "Designation": "Institutional Investors",
                "Commitment": 15000000,
                "Capital Called": 6169500
            },
            {
                "Investor": "Teamsters 120",
                "Master/Feeder": None,
                "Ultimate Investor Parent": None,
                "Designation": "Institutional Investors",
                "Commitment": 20000000,
                "Capital Called": 8226000
            },
            {
                "Investor": "Pompano General",
                "Master/Feeder": None,
                "Ultimate Investor Parent": None,
                "Designation": "Institutional Investors",
                "Commitment": 5000000,
                "Capital Called": 2056500
            },
            {
                "Investor": "Miramar Police",
                "Master/Feeder": None,
                "Ultimate Investor Parent": None,
                "Designation": "Institutional Investors",
                "Commitment": 5000000,
                "Capital Called": 2056500
            },
            {
                "Investor": "Plantation Police",
                "Master/Feeder": None,
                "Ultimate Investor Parent": None,
                "Designation": "Institutional Investors",
                "Commitment": 3000000,
                "Capital Called": 1233900
            },
            {
                "Investor": "Lauderhill Police",
                "Master/Feeder": None,
                "Ultimate Investor Parent": None,
                "Designation": "Institutional Investors",
                "Commitment": 4000000,
                "Capital Called": 1645200
            },
            {
                "Investor": "Hollywood Police",
                "Master/Feeder": None,
                "Ultimate Investor Parent": None,
                "Designation": "Institutional Investors",
                "Commitment": 4000000,
                "Capital Called": 1645200
            },
            {
                "Investor": "Cape Coral Police",
                "Master/Feeder": None,
                "Ultimate Investor Parent": None,
                "Designation": "Institutional Investors",
                "Commitment": 5000000,
                "Capital Called": 2056500
            },
            {
                "Investor": "Boynton Beach Employees Pension Plan",
                "Master/Feeder": None,
                "Ultimate Investor Parent": None,
                "Designation": "Institutional Investors",
                "Commitment": 5000000,
                "Capital Called": 2056500
            },
            {
                "Investor": "City of Riviera Beach General Employees Retirement System",
                "Master/Feeder": None,
                "Ultimate Investor Parent": None,
                "Designation": "Institutional Investors",
                "Commitment": 3000000,
                "Capital Called": 1233900
            },
            {
                "Investor": "City of Boca Raton General Employees Pension Plan",
                "Master/Feeder": None,
                "Ultimate Investor Parent": None,
                "Designation": "Institutional Investors",
                "Commitment": 5000000,
                "Capital Called": 2056500
            },
            {
                "Investor": "City of Pompano Beach Police and Firefighters Retirement System",
                "Master/Feeder": None,
                "Ultimate Investor Parent": None,
                "Designation": "Institutional Investors",
                "Commitment": 7000000,
                "Capital Called": 2879100
            },
            {
                "Investor": "Davie Firefighters' Pension Fund",
                "Master/Feeder": None,
                "Ultimate Investor Parent": None,
                "Designation": "Institutional Investors",
                "Commitment": 5000000,
                "Capital Called": 2056500
            },
            {
                "Investor": "City of Riviera Beach Firefighters Retirement System",
                "Master/Feeder": None,
                "Ultimate Investor Parent": None,
                "Designation": "Institutional Investors",
                "Commitment": 3000000,
                "Capital Called": 1233900
            },
            {
                "Investor": "Wayne County Employee Retirement System",
                "Master/Feeder": None,
                "Ultimate Investor Parent": None,
                "Designation": "Institutional Investors",
                "Commitment": 12000000,
                "Capital Called": 4935600
            },
            {
                "Investor": "New England Teamsters & Trucking Industry Pension Fund",
                "Master/Feeder": None,
                "Ultimate Investor Parent": None,
                "Designation": "Institutional Investors",
                "Commitment": 20000000,
                "Capital Called": 8226000
            },
            {
                "Investor": "Moody Gardens",
                "Master/Feeder": None,
                "Ultimate Investor Parent": None,
                "Designation": "Institutional Investors",
                "Commitment": 1000000,
                "Capital Called": 411300
            },
            {
                "Investor": "Mary Moody Northern",
                "Master/Feeder": None,
                "Ultimate Investor Parent": None,
                "Designation": "Institutional Investors",
                "Commitment": 1000000,
                "Capital Called": 411300
            },
            {
                "Investor": "Illinois Municipal Retirement Fund",
                "Master/Feeder": None,
                "Ultimate Investor Parent": None,
                "Designation": "Institutional Investors",
                "Commitment": 50000000,
                "Capital Called": 20565001
            },
            {
                "Investor": "Miami Firefighters Relief and Pension",
                "Master/Feeder": None,
                "Ultimate Investor Parent": None,
                "Designation": "Institutional Investors",
                "Commitment": 10000000,
                "Capital Called": 4113000
            },
            {
                "Investor": "St Lucie County Fire District",
                "Master/Feeder": None,
                "Ultimate Investor Parent": None,
                "Designation": "Institutional Investors",
                "Commitment": 5000000,
                "Capital Called": 2056500
            },
            {
                "Investor": "City of Plantation Employees Retirement System",
                "Master/Feeder": None,
                "Ultimate Investor Parent": None,
                "Designation": "Institutional Investors",
                "Commitment": 5000000,
                "Capital Called": 2056500
            },
            {
                "Investor": "Macomb County Retiree Health Care Trust",
                "Master/Feeder": None,
                "Ultimate Investor Parent": None,
                "Designation": "Institutional Investors",
                "Commitment": 2100000,
                "Capital Called": 863730
            },
            {
                "Investor": "Macomb County Retirement System",
                "Master/Feeder": None,
                "Ultimate Investor Parent": None,
                "Designation": "Institutional Investors",
                "Commitment": 7000000,
                "Capital Called": 2879100
            },
            {
                "Investor": "Macomb County Intermediate Retirees' Medical Benefits",
                "Master/Feeder": None,
                "Ultimate Investor Parent": "",
                "Designation": "Institutional Investors",
                "Commitment": 1750000,
                "Capital Called": 719775
            },
            {
                "Investor": "City of Plantation Volunteer Firefighters Retirement System",
                "Master/Feeder": None,
                "Ultimate Investor Parent": None,
                "Designation": "Institutional Investors",
                "Commitment": 750000,
                "Capital Called": 308475
            },
            {
                "Investor": "Pantheon (Aggregate)",
                "Master/Feeder": None,
                "Ultimate Investor Parent": None,
                "Designation": "Institutional Investors",
                "Commitment": 41000000,
                "Capital Called": 16863301
            },
            {
                "Investor": "Holyoke Retirement Board",
                "Master/Feeder": None,
                "Ultimate Investor Parent": None,
                "Designation": "Institutional Investors",
                "Commitment": 5000000,
                "Capital Called": 2056500
            },
            {
                "Investor": "City of Delray Beach Police Retirement System",
                "Master/Feeder": None,
                "Ultimate Investor Parent": None,
                "Designation": "Institutional Investors",
                "Commitment": 3000000,
                "Capital Called": 1233900
            },
            {
                "Investor": "City of Hialeah Employees' Retirement System",
                "Master/Feeder": None,
                "Ultimate Investor Parent": None,
                "Designation": "Institutional Investors",
                "Commitment": 5000000,
                "Capital Called": 2056500
            },
            {
                "Investor": "Town of Jupiter Police Officers' Retirement Fund",
                "Master/Feeder": None,
                "Ultimate Investor Parent": None,
                "Designation": "Institutional Investors",
                "Commitment": 3000000,
                "Capital Called": 1233900
            }
        ]
        df_subscription_bb = pd.DataFrame(subscription_bb_data)
        df_subscription_bb["Uncalled Capital"] = (df_subscription_bb["Commitment"] - df_subscription_bb["Capital Called"])
        total_capitalCalled = df_subscription_bb["Capital Called"].sum()
        total_uncalled_Capital = df_subscription_bb["Uncalled Capital"].sum()

        input_other_metrics_data = [
            {
                "Other Metrics": "First Lien Leverage Cut-Off Point",
                "values": 4.0
            },
            {
                "Other Metrics": "Warehouse First Lien Leverage Cut-Off",
                "values": 4.5
            },
            {
                "Other Metrics": "Last Out Attachment Point",
                "values": 2.25
            },
            {
                "Other Metrics": "1 out of 2 Test",
                "values": None
            },
            {
                "Other Metrics": "Trailing 12-Month EBITDA",
                "values": 10.0
            },
            {
                "Other Metrics": "Trailing 24-Month EBITDA",
                "values": 20.0
            },
            {
                "Other Metrics": "Total Leverage",
                "values": 4.5
            },
            {
                "Other Metrics": "LTV",
                "values": 0.65
            },
            {
                "Other Metrics": "Concentration Test Threshold 1",
                "values": 0.075
            },
            {
                "Other Metrics": "Concentration Test Threshold 1",
                "values": 0.010
            },
            {
                "Other Metrics": "Threshold 1 Advance Rate",
                "values": 0.50
            },
            {
                "Other Metrics": "Threshold 2 Advance Rate",
                "values": 0.0
            }
        ]
        df_Inputs_Other_Metrics = pd.DataFrame(input_other_metrics_data)

        inputs_portfolio_lev_bb_data = [
            {
                "Investment Type": "Cash",
                "Unquoted": None,
                "Quoted": 1.0
            },
            {
                "Investment Type": "Cash Equivalent",
                "Unquoted": None,
                "Quoted": 1.0
            },
            {
                "Investment Type": "LT US Debt",
                "Unquoted": None,
                "Quoted": 0.85
            },
            {
                "Investment Type": "First Lien",
                "Unquoted": 0.65,
                "Quoted": 0.75
            },
            {
                "Investment Type": "Warehouse First Lien",
                "Unquoted": 0.70,
                "Quoted": 0.75
            },
            {
                "Investment Type": "Last Out",
                "Unquoted": 0.55,
                "Quoted": 0.65
            },
            {
                "Investment Type": "Second Lien",
                "Unquoted": 0.50,
                "Quoted": 0.60
            },
            {
                "Investment Type": "High Yield",
                "Unquoted": 0.45,
                "Quoted": 0.55
            },
            {
                "Investment Type": "Mezzanine",
                "Unquoted": 0.40,
                "Quoted": 0.50
            },
            {
                "Investment Type": "Cov-Lite",
                "Unquoted": 0.40,
                "Quoted": 0.50
            },
            {
                "Investment Type": "PIK",
                "Unquoted": 0.35,
                "Quoted": 0.40
            },
            {
                "Investment Type": "Preferred Stock",
                "Unquoted": 0.20,
                "Quoted": 0.30
            },
            {
                "Investment Type": "Equity",
                "Unquoted": 0.0,
                "Quoted": 0.0
            }
        ]
        df_Inputs_Portfolio_LeverageBorrowingBase = pd.DataFrame(inputs_portfolio_lev_bb_data)

        obligors_net_capital_data =[
            {
                "Obligors' Net Capital": "Equity Paid in Capital",
                "Values": 125000000
            },
            {
                "Obligors' Net Capital": "Distributions",
                "Values": None
            },
            {
                "Obligors' Net Capital": "Retained Earnings",
                "Values": 11666422
            },
            {
                "Obligors' Net Capital": "(a) Partners' Capital",
                "Values": 136666422
            },
            {
                "Obligors' Net Capital": "(b) Uncalled Capital Commitments (excl. Defaulting Investors)",
                "Values": 178914408
            },
            {
                "Obligors' Net Capital": "Obligors' Net Capital ((a) + (b))",
                "Values": 315580830
            },
            {
                "Obligors' Net Capital": "Debt / Equity",
                "Values": 1.65
            }
        ]
        df_Obligors_Net_Capital = pd.DataFrame(obligors_net_capital_data)

        df_PL_BB_Build = base_data_df.copy()

        # for now, hardcodedly adding cash row
        cash_row_data = {
            'Investment Name': ['Cash'], 
            'Issuer': ['Cash'], 
            'Investment Investment Type': ['Cash'],
            'Investment Industry': ['Cash'], 
            'Investment Closing Date': [None], 
            'Investment Maturity': [None],
            'Investment Par': [7489255], 
            'Investment Cost': [7489255], 
            'Investment External Valuation': [7489255],
            'Investment Internal Valuation': [7489255], 
            'Rates Fixed Coupon': [None],
            'Rates Floating Cash Spread': [None], 
            'Rates Current LIBOR/Floor': [None], 
            'Rates PIK': [None],
            'Rates Fixed / Floating': ['Floating'], 
            'Classifications Quoted / Unquoted': ['Quoted'],
            'Classifications Warehouse Asset': ['No'],
            'Classifications Warehouse Asset Inclusion Date': [pd.NaT],
            'Classifications Warehouse Asset Expected Rating': [None],
            'Classifications Approved Foreign Jurisdiction': ['NA'],
            'Classifications LTV Transaction': ['No'],
            'Classifications Noteless Assigned Loan': ['No'],
            'Classifications Undelivered Note': ['No'],
            'Classifications Structured Finance Obligation': ['No'],
            'Classifications Third Party Finance Company': ['No'],
            'Classifications Affiliate Investment': ['No'],
            'Classifications Defaulted / Restructured': ['No'],
            'Financials LTM Revenue ($MMs)': [None], 
            'Financials LTM EBITDA ($MMs)': [None],
            'Leverage Revolver Commitment': [None], 
            'Leverage Total Enterprise Value': [None],
            'Leverage Total Leverage': [None], 
            'Leverage PCOF IV Leverage': [None],
            'Leverage Attachment Point': [None], 
            'Leverage Total Capitalization': [None],
            'Leverage LTV Thru PCOF IV': [None], 
            'Final Eligibility Override': [None],
            'Final Comment': [None], 
            'Concentration Adjustment': [None], 
            'Concentration Comment': [None],
            'Borrowing Base Other Adjustment': [None],
            'Borrowing Base Industry Concentration': [None], 
            'Borrowing Base Comment': [None],
            'Is Eligible Issuer': [None]
        }
        
        cash_row_df = pd.DataFrame(cash_row_data)

        cash_row_df = cash_row_df.reindex(columns=df_PL_BB_Build.columns)
        # Concatenate df_PL_BB_Build and uploaded_df
        df_PL_BB_Build = pd.concat([df_PL_BB_Build, cash_row_df], ignore_index=True)
        df_PL_BB_Build.reset_index(drop=True, inplace=True)

        df_PL_BB_Build[["Classifications Structured Finance Obligation", 
                        "Classifications Third Party Finance Company", 
                        "Classifications Affiliate Investment", 
                        "Classifications Defaulted / Restructured"]].fillna('') # Note: This initialized to '', value must be asked.
        
        df_PL_BB_Build[["Final Eligibility Override"]].fillna('') # Note: This initialized to '', value must be asked.

        df_PL_BB_Build["Investment Cost"] = df_PL_BB_Build["Investment Cost"].astype(float)
        df_PL_BB_Build[["Investment Cost"]].fillna(0)
        df_PL_BB_Build["Investment Par"] = df_PL_BB_Build["Investment Cost"].astype(float)
        df_PL_BB_Build[["Investment Par"]].fillna(0)

        df_PL_BB_Build["Leverage PCOF IV Leverage"].fillna(0, inplace=True)

        df_PL_BB_Build["Rates Fixed Coupon"] = pd.to_numeric(df_PL_BB_Build["Rates Fixed Coupon"], errors='coerce')
        df_PL_BB_Build["Rates Fixed Coupon"] = df_PL_BB_Build["Rates Fixed Coupon"].fillna(0).astype(int)

        df_PL_BB_Build["Rates Current LIBOR/Floor"] = pd.to_numeric(df_PL_BB_Build["Rates Current LIBOR/Floor"], errors='coerce')
        df_PL_BB_Build["Rates Current LIBOR/Floor"] = df_PL_BB_Build["Rates Current LIBOR/Floor"].fillna(0).astype(int)

        df_PL_BB_Build["Rates Floating Cash Spread"] = pd.to_numeric(df_PL_BB_Build["Rates Floating Cash Spread"], errors='coerce')
        df_PL_BB_Build["Rates Floating Cash Spread"] = df_PL_BB_Build["Rates Floating Cash Spread"].fillna(0).astype(int)

        

        # df_PL_BB_Build = calculation_for_build(
        #     df_PL_BB_Build, 
        #     df_Inputs_Other_Metrics, 
        #     df_Availability_Borrower,
        #     total_capitalCalled,
        #     df_Inputs_Portfolio_LeverageBorrowingBase,
        #     total_uncalled_Capital,
        #     df_Obligors_Net_Capital
        # ) # For now, checking PL BB Build

        xl_df_map = {
            "PL BB Build": df_PL_BB_Build,
            "Other Metrics": df_Inputs_Other_Metrics,
            "Availability Borrower": df_Availability_Borrower,
            "Portfolio LeverageBorrowingBase": df_Inputs_Portfolio_LeverageBorrowingBase,
            "Obligors' Net Capital": df_Obligors_Net_Capital
        }
        pickled_xl_df_map = pickle.dumps(xl_df_map)

        included_excluded_assets = pcofDashboardService.pcof_included_excluded_assets(xl_df_map)

        dt_string = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        base_data_file = BaseDataFile(
            user_id=1,
            file_data=pickled_xl_df_map,
            fund_type='PCOF',
            file_name ='Generated Data '+dt_string,
            included_excluded_assets_map=included_excluded_assets,
            closing_date=extracted_base_data_info.report_date
        )
        db.session.add(base_data_file)
        db.session.commit()

        wb2.close()
        writer.close()
        os.remove(file_name)

        return ServiceResponse.success(message="Succesfully processed PL BB Build")


    except Exception as e:
        print(str(e))
        return {
            "success": False,
            "message": "Something went wrong while executing borrowing base trigger for PCOF"
        }
       