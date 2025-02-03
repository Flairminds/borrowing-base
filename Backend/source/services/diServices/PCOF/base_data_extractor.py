import pandas as pd
from sqlalchemy import text

from source.utility.Log import Log
from source.utility.ServiceResponse import ServiceResponse
def map_and_store_base_data(engine, extracted_base_data_info, source_file_details):
    try:
        print("storing base data of pcof")
        with engine.connect() as connection:
            pcof_base_data = pd.DataFrame(connection.execute(text(f'''select distinct
	            ppi."Asset" as "investment_name",
	            ppi."MC Name" as "issuer",
	            ppi."LTV"  as "leverage_ltv_thru_pcof_iv",
	            ppibb."Quoted / Unquoted" as "classifications_quoted_unquoted",
	            ppibb."Warehouse Yes / No" as "classifications_warehouse_asset",
	            ppibb."Warehouse - Credit Rating" as "classifications_warehouse_asset_expected_rating",
	            ppibb."Approved Foreign Jurisdiction" as "classifications_approved_foreign_jurisdiction",
	            ppibb."LTV Transaction" as "classifications_ltv_transaction",
	            ppibb."Noteless Assigned Loan" as "Classifications_noteless_assigned_loan",
	            ppibb."Undelivered Note" as "classifications_undelivered_note",
	            ppibb."Structured Finance Obligation" as "classifications_structured_finance_obligation",
                ppibb."Third Party Finance Company" as "classifications_third_party_finance_company",
                ppibb."Affiliate Investment" as "classifications_affiliate_investment",
                ppibb."Defaulted / Restructured" as "classifications_defaulted_restructured",
                ppibb."TotalCapitalization" as "leverage_total_capitalization"
            from pcof_pcof_iv ppi
            left join pcof_pcof_iii_borrrowing_base ppibb on ppibb."Family Name" = ppi."MC Name" 
            where ppi.source_file_id = :source_file_details_id --and ppibb.source_file_id  = 112
            order by ppi."Asset"'''), {'source_file_details_id': source_file_details.id}))

        if pcof_base_data.empty:
                raise Exception('Base data is empty')
        pcof_base_data["base_data_info_id"] = extracted_base_data_info.id
        pcof_base_data["company_id"] = source_file_details.company_id
        pcof_base_data["report_date"] = source_file_details.report_date
        # df.to_csv('file1.csv')
        pcof_base_data.to_sql("pcof_base_data", con=engine, if_exists='append', index=False, method='multi')
        
        return ServiceResponse.success(message=f"Successfully stored base data from pcof for extracted_base_data_info.id {extracted_base_data_info.id}")
    except Exception as e:
        Log.func_error(e=e)
        print(f"Could not map and store data from sheet table for extracted_base_data_info.id {extracted_base_data_info.id}")
        ServiceResponse.error(message=f"Could not map and store data from sheet table for extraction_info_id {extracted_base_data_info.id}")