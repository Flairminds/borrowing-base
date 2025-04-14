import pandas as pd
from sqlalchemy import text

from source.utility.Log import Log
from source.utility.ServiceResponse import ServiceResponse

def map_and_store_base_data(engine, extracted_base_data_info, master_comp_file_details, cash_file_details, market_book_file_details):
    try:
        print("storing base data of pcof")
        with engine.connect() as connection:
            pcof_base_data = pd.DataFrame(connection.execute(text(f'''
                select 
                    distinct usbh."Security/Facility Name" as "investment_name",
                    usbh."Issuer/Borrower Name"  as "issuer",
                    case
						when lien_master.lien_type is null then ss."[SI] Credit Facility Lien Type"
						else lien_master.lien_type
					end
					as "investment_investment_type",
                    bs."[ACM] [COI/LC] PNNT Industry" as "investment_industry",
                    bs."[ACM] [COI/LC] Closing Date" as "investment_closing_date",
                    ss."[SI] Maturity" as "investment_maturity",
                --    sum(usbh."P. Lot Current Par Amount (Deal Currency)"::float) as "investment_par", -- selecting this column for now
                    ssmb."Commitment" as "investment_par",
                --    sum(ssmb."Book Value"::float)  as "investment_cost", -- could not map -- considering null for now
                    ssmb."BookValue" as "investment_cost",
                --    sum(ssmb."Market Value"::float)  as "investment_external_valuation", -- could not map -- considering null for now
                    ssmb."MarketValue"  as "investment_external_valuation",
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
                        when sspibb."Quoted / Unquoted" is null or sspibb."Quoted / Unquoted" = '0' or sspibb."Quoted / Unquoted" = 'No' then 'Unquoted'
                        when sspibb."Quoted / Unquoted" = '1' or sspibb."Quoted / Unquoted" = 'Yes' then 'Quoted'
                        else sspibb."Quoted / Unquoted"
                    end as "classifications_quoted_unquoted", -- from PCOF III Borrrowing Base
                    case 
                        when sspibb."Warehouse Yes / No" is null then 'No'
                        when sspibb."Warehouse Yes / No" like '0' then 'No'
                        when sspibb."Warehouse Yes / No" like '1' then 'Yes'
                        else sspibb."Warehouse Yes / No"
                    end
                    as "classifications_warehouse_asset", -- from PCOF III Borrrowing Base
                    null as "classifications_warehouse_asset_inclusion_date", -- could not map -- Complete column is empty
                    sspibb."Warehouse - Credit Rating" as "classifications_warehouse_asset_expected_rating", -- from PCOF III Borrrowing Base
                    case
                        when sspibb."Approved Foreign Jurisdiction" is null then 'NA'
                        else sspibb."Approved Foreign Jurisdiction"
                    end as "classifications_approved_foreign_jurisdiction", -- from PCOF III Borrrowing Base
                    case
                        when sspibb."LTV Transaction" is null or sspibb."LTV Transaction" = '0'  then 'No'
                        else sspibb."LTV Transaction"
                    end as "classifications_ltv_transaction", -- from PCOF III Borrrowing Base
                    case
                        when sspibb."Noteless Assigned Loan" is null then 'No'
                        else sspibb."Noteless Assigned Loan"
                    end as "classifications_noteless_assigned_loan", -- from PCOF III Borrrowing Base
                    case
                        when sspibb."Undelivered Note" is null then 'No'
                        else sspibb."Undelivered Note"
                    end as "classifications_undelivered_note", -- from PCOF III Borrrowing Base
                    case
                        when sspibb."Structured Finance Obligation" is null then 'No'
                        else sspibb."Structured Finance Obligation"
                    end as "classifications_structured_finance_obligation", -- from PCOF III Borrrowing Base
                    case
                        when sspibb."Third Party Finance Company" is null then 'No'
                        else sspibb."Third Party Finance Company"
                    end as "classifications_third_party_finance_company", -- from PCOF III Borrrowing Base
                    case 
                        when sspibb."Affiliate Investment" is null then 'No'
                        else sspibb."Affiliate Investment"
                    end as "classifications_affiliate_investment", -- from PCOF III Borrrowing Base
                    case 
                        when sspibb."Defaulted / Restructured" is null then 'No'
                        else sspibb."Defaulted / Restructured"
                    end as "classifications_defaulted_restructured", -- from PCOF III Borrrowing Base
                    ss."[C] LTM Rev" as "financials_ltm_revenue_mms",
                    ss."EBITDA" as "financials_ltm_ebitda_mms",
                    null as "leverage_revolver_commitment", -- could not map -- considering null for now
                    ss."[PSM] TEV" as "leverage_total_enterprise_value",
                    ss."Total Gross Leverage" as "leverage_total_leverage",
                    case
                        when ss."Pennant Gross Leverage" is null or ss."Pennant Gross Leverage" = 'NM' then null
                        else ss."Pennant Gross Leverage"
                    end as "leverage_pcof_iv_leverage",
                    null as "leverage_attachment_point", -- could not map -- Complete column is empty
                    sspibb."TotalCapitalization" as "leverage_total_capitalization", -- from PCOF III Borrrowing Base
                    ss."LTV" as "leverage_ltv_thru_pcof_iv", -- was from PCOF IV, Now taking from security stats (BU)
                    null as "final_eligibility_override", -- could not map -- Complete column is empty
                    null as "final_comment", -- could not map -- Complete column is empty
                    null as "concentration_adjustment", -- could not map -- -- considering null for now
                    null as "concentration_comment", -- could not map -- Complete column is empty
                    null as "borrowing_base_other_adjustment", -- could not map -- Complete column is empty
                    null as "borrowing_base_industry_concentration", -- could not map -- Complete column is empty
                    null as "borrowing_base_comment", -- could not map -- Complete column is empty
                    'Yes' as "is_eligible_issuer" -- could not map
                from sf_sheet_us_bank_holdings usbh
                left join sf_sheet_client_Holdings ch on ch."Issuer/Borrower Name" = usbh."Issuer/Borrower Name"
                    and ch."Current Par Amount (Issue Currency) - Settled" = usbh."Current Par Amount (Issue Currency) - Settled"
                left join pflt_security_mapping sm on sm.cashfile_security_name = usbh."Security/Facility Name"
                left join sf_sheet_securities_stats ss on ss."Security" = sm.master_comp_security_name
                left join sf_sheet_pcof_iii_borrrowing_base sspibb on ss."Security" = sspibb."Security Name" -- check this join
                left join sf_sheet_borrower_stats bs on bs."Company" = ss."Family Name"
                left join lien_type_mapping lien_mapping on lien_mapping.lien_type = ss."[SI] Credit Facility Lien Type" and (lien_mapping.is_deleted = false or lien_mapping.is_deleted is null)
				left join lien_type_master lien_master on lien_master.id = lien_mapping.master_lien_type_id
                left join sf_sheet_marketbook_1 ssmb on lower(substring(ch."Issuer/Borrower Name" from 1 for 20)) = lower(ssmb."Issuer_Name") and ssmb."Asset_Name" like '%' || usbh."Issue Name" || '%'
                where (usbh.source_file_id = :cash_file_id AND ch.source_file_id = :cash_file_id and (ssmb.source_file_id is null or ssmb.source_file_id = :market_book_file_id)) and
                ((sm.id is not null AND ss.source_file_id = :master_comp_file_id AND bs.source_file_id = :master_comp_file_id) or sm.id is null)
                group by sm.id, usbh."Security/Facility Name", usbh."Issuer/Borrower Name", ss."[SI] Credit Facility Lien Type", bs."[ACM] [COI/LC] PNNT Industry",
                bs."[ACM] [COI/LC] Closing Date", ss."[SI] Maturity",
                    ss."[SI] PIK Coupon",
                    ss."[SI] Cash Spread to LIBOR",
                    ss."[SI] LIBOR Floor",
                    ss."[SI] Type of Rate",
                    sspibb."Quoted / Unquoted", -- from PCOF III Borrrowing Base
                    sspibb."Warehouse Yes / No",
                    sspibb."Warehouse - Credit Rating", -- from PCOF III Borrrowing Base
                    sspibb."Approved Foreign Jurisdiction", -- from PCOF III Borrrowing Base
                    sspibb."LTV Transaction", -- from PCOF III Borrrowing Base
                    sspibb."Noteless Assigned Loan", -- from PCOF III Borrrowing Base
                    sspibb."Undelivered Note", -- from PCOF III Borrrowing Base
                    sspibb."Structured Finance Obligation", -- from PCOF III Borrrowing Base
                    sspibb."Third Party Finance Company", -- from PCOF III Borrrowing Base
                    sspibb."Affiliate Investment", -- from PCOF III Borrrowing Base
                    sspibb."Defaulted / Restructured", -- from PCOF III Borrrowing Base
                    ss."[C] LTM Rev",
                    ss."EBITDA",
                    ss."[PSM] TEV",
                    ss."Total Gross Leverage",
                    ss."Pennant Gross Leverage",
                    sspibb."TotalCapitalization", -- from PCOF III Borrrowing Base
                    ss."LTV",
                    ssmb."Commitment",
                    ssmb."BookValue",
                    ssmb."MarketValue",
                    lien_master.lien_type
                order by usbh."Security/Facility Name"
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