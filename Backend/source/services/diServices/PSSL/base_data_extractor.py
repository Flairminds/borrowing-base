import pandas as pd
from sqlalchemy import text

from source.utility.Log import Log
from source.utility.ServiceResponse import ServiceResponse

def map_and_store_base_data(engine, extracted_base_data_info, master_comp_file_details, cash_file_details):
    try:
        with engine.connect() as connection:
            pssl_base_data = pd.DataFrame(connection.execute(text(f'''
                select distinct
                    usbh."Issuer/Borrower Name" as borrower,
                    ss."[SI] Credit Facility Lien Type" as loan_type, -- check this
                    null as rcf_exposure_type,
                    null as rcf_commitment_amount,
                    null as rcf_outstanding_amount,
                    (date_trunc('month', CURRENT_DATE) - interval '1 day')::date as rcf_update_date,
                    sum(ch."Principal Balance (Deal Currency)"::float) as "borrower_outstanding_principal_balance",
                    sum(ch."Par Amount (Deal Currency)"::float) as "borrower_facility_commitment",
                    null as initial_unrestricted_cash,
                    null as "initial_gross_senior_debt",
                    null as "initial_gross_total_debt",
                    case when bs."[CM] [CS] Cash" = 'NM' then null else (bs."[CM] [CS] Cash"::float)*1000000 end as "current_unrestricted_cash",
                    case when bs."First Lien Debt" = 'NM' or bs."First Lien Debt" is null then null else (bs."First Lien Debt"::float)*1000000 end as "current_gross_senior_debt",
                    case when bs."Total Debt" = 'NM' then null else (bs."Total Debt"::float)*1000000 end as "current_gross_total_debt",
                    null as "upfront_approval_rights",
                    case when ss."[SI] Maturity" is not null and ss."[SI] Maturity" != 'NA' and ss."[SI] Maturity" != 'NM' then ss."[SI] Maturity" else null end as "maturity_date",
                    null as "eligible_loan_attestation",
                    ss."[B] Cov-Lite?" as "cov_lite",
                    ss."[SI] Cash Spread to LIBOR"  as "spread",
                    null as "dip_loan",
                    ss."[SI] Obligor Country" as approved_country,
                    ss."[SI] Currency" as "approved_currency",
                    bs."[ACM] [COI/LC] S&P Industry"  as "approved_industry",
                    case when ss."[SI] Type of Rate" like 'Fixed Rate%' then 'Yes' else 'No' end as is_fixed_rate,
                    case when ch."Payment Period" = '3 Months' then 'Quarterly' when ch."Payment Period" = '1 Month' then 'Quarterly' when ch."Payment Period" = '6 Months' then 'Half-Yearly' else null end as interest_paid,
                    'No' as paid_less_than_qtrly,
                    ch."Deal Issue (Derived) Rating - S&P" as "sp_rating",
                    ch."Deal Issue (Derived) Rating - Moody's" as "moodys_rating",
                    null as "rated_b_or_better",
                    null  as two_market_quotes,
                    bs."[CM] [CS] Updated as of" as date_of_ttm_financials,
                    null as "initial_ttm_adjusted_ebitda",
                    null as "add_backs",
                    bs."[CM] [CS] Updated as of" as relevent_test_period,
                    case when bs."[CM] [R] LTM EBITDA" = 'NM' then null else (bs."[CM] [R] LTM EBITDA"::float)*1000000 end as adjusted_ttm_ebiteda,
                    case when bs."[CM] [R] LTM Cash Interest" = 'NM' then null else (bs."[CM] [R] LTM Cash Interest"::float)*1000000 end as current_cash_interest_expense,
                    null as "obligor_payment_default",
                    null as "exercise_rights_and_remedies",
                    null as "reduces_waives_principal",
                    null as "extends_maturity_date",
                    null as "reduces_waives_interest",
                    null as "subordinates_loans",
                    null as "releases_collateral_lien",
                    null as "amends_covenants",
                    null as "reporting_failure_event",
                    null as "insolvency_event",
                    case when ss."[SI] Blended Purchase Price" is not null and ss."[SI] Blended Purchase Price" != 'NA' and ss."[SI] Blended Purchase Price" != 'NM' then ss."[SI] Blended Purchase Price"::float else null end as acquisition_price,
                    --usbh."Settle Date" as acquisition_date,
                    case when ss."[SI] Investment Dates" is not null and ss."[SI] Investment Dates" != 'NA' and ss."[SI] Investment Dates" != 'NM' and STRPOS(ss."[SI] Investment Dates", ',') = 0 and STRPOS(ss."[SI] Investment Dates", ';') = 0 then ss."[SI] Investment Dates" else null end as "origination_date",
                    'No' as amends_definitions,
                    'No' as waives_or_extends_due_date_of_financial_reports,
                    'No' as ddtl,
                    'No' as finanicals_since_received,
                    null as initial_cash_interest_expense,
                    null as initial_liquidity,
                    null as current_liquidity,
                    null as initial_annualized_recurring_revenue,
                    null as annualized_recurring_revenue,
                    'No' as revolver,
                    STRING_AGG(ch."LoanX ID", ', ') AS loanx_id
                from sf_sheet_us_bank_holdings usbh
                left join sf_sheet_client_Holdings ch on ch."Issuer/Borrower Name" = usbh."Issuer/Borrower Name"
                    and ch."Current Par Amount (Issue Currency) - Settled" = usbh."Current Par Amount (Issue Currency) - Settled" 
                left join pflt_security_mapping sm on sm.cashfile_security_name = usbh."Security/Facility Name"
                left join sf_sheet_securities_stats ss on ss."Security" = sm.master_comp_security_name
                /*left join sf_sheet_pssl_ii_borrowing_base sspibb on sspibb."Security" = ss."Security"*/
                left join sf_sheet_borrower_stats bs on bs."Company" = ss."Family Name"  
                where (usbh.source_file_id= :cash_file_id AND ch.source_file_id= :cash_file_id) and
                ((sm.id is not null AND ss.source_file_id= :master_comp_file_id AND bs.source_file_id= :master_comp_file_id) or sm.id is null)
                group by 
                    usbh."Issuer/Borrower Name", 
                    ss."[SI] Blended Purchase Price",
                    ss."[SI] Credit Facility Lien Type", 
                    ss."[SI] Maturity",
                    ss."[SI] Investment Dates",
                    bs."[CM] [CS] Updated as of",
                    ss."[SI] Blended Purchase Price",
                    bs."[CM] [R] LTM Cash Interest",
                    bs."[CM] [CS] Cash", bs."First Lien Debt", bs."Total Debt", ss."[B] Cov-Lite?", ss."[SI] Cash Spread to LIBOR", ss."[SI] Obligor Country", ss."[SI] Currency", bs."[ACM] [COI/LC] S&P Industry", ss."[SI] Type of Rate", ch."Payment Period", ch."Deal Issue (Derived) Rating - S&P", ch."Deal Issue (Derived) Rating - Moody's", bs."[CM] [R] LTM EBITDA"
                order by 
                    usbh."Issuer/Borrower Name"
            '''), {'cash_file_id': cash_file_details.id, 'master_comp_file_id': master_comp_file_details.id}))

        if pssl_base_data.empty:
                raise Exception('Base data is empty')
        pssl_base_data["base_data_info_id"] = extracted_base_data_info.id
        pssl_base_data["company_id"] = master_comp_file_details.company_id
        pssl_base_data["report_date"] = master_comp_file_details.report_date
        # df.to_csv('file1.csv')
        pssl_base_data.to_sql("pssl_base_data", con=engine, if_exists='append', index=False, method='multi')
        
        return ServiceResponse.success(message=f"Successfully stored base data from pcof for extracted_base_data_info.id {extracted_base_data_info.id}")
    except Exception as e:
        print(f"Could not map and store data from sheet table for extracted_base_data_info.id {extracted_base_data_info.id}")
        print(str(e)[:150])
        raise Exception(e)


