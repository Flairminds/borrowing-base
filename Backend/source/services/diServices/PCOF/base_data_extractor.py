import pandas as pd
from sqlalchemy import text

from source.utility.Log import Log
from source.utility.ServiceResponse import ServiceResponse

def map_and_store_base_data(engine, extracted_base_data_info, master_comp_file_details, market_book_file_details):
    try:
        print("storing base data of pcof")
        with engine.connect() as connection:
            pcof_base_data = pd.DataFrame(connection.execute(text(f'''
                select distinct
                    ss."Security" as investment_name,
                    sm.family_name  as "issuer",
                    case
						when lien_master.lien_type is null then ss."[SI] Credit Facility Lien Type"
						else lien_master.lien_type
					end
					as "investment_investment_type",
                    bs."[ACM] [COI/LC] PNNT Industry" as "investment_industry",
                    bs."[ACM] [COI/LC] Closing Date"::date as "investment_closing_date",
                    case when ss."[SI] Maturity" is not null and ss."[SI] Maturity" != 'NM' then ss."[SI] Maturity" else null end as "investment_maturity",
                    ssm."Commitment" as "investment_par",
                    ssm."BookValue" as "investment_cost",
                    ssm."MarketValue"  as "investment_external_valuation",
                    null as "investment_internal_valuation", -- Complete column is empty
                    case when ss."[SI] PIK Coupon" = 'NM' then null else ss."[SI] PIK Coupon"::float end as "rates_fixed_coupon",
                    case when ss."[SI] Cash Spread to LIBOR" = 'NM' then null else ss."[SI] Cash Spread to LIBOR"::float end as "rates_floating_cash_spread",
                    case when ss."[SI] LIBOR Floor" = 'NM' then null else ss."[SI] LIBOR Floor"::float end as "rates_current_lobor_floor",
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
                    case
						when ss."[SI] Credit Facility Lien Type" = 'Ineligible' then 'No'
						else 'Yes'
					end as "is_eligible_issuer" -- could not map
                from sf_sheet_marketbook_1 ssm
                left join pflt_security_mapping sm on sm.marketvalue_issuer = ssm."Issuer_Name" and sm.marketvalue_asset = ssm."Asset_Name"
                left join sf_sheet_securities_stats ss on ss."Security" = sm.master_comp_security_name
                left join sf_sheet_borrower_stats bs on bs."Company" = ss."Family Name"
                left join lien_type_mapping lien_mapping on lien_mapping.lien_type = ss."[SI] Credit Facility Lien Type" and (lien_mapping.is_deleted = false or lien_mapping.is_deleted is null)
				left join lien_type_master lien_master on lien_master.id = lien_mapping.master_lien_type_id
                where (ssm.source_file_id = :market_book_file_id) and
                ((sm.id is not null AND ss.source_file_id = :master_comp_file_id AND bs.source_file_id = :master_comp_file_id) or sm.id is null)
                group by ss."Security", sm.family_name, ss."[SI] Credit Facility Lien Type", bs."[ACM] [COI/LC] PNNT Industry", bs."[ACM] [COI/LC] Closing Date", ss."[SI] Maturity",
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
            '''), {'master_comp_file_id': master_comp_file_details.id, 'market_book_file_id': market_book_file_details.id}))

        if pcof_base_data.empty:
                raise Exception('Base data is empty')
        
        cash_row = {
            "investment_name": "Cash",
            "issuer": "Cash",
            "investment_investment_type": "Cash",
            "investment_industry": "Cash",
            "is_eligible_issuer": "Yes"
        }

        # pcof_base_data = pcof_base_data.append(cash_row, ignore_index=True)
        pcof_base_data = pd.concat([pcof_base_data, pd.DataFrame([cash_row])], ignore_index=True)
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