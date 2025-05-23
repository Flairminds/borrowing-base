import pandas as pd
import numpy as np
from datetime import datetime
import pickle
import json
from sqlalchemy import text

from models import db, BaseDataFile
from source.services.PSSL.pssl_calculation_initiator import PsslCalculationInitiator
from source.utility.ServiceResponse import ServiceResponse
from models import db, ExtractedBaseDataInfo, BaseDataOtherInfo, VaeData
from source.utility.Log import Log
pssl_calculation_initiator = PsslCalculationInitiator()

def trigger_pssl_bb(bdi_id):
    try:
        engine = db.get_engine()
        extracted_base_data_info = ExtractedBaseDataInfo.query.filter_by(id=bdi_id).first()
        base_data_other_info = BaseDataOtherInfo.query.filter_by(extraction_info_id=bdi_id).first()

        vae_info = VaeData.query.all()

        vae_dicts = [row.__dict__ for row in vae_info]

        for row in vae_dicts:
            row.pop('_sa_instance_state', None)

        vae_df = pd.DataFrame(vae_dicts)
        with engine.connect() as connection:
            base_data_df = pd.DataFrame(connection.execute(text(f"select * from pssl_base_data where base_data_info_id = :ebd_id"), {'ebd_id': bdi_id}).fetchall())
            base_data_mapping_df = pd.DataFrame(connection.execute(text("""select bd_sheet_name, bd_column_name, bd_column_lookup from base_data_mapping bdm where fund_type = 'PSSL' and bd_sheet_name = 'Portfolio'""")))

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
        
        rename_df_col = {}
        for index, row in base_data_mapping_df.iterrows():
            rename_df_col[row['bd_column_lookup']] = row['bd_column_name']
        base_data_df.rename(columns=rename_df_col, inplace=True)

        base_data_df["Admin Agent Approval (RCF)"] = "No"
        base_data_df["Admin Agent Add-Back Discretion"] = "N"
        base_data_df["Admin Agent Approved Add-Backs"] = 0
        base_data_df["Date of Financial Delivery VAE"] = None
        base_data_df["Date Financials Provided to Ally"] = None
        # base_data_df["Current Cash Interest Expense"] = 1
        # datatype of following columns should get handled in query itself
        base_data_df["RCF Update Date"] = pd.to_datetime(base_data_df["RCF Update Date"])
        base_data_df['Borrower Outstanding Principal Balance'] = pd.to_numeric(base_data_df['Borrower Outstanding Principal Balance'], errors='coerce')
        base_data_df["Initial Unrestricted Cash (Local Currency)"] = pd.to_numeric(base_data_df["Initial Unrestricted Cash (Local Currency)"], errors='coerce')
        base_data_df["Borrower Facility Commitment"] = pd.to_numeric(base_data_df["Borrower Facility Commitment"], errors='coerce')
        # base_data_df["Acquisition Date"] = datetime(2023, 7, 28)
        # base_data_df["Maturity Date"] = datetime(2028, 4, 21)

        availability_data = [
            {"Terms": "Determination Date", "Values": datetime.strptime(base_data_other_info.other_info_list.get('availability').get('determination_date')[:-5], "%Y-%m-%dT%H:%M:%S")},
            {"Terms": "Measurement Date:", "Values": datetime.strptime(base_data_other_info.other_info_list.get('availability').get('measurement_date')[:-5], "%Y-%m-%dT%H:%M:%S")},
            {"Terms": "Facility Amount ($)", "Values": float(base_data_other_info.other_info_list.get('availability').get('facility_amount'))},
            {"Terms": "On Deposit in Unfunded Exposure Account", "Values": base_data_other_info.other_info_list.get('availability').get('on_deposit_in_unfunded_exposure_account')},
            {"Terms": "Foreign Currency hedged by Borrower", "Values":  base_data_other_info.other_info_list.get('availability').get('foreign_currency_hedged_by_borrower')},
            {"Terms": "Current Advances Outstanding", "Values":  float(base_data_other_info.other_info_list.get('availability').get('current_advances_outstanding'))},
            {"Terms": "Advances Repaid", "Values":  float(base_data_other_info.other_info_list.get('availability').get('advances_repaid'))},
            {"Terms": "Advances Requested", "Values":  float(base_data_other_info.other_info_list.get('availability').get('advances_requested'))},
            {"Terms": "Cash on deposit in Principal Collections Account ($)", "Values":  float(base_data_other_info.other_info_list.get('availability').get('cash_on_deposit_in_principal_collections_account'))}
        ]
        availability_df = pd.DataFrame(availability_data)

        exchange_rates_data = [
            {
                "Currency": exchange_rates_value.get('currency'),
                "Exchange Rate": float(exchange_rates_value.get('exchange_rates')),
            } for exchange_rates_value in base_data_other_info.other_info_list.get('exchange_rates')]
        exchange_rates_df = pd.DataFrame(exchange_rates_data)

        # obligor_tiers_data = [
        #     {
        #         "Obligor": obligor_tiers_value.get('obligor'),
        #         "First Lien Loans": float(obligor_tiers_value.get('first_lien_loans')),
        #         "FLLO/2nd Lien Loans": float(obligor_tiers_value.get('fllo_2nd_lien_loans')),
        #         "Recurring Revenue": float(obligor_tiers_value.get('recurring_revenue')),
        #         "Applicable Collateral Value": float(obligor_tiers_value.get('applicable_collateral_value')),
        #     } for obligor_tiers_value in base_data_other_info.other_info_list.get('obligor_tiers')]
        # obligor_tiers_df = pd.DataFrame(obligor_tiers_data)

        obligor_understandings = [
            {"Terms": "First Lien < $10MM", "Values": base_data_other_info.other_info_list.get('obligor_outstandings').get('first_lien_10mm')},
            {"Terms": "First Lien < $10MM, Senior Leverage in excess of 6.5x", "Values": base_data_other_info.other_info_list.get('obligor_outstandings').get('first_lien_10mm_senior_leverage_in_excess_of_6_5x')},
            {"Terms": "First Lien < $10MM, Senior Leverage in excess of 7.5x", "Values": base_data_other_info.other_info_list.get('obligor_outstandings').get('first_lien_10mm_senior_leverage_in_excess_of_7_5x')},
            {"Terms": "First Lien ≥ $10MM and < $50MM", "Values": base_data_other_info.other_info_list.get('obligor_outstandings').get('first_lien_10mm_and_50mm')},
            {"Terms": "First Lien ≥ $10MM and < $50MM, Senior Leverage in excess of 6.5x", "Values": base_data_other_info.other_info_list.get('obligor_outstandings').get('first_lien_10mm_and_50mm_senior_leverage_in_excess_of_6_5x')},
            {"Terms": "First Lien ≥ $10MM and < $50MM, Senior Leverage in excess of 7.5x", "Values": base_data_other_info.other_info_list.get('obligor_outstandings').get('first_lien_10mm_and_50mm_senior_leverage_in_excess_of_7_5x')},
            {"Terms": "First Lien ≥ $50MM & Unrated", "Values": base_data_other_info.other_info_list.get('obligor_outstandings').get('first_lien_50mm_unrated')},
            {"Terms": "First Lien ≥ $50MM & Unrated, Senior Leverage in excess of 6.5x", "Values": base_data_other_info.other_info_list.get('obligor_outstandings').get('first_lien_50mm_unrated_senior_leverage_in_excess_of_6_5x')},
            {"Terms": "First Lien ≥ $50MM & Unrated, Senior Leverage in excess of 7.5x", "Values": base_data_other_info.other_info_list.get('obligor_outstandings').get('first_lien_50mm_unrated_senior_leverage_in_excess_of_7_5x')},
            {"Terms": "First Lien ≥ $50MM & B- or better", "Values": base_data_other_info.other_info_list.get('obligor_outstandings').get('first_lien_50mm_b_or_better')},
            {"Terms": "First Lien ≥ $50MM & B- or better, Senior Leverage in excess of 6.5x", "Values": base_data_other_info.other_info_list.get('obligor_outstandings').get('first_lien_50mm_b_or_better_senior_leverage_in_excess_of_6_5x')},
            {"Terms": "First Lien ≥ $50MM & B- or better, Senior Leverage in excess of 7.5x", "Values": base_data_other_info.other_info_list.get('obligor_outstandings').get('first_lien_50mm_b_or_better_senior_leverage_in_excess_of_7_5x')},
            {"Terms": "Last Out", "Values": base_data_other_info.other_info_list.get('obligor_outstandings').get('last_out')},
            {"Terms": "Last Out Total Leverage in excess of 7.5x", "Values": base_data_other_info.other_info_list.get('obligor_outstandings').get('last_out_total_leverage_in_excess_of_7_5_x')},
            {"Terms": "Second Lien", "Values": base_data_other_info.other_info_list.get('obligor_outstandings').get('second_lien')},
            {"Terms": "Second Lien Total Leverage in excess of 7.5x", "Values": base_data_other_info.other_info_list.get('obligor_outstandings').get('second_lien_total_leverage_in_excess_of_7_5_x')},
            {"Terms": "Recurring Revenue", "Values": base_data_other_info.other_info_list.get('obligor_outstandings').get('recurring_revenue')},
            {"Terms": "Recurring Revenue, Amounts above 2.5x", "Values": base_data_other_info.other_info_list.get('obligor_outstandings').get('recurring_revenue_amounts_above_2_5_x')},
            {"Terms": "Ineligible", "Values": base_data_other_info.other_info_list.get('obligor_outstandings').get('ineligible')},
        ]
        obligor_understandings_df = pd.DataFrame(obligor_understandings)

        # obligor_tiers_ebitda = [
        #     {
        #         "EBITDA": obligor_tiers_ebitda_value.get('ebitda'),
        #         "Absolute Value": float(obligor_tiers_ebitda_value.get('absolute_value')) if obligor_tiers_ebitda_value.get('absolute_value') is not None else None,
        #         "Debt-to-Cash Capitalization Ratio": float(obligor_tiers_ebitda_value.get('debt_to_cash_capitalization_ratio')),
        #         "Permitted Add-Backs": float(obligor_tiers_ebitda_value.get('permitted_add_backs')),
        #     } for obligor_tiers_ebitda_value in base_data_other_info.other_info_list.get('obligor_tiers_ebitda')]
        # obligor_tiers_ebitda_df = pd.DataFrame(obligor_tiers_ebitda)

        path1 = 'PSSL_Base_Data.xlsx'
        base_data_dict = pd.read_excel(path1, sheet_name=None)
        base_data_dict["Portfolio"] = base_data_df
        base_data_dict["Availability"] = availability_df
        base_data_dict["Exchange Rates"] = exchange_rates_df
        base_data_dict["VAE"] = vae_df
        # base_data_dict["Obligor Tiers"] = obligor_tiers_df


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