import pandas as pd
from sqlalchemy import text

from source.utility.Log import Log
from source.utility.ServiceResponse import ServiceResponse

def map_and_store_base_data(engine, extracted_base_data_info, master_comp_file_details, cash_file_details, market_book_file_details):
    try:
        print("storing base data of pcof")
        with engine.connect() as connection:
            pcof_base_data = pd.DataFrame(connection.execute(text(f'''
                select distinct
                    --usbh."Security/Facility Name" as "investment_name",
                    ss."Security" as investment_name,
                    usbh."Issuer/Borrower Name"  as "issuer",
                    case
						when lien_master.lien_type is null then ss."[SI] Credit Facility Lien Type"
						else lien_master.lien_type
					end
					as "investment_investment_type",
                    bs."[ACM] [COI/LC] PNNT Industry" as "investment_industry",
                    bs."[ACM] [COI/LC] Closing Date" as "investment_closing_date",
                    case when ss."[SI] Maturity" is not null and ss."[SI] Maturity" != 'NM' then ss."[SI] Maturity" else null end as "investment_maturity",
                --    sum(usbh."P. Lot Current Par Amount (Deal Currency)"::float) as "investment_par", -- selecting this column for now
                    ssm."Commitment" as "investment_par",
                --    sum(ssmb."Book Value"::float)  as "investment_cost", -- could not map -- considering null for now
                    ssm."BookValue" as "investment_cost",
                --    sum(ssmb."Market Value"::float)  as "investment_external_valuation", -- could not map -- considering null for now
                    ssm."MarketValue"  as "investment_external_valuation",
                    null as "investment_internal_valuation", -- Complete column is empty
                    ss."[SI] PIK Coupon" as "rates_fixed_coupon",
                    ss."[SI] Cash Spread to LIBOR" as "rates_floating_cash_spread",
                    ss."[SI] LIBOR Floor" as "rates_current_lobor_floor",
                    null as "rates_pik", -- Complete column is empty
                    case
                        when ss."[SI] Type of Rate" like 'Fixed Rate%' then 'Fixed'
                        when ss."[SI] Type of Rate" like 'Floating Rate%' then 'Floating'
                    end
                        as "rates_fixed_floating",
                    case 
                        when ss."[SI] Broker / Dealer Quoted" = 'Yes' then 'Quoted'
                        else 'Unquoted'
                    end as "classifications_quoted_unquoted",
                    case 
                        when ss."[PSM] Defaulted / Restructured?" = 'Yes' then 'Yes'
                        else 'No'
                    end as "classifications_defaulted_restructured",
                    ss."[C] LTM Rev" as "financials_ltm_revenue_mms",
                    ss."EBITDA" as "financials_ltm_ebitda_mms",
                    null as "leverage_revolver_commitment", -- could not map -- considering null for now
                    ss."[PSM] TEV" as "leverage_total_enterprise_value",
                    ss."Total Gross Leverage" as "leverage_total_leverage",
                    case
                        when ss."Pennant Gross Leverage" is null or ss."Pennant Gross Leverage" = 'NM' then null
                        else ss."Pennant Gross Leverage"
                    end as "leverage_pcof_iv_leverage",
                    ss."[PSM] Capitalization Multiple" as "leverage_total_capitalization",
                    ss."LTV" as "leverage_ltv_thru_pcof_iv", -- was from PCOF IV, Now taking from security stats (BU)
                    'Yes' as "is_eligible_issuer", -- could not map
                    STRING_AGG(ch."LoanX ID", ', ') AS loanx_id
                from sf_sheet_us_bank_holdings usbh
                left join sf_sheet_client_Holdings ch on ch."Issuer/Borrower Name" = usbh."Issuer/Borrower Name"
                    and ch."Current Par Amount (Issue Currency) - Settled" = usbh."Current Par Amount (Issue Currency) - Settled"
                left join pflt_security_mapping sm on sm.cashfile_security_name = usbh."Security/Facility Name"
                left join sf_sheet_securities_stats ss on ss."Security" = sm.master_comp_security_name
                left join sf_sheet_borrower_stats bs on bs."Company" = ss."Family Name"
                left join lien_type_mapping lien_mapping on lien_mapping.lien_type = ss."[SI] Credit Facility Lien Type" and (lien_mapping.is_deleted = false or lien_mapping.is_deleted is null)
				left join lien_type_master lien_master on lien_master.id = lien_mapping.master_lien_type_id
                left join 
	                (select loan_mapping_cashfile.loan_type, loan_master_cashfile.loan_type as master_loan_type from loan_type_mapping loan_mapping_cashfile
		                left join loan_type_master loan_master_cashfile on loan_master_cashfile.id = loan_mapping_cashfile.master_loan_type_id
		                where (loan_mapping_cashfile.is_deleted = false or loan_mapping_cashfile.is_deleted is null) and loan_master_cashfile.fund_type = 'PCOF')
                    as t2 on t2.loan_type = ch."Issue Name"
                left join 
	                (select *, loan_master_marketbook.loan_type as master_loan_type from sf_sheet_marketbook_1 ssm 
			            left join loan_type_mapping loan_mapping_marketbook on loan_mapping_marketbook.loan_type = ssm."Asset_Name" and (loan_mapping_marketbook.is_deleted = false or loan_mapping_marketbook.is_deleted is null)
			            left join loan_type_master loan_master_marketbook on loan_master_marketbook.id = loan_mapping_marketbook.master_loan_type_id and loan_master_marketbook.fund_type = 'PCOF'
			            where ssm.source_file_id = :market_book_file_id)
                    as ssm on lower(regexp_replace(ch."Issuer/Borrower Name", '[^a-zA-Z0-9]','', 'g')) = lower(regexp_replace(ssm."Issuer_Name", '[^a-zA-Z0-9]','', 'g')) and t2.master_loan_type = ssm.master_loan_type
                where (usbh.source_file_id = :cash_file_id AND ch.source_file_id = :cash_file_id and (ssm.source_file_id is null or ssm.source_file_id = :market_book_file_id)) and
                ((sm.id is not null AND ss.source_file_id = :master_comp_file_id AND bs.source_file_id = :master_comp_file_id) or sm.id is null)
                group by sm.id, ss."Security", usbh."Security/Facility Name", usbh."Issuer/Borrower Name", ss."[SI] Credit Facility Lien Type", bs."[ACM] [COI/LC] PNNT Industry",
                bs."[ACM] [COI/LC] Closing Date", ss."[SI] Maturity",
                    ss."[SI] PIK Coupon",
                    ss."[SI] Cash Spread to LIBOR",
                    ss."[SI] LIBOR Floor",
                    ss."[SI] Type of Rate",
                    ss."[C] LTM Rev",
                    ss."EBITDA",
                    ss."[PSM] TEV",
                    ss."Total Gross Leverage",
                    ss."Pennant Gross Leverage",
                    ss."[SI] Broker / Dealer Quoted",
                    ss."[PSM] Defaulted / Restructured?",
                    ss."[PSM] Capitalization Multiple",
                    ss."LTV",
                    ssm."Commitment",
                    ssm."BookValue",
                    ssm."MarketValue",
                    lien_master.lien_type
                order by ss."Security"
            '''), {'cash_file_id': cash_file_details.id, 'master_comp_file_id': master_comp_file_details.id, 'market_book_file_id': market_book_file_details.id}))

        if pcof_base_data.empty:
                raise Exception('Base data is empty')
        pcof_base_data["base_data_info_id"] = extracted_base_data_info.id
        pcof_base_data["company_id"] = master_comp_file_details.company_id
        pcof_base_data["report_date"] = master_comp_file_details.report_date
        # df.to_csv('file1.csv')
        pcof_base_data.to_sql("pcof_base_data", con=engine, if_exists='append', index=False, method='multi')
        
        return ServiceResponse.success(message=f"Successfully stored base data from pcof for extracted_base_data_info.id {extracted_base_data_info.id}")
    except Exception as e:
        Log.func_error(e=e)
        print(f"Could not map and store data from sheet table for extracted_base_data_info.id {extracted_base_data_info.id}")
        ServiceResponse.error(message=f"Could not map and store data from sheet table for extraction_info_id {extracted_base_data_info.id}")