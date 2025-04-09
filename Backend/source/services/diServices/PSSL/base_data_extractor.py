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
                    sspibb."RCF Exposure Type" as rcf_exposure_type,
                    sspibb."RCF Commitment Amount" as "rcf_commitment_amount",
                    null as rcf_outstanding_amountd,
                    null as rcf_update_date,
                    sspibb."Borrower Outstanding Principal Balance" as "borrower_outstanding_principal_balance",
                    sspibb."Borrower Facility Commitment" as "borrower_facility_commitment",
                    sspibb."[IDI$AM] Initial Unrestricted Cash" as initial_unrestricted_cash,
                    sspibb."[IDI$AM] Initial Senior Debt" as "initial_gross_senior_debt",
                    sspibb."[IDI$AM] Initial Total Debt" as "initial_gross_total_debt",
                    sspibb."[CDI$AM] Current Unrestricted Cash" as "current_unrestricted_cash",
                    sspibb."[CDI$AM] Current Senior Debt" as "current_gross_senior_debt",
                    sspibb."[CDI$AM] Current Total Debt" as "current_gross_total_debt",
                    sspibb."Upfront Approval Rights" as "upfront_approval_rights",
                    usbh."Maturity Date" as "maturity_date",
                    sspibb."Eligible Loan" as "eligible_loan_attestation",
                    sspibb."Cov-Lite?" as "cov_lite",
                    sspibb.spread  as "spread",
                    sspibb."DIP Loan" as "dip_loan",
                    sspibb."Approved Country Domicile" as approved_country,
                    sspibb."Approved Currency" as "approved_currency",
                    sspibb."GICS Industry"  as "approved_industry",
                    sspibb."Fixed Rate?" as "is_fixed_rate",
                    sspibb."Interest Paid (Mthly, Qtrly)" as "interest_paid",
                    sspibb."Paid Less than Qtrly or Mthly" as "paid_less_than_qtrly",
                    sspibb."[R] S&P" as "sp_rating",
                    sspibb."[R] Moody's" as "moodys_rating",
                    sspibb."Rated B- or better" as "rated_b_or_better",
                    sspibb."Two Market  Quotes"  as two_market_quotes,
                    sspibb."[IE] Initial Date of TTM Financials" as "date_of_ttm_financials",
                    sspibb."[IE] Initial Adjusted TTM EBITDA" as "initial_ttm_adjusted_ebitda",
                    sspibb."[IE] Initial Initial EBITDA Addbacks" as "add_backs",
                    null as relevent_test_period,
                    sspibb."[CU] Current Adjusted TTM EBITDA" as "adjusted_ttm_ebiteda",
                    sspibb."[VAE] Obligor Payment Default"  as "obligor_payment_default",
                    sspibb."[VAE] Exercise of Rights and Remedies" as "exercise_rights_and_remedies",
                    sspibb."[VAE] (a) Reduces/waives Principal" as "reduces_waives_principal",
                    sspibb."[VAE] (b) Extends Maturity/ Payment Date" as "extends_maturity_date",
                    sspibb."[VAE] (c) Waives Interest" as "reduces_waives_interest",
                    sspibb."[VAE] (d) Subordinates Loan" as "subordinates_loans",
                    sspibb."[VAE] (e) Releases Collateral/Lien" as "releases_collateral_lien",
                    sspibb."[VAE] (f) Amends Covenants" as "amends_covenants",
                    sspibb."[VAE] (f) Failure to Deliver Financial Reports" as "reporting_failure_event",
                    sspibb."[VAE] (e) Obligor Insolvency Event"  as "insolvency_event",
                    null as acquisition_price,
                    null as acquisition_date,
                    null as origination_date,
                    null as amends_definitions,
                    null as waives_or_extends_due_date_of_financial_reports,
                    null as ddtl,
                    null as initial_cash_interest_expense,
                    null as initial_liquidity,
                    null as revolver,
                    ch."LoanX ID" as "loanx_id"
                from sf_sheet_us_bank_holdings usbh
                left join sf_sheet_client_Holdings ch on ch."Issuer/Borrower Name" = usbh."Issuer/Borrower Name"
                    and ch."Current Par Amount (Issue Currency) - Settled" = usbh."Current Par Amount (Issue Currency) - Settled" 
                left join pflt_security_mapping sm on sm.cashfile_security_name = usbh."Security/Facility Name"
                left join sf_sheet_securities_stats ss on ss."Security" = sm.master_comp_security_name
                left join sf_sheet_pssl_ii_borrowing_base sspibb on sspibb."Security" = ss."Security"
                left join sf_sheet_borrower_stats bs on bs."Company" = ss."Family Name"
                left join loan_type_mapping loan_mapping on loan_mapping.loan_type = ch."Issue Name" and (loan_mapping.is_deleted = false or loan_mapping.is_deleted is null)
                left join loan_type_master loan_master on loan_master.id = loan_mapping.master_loan_type_id
                left join lien_type_mapping lien_mapping on lien_mapping.lien_type = ss."[SI] Credit Facility Lien Type" and (lien_mapping.is_deleted = false or lien_mapping.is_deleted is null)
                left join lien_type_master lien_master on lien_master.id = lien_mapping.master_lien_type_id  
                where (usbh.source_file_id= :cash_file_id AND ch.source_file_id= :cash_file_id) and
                ((sm.id is not null AND ss.source_file_id= :master_comp_file_id AND (sspibb.source_file_id = :master_comp_file_id or sspibb.source_file_id is null) AND bs.source_file_id= :master_comp_file_id) or sm.id is null)
                group by 
                    usbh."Issuer/Borrower Name", 
                    ss."[SI] Credit Facility Lien Type", 
                    sspibb."RCF Exposure Type", 
                    ch."LoanX ID",
                    sspibb."RCF Commitment Amount",
                    sspibb."Borrower Outstanding Principal Balance",
                    sspibb."Borrower Facility Commitment",
                    sspibb."[IDI$AM] Initial Unrestricted Cash",
                    sspibb."[IDI$AM] Initial Senior Debt",
                    sspibb."[IDI$AM] Initial Total Debt",
                    sspibb."[CDI$AM] Current Unrestricted Cash",
                    sspibb."[CDI$AM] Current Senior Debt",
                    sspibb."[CDI$AM] Current Total Debt",
                    sspibb."Upfront Approval Rights",
                    sspibb."Eligible Loan",
                    sspibb."Cov-Lite?",
                    sspibb.spread,
                    sspibb."DIP Loan", 
                    usbh."Maturity Date",
                    sspibb."Approved Country Domicile",
                    sspibb."Approved Currency",
                    sspibb."GICS Industry",
                    sspibb."Fixed Rate?",
                    sspibb."Interest Paid (Mthly, Qtrly)",
                    sspibb."Paid Less than Qtrly or Mthly",
                    sspibb."[R] S&P",
                    sspibb."[R] Moody's",
                    sspibb."Rated B- or better",
                    sspibb."Two Market  Quotes",
                    sspibb."[IE] Initial Date of TTM Financials",
                    sspibb."[IE] Initial Adjusted TTM EBITDA",
                    sspibb."[IE] Initial Initial EBITDA Addbacks",
                    sspibb."[CU] Current Adjusted TTM EBITDA",
                    sspibb."[VAE] Obligor Payment Default",
                    sspibb."[VAE] Exercise of Rights and Remedies",
                    sspibb."[VAE] (a) Reduces/waives Principal",
                    sspibb."[VAE] (b) Extends Maturity/ Payment Date",
                    sspibb."[VAE] (c) Waives Interest",
                    sspibb."[VAE] (d) Subordinates Loan",
                    sspibb."[VAE] (e) Releases Collateral/Lien",
                    sspibb."[VAE] (f) Amends Covenants",
                    sspibb."[VAE] (f) Failure to Deliver Financial Reports",
                    sspibb."[VAE] (e) Obligor Insolvency Event" 
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
        Log.func_error(e=e)
        print(f"Could not map and store data from sheet table for extracted_base_data_info.id {extracted_base_data_info.id}")
        ServiceResponse.error(message=f"Could not map and store data from sheet table for extraction_info_id {extracted_base_data_info.id}")


