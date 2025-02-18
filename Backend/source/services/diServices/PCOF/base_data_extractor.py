import pandas as pd
from sqlalchemy import text

from source.utility.Log import Log
from source.utility.ServiceResponse import ServiceResponse
def map_and_store_base_data(engine, extracted_base_data_info, master_comp_file_details, cash_file_details, market_book_file_details):
    try:
        print("storing base data of pcof")
        with engine.connect() as connection:
            pcof_base_data = pd.DataFrame(connection.execute(text(f'''select 
                distinct usbh."Security/Facility Name" as "investment_name",
                usbh."Issuer/Borrower Name"  as "issuer",
                ss."[SI] Credit Facility Lien Type" as "investment_investment_type",
                bs."[ACM] [COI/LC] PNNT Industry" as "investment_industry",
                bs."[ACM] [COI/LC] Closing Date" as "investment_closing_date",
                ss."[SI] Maturity" as "investment_maturity",
                usbh."P. Lot Current Par Amount (Deal Currency)" as "investment_par", -- selecting this column for now
                ssmb."Book Value"  as "investment_cost", -- could not map -- considering null for now
                ssmb."Market Value"  as "investment_external_valuation", -- could not map -- considering null for now
                null as "investment_internal_valuation", -- Complete column is empty
                ss."[SI] PIK Coupon" as "rates_fixed_coupon",
                ss."[SI] Cash Spread to LIBOR" as "rates_floating_cash_spread",
                ss."[SI] LIBOR Floor" as "rates_current_lobor_floor",
                null as "rates_pik", -- Complete column is empty
                ss."[SI] Type of Rate" as "rates_fixed_floating",
                sspibb."Quoted / Unquoted"  as "classifications_quoted_unquoted", -- from PCOF III Borrrowing Base
                sspibb."Warehouse Yes / No"  as "classifications_warehouse_asset", -- from PCOF III Borrrowing Base
                null as "classifications_warehouse_asset_inclusion_date", -- could not map -- Complete column is empty
                sspibb."Warehouse - Credit Rating" as "classifications_warehouse_asset_expected_rating", -- from PCOF III Borrrowing Base
                sspibb."Approved Foreign Jurisdiction" as "classifications_approved_foreign_jurisdiction", -- from PCOF III Borrrowing Base
                sspibb."LTV Transaction" as "classifications_ltv_transaction", -- from PCOF III Borrrowing Base
                sspibb."Noteless Assigned Loan" as "classifications_noteless_assigned_loan", -- from PCOF III Borrrowing Base
                sspibb."Undelivered Note" as "classifications_undelivered_note", -- from PCOF III Borrrowing Base
                sspibb."Structured Finance Obligation" as "classifications_structured_finance_obligation", -- from PCOF III Borrrowing Base
                sspibb."Third Party Finance Company" as "classifications_third_party_finance_company", -- from PCOF III Borrrowing Base
                sspibb."Affiliate Investment" as "classifications_affiliate_investment", -- from PCOF III Borrrowing Base
                sspibb."Defaulted / Restructured" as "classifications_defaulted_restructured", -- from PCOF III Borrrowing Base
                ss."[C] LTM Rev" as "financials_ltm_revenue_mms",
                ss."EBITDA" as "financials_ltm_ebitda_mms",
                null as "leverage_revolver_commitment", -- could not map -- considering null for now
                ss."[PSM] TEV" as "leverage_total_enterprise_value",
                ss."Total Gross Leverage" as "leverage_total_leverage",
                case 
                    when ss."Pennant Gross Leverage" = 'NM' then null
                end
                as "leverage_pcof_iv_leverage",
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
            left join sf_sheet_pcof_iv sspi on ss."Security" = sspi."Asset"
            left join sf_sheet_borrower_stats bs on bs."Company" = ss."Family Name"
            left join sf_sheet_marketbook ssmb on ch."Issuer/Borrower Name" = ssmb."Issuer"
            where (usbh.source_file_id = 132 AND ch.source_file_id = 132 and ssmb.source_file_id = 138) and
            ((sm.id is not null AND ss.source_file_id = 133 AND bs.source_file_id = 133) or sm.id is null)
            order by usbh."Security/Facility Name"'''), {'cash_file_id': cash_file_details.id, 'master_comp_file_id': master_comp_file_details.id}))

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