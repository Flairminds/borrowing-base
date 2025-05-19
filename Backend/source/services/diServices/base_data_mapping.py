import pandas as pd
from sqlalchemy import text
from models import db, PfltBaseData, BaseDataMapping


def rename_duplicate_columns(df):
    """Rename duplicate columns by appending incremental suffixes."""
    cols = pd.Series(df.columns)
    for dup in cols[cols.duplicated()].unique():
        new_names = [dup if i == 0 else f"{dup}_{i}" for i in range(sum(cols == dup))]
        cols[cols[cols == dup].index.values.tolist()] = new_names
    df.columns = cols
    return df

def base_data_mapping(cf, engine, bs = None):
    try:
        with engine.connect() as connection:
            base_data_map = pd.DataFrame(connection.execute(text('select * from "base_data_mapping"')).fetchall())
        data = []
        # new_dict = {}
        for i, r in base_data_map.iterrows():
            # if r['bd_column_name'] == 'Stretch Senior Loan (Y/N)':
            # if bs is not None and r['rd_column_name'] in bs:
            #     if isinstance((bs[r["rd_column_name"]]), pd.core.series.Series):
            #         data.append(bs[r["rd_column_name"]].astype("string"))
            #     else:
            #         data.append(bs[r["rd_column_name"]])
            if r["rd_column_name"] in cf and cf[r['rd_column_name']] is not None:
                # print("here", r['rd_column_name'], cf[r['rd_column_name']])
                if isinstance((cf[r["rd_column_name"]]), pd.core.series.Series):
                    data.append(cf[r["rd_column_name"]].astype("string"))
                else:
                    data.append(cf[r["rd_column_name"]])
            else:
                data.append(None)
        return data
    except Exception as e:
        print({
                    "error": str(e),
                    "error_type": str(type(e).__name__),
                    "error_file_details": f"error on line {e.__traceback__.tb_lineno} inside {__file__}",
                })

def soi_mapping(engine, extracted_base_data_info, master_comp_file_details, cash_file_details, market_book_file_details, master_rating_details):
    try:
        with engine.connect() as connection:
            cash_file = pd.DataFrame(connection.execute(text('''select td.obligor_name, td.security_name, td.purchase_price, td.stretch_senior_loan, td.loan_type, td.current_moodys_rating,
	td.current_sp_rating, td.initial_fixed_charge_coverage_ratio, td.market_value, td.current_fixed_charge_coverage_ratio, td.current_interest_coverage_ratio,
	td.initial_debt_to_capitalization_ratio, td.initial_senior_debt_ebitda, td.initial_total_debt_ebitda, td.current_senior_debt_ebitda, td.current_total_debt_ebitda,
	td.initial_ttm_ebitda, td.current_ttm_ebitda, td.current_as_of_date, td.maturity_date, td.lien_type, td.fixed_rate, td.floor_obligation, td.floor, td.spread_incl_pik_pikable,
	td.interest_paid, td.obligor_industry, td.currency, td.obligor_country, sum(total_commitment) as total_commitment, sum(outstanding_principal) as outstanding_principal,
	STRING_AGG(distinct td.loanx_id, ', ') AS loanx_id
	from (select distinct
	usbh."Issuer/Borrower Name" as obligor_name,
	ss."Security" as security_name,
	ch."Par Amount (Deal Currency)"::float as total_commitment,
	ch."Principal Balance (Deal Currency)"::float as outstanding_principal,
	case when ss."[SI] Blended Purchase Price" is not null and ss."[SI] Blended Purchase Price" != 'NA' and ss."[SI] Blended Purchase Price" != 'NM' then ss."[SI] Blended Purchase Price"::float else null end as purchase_price,
	case when ss."[SI] Stretch Senior (Y/N)" = 'Y' then 'Yes' else 'No' end as stretch_senior_loan,
	case when t2.master_loan_type is null then ch."Issue Name" else t2.master_loan_type end as loan_type,
	ssmr."[RD(] [M] Rating" as current_moodys_rating,
	ssmr."[RD(] [S] Rating" as current_sp_rating,
	bs."[ACM] [C-ACM(AC] Closing Fixed Charge Coverage Ratio" as initial_fixed_charge_coverage_ratio,
	ssm."MarkPrice_MarkPrice"::float as market_value,
	bs."[ACM] [C-ACM(AC] Closing Fixed Charge Coverage Ratio" as current_fixed_charge_coverage_ratio,
	bs."[CM] [CLSO] EBITDA / Cash Interest" as current_interest_coverage_ratio,
	bs."[ACM] [C-ACM(AC] Closing Debt to Capitalization" as initial_debt_to_capitalization_ratio,
	bs."[ACM] [C-ACM(AC] 1st Lien Net Debt / EBITDA" as initial_senior_debt_ebitda,
	bs."[ACM] [C-ACM(AC] HoldCo Net Debt / EBITDA" as initial_total_debt_ebitda,
	case when bs."First Lien Debt" = 'NM' or bs."First Lien Debt" is null or bs."[CM] [R] LTM EBITDA" = 'NM' or bs."[CM] [R] LTM EBITDA" is null
	then null else (bs."First Lien Debt"::float/bs."[CM] [R] LTM EBITDA"::float) end as current_senior_debt_ebitda,
	case when bs."Total Debt" = 'NM' or bs."Total Debt" is null or bs."[CM] [R] LTM EBITDA" = 'NM' or bs."[CM] [R] LTM EBITDA" is null
	then null else (bs."Total Debt"::float/bs."[CM] [R] LTM EBITDA"::float) end as current_total_debt_ebitda,
	case when bs."[ACM] [C-ACM(AC] LTM EBITDA" = 'NM' then null else (bs."[ACM] [C-ACM(AC] LTM EBITDA"::float)*1000000 end as initial_ttm_ebitda,
	case when bs."[CM] [R] LTM EBITDA" = 'NM' then null else (bs."[CM] [R] LTM EBITDA"::float)*1000000 end as current_ttm_ebitda,
	bs."[CM] [CS] Updated as of" as current_as_of_date,
	case when ss."[SI] Maturity" is not null and ss."[SI] Maturity" != 'NA' and ss."[SI] Maturity" != 'NM' then ss."[SI] Maturity" else null end as maturity_date,
	case when lien_master.lien_type is null then ss."[SI] Credit Facility Lien Type" else lien_master.lien_type end as lien_type,
	case when ss."[SI] Type of Rate" like 'Fixed Rate%' then 'Yes' else 'No' end as fixed_rate,
	case when ss."[SI] LIBOR Floor" is not null then 'Yes' else 'No' end as floor_obligation,
	case when ss."[SI] LIBOR Floor" != 'NM' then ss."[SI] LIBOR Floor"::float else null end as floor,
	case when ss."[SI] Cash Spread to LIBOR" != 'NM' and ss."[SI] Cash Spread to LIBOR" is not null and ss."[SI] PIK Coupon" != 'NM' then ss."[SI] Cash Spread to LIBOR"::float + coalesce(ss."[SI] PIK Coupon"::float, 0)::float else 0 end as spread_incl_pik_pikable,
	case when ch."Payment Period" = '3 Months' then 'Quarterly' when  ch."Payment Period" = '1 Month' then 'Quarterly' when ch."Payment Period" = '6 Months' then 'Half-Yearly' else null end as interest_paid,
	bs."[ACM] [COI/LC] S&P Industry" as obligor_industry,
	ss."[SI] Currency" as currency,
	ss."[SI] Obligor Country" as obligor_country,
	ch."LoanX ID" as "loanx_id"
from sf_sheet_us_bank_holdings usbh
left join sf_sheet_client_Holdings ch on ch."Issuer/Borrower Name" = usbh."Issuer/Borrower Name"
	and ch."Current Par Amount (Issue Currency) - Settled" = usbh."Current Par Amount (Issue Currency) - Settled"
left join 
	(select loan_mapping_cashfile.loan_type, loan_master_cashfile.loan_type as master_loan_type from loan_type_mapping loan_mapping_cashfile
		left join loan_type_master loan_master_cashfile on loan_master_cashfile.id = loan_mapping_cashfile.master_loan_type_id
		where (loan_mapping_cashfile.is_deleted = false or loan_mapping_cashfile.is_deleted is null) and loan_master_cashfile.fund_type = 'PFLT')
	as t2 on t2.loan_type = ch."Issue Name"
left join 
	(select *, loan_master_marketbook.loan_type as master_loan_type from sf_sheet_marketbook_1 ssm 
		left join loan_type_mapping loan_mapping_marketbook on loan_mapping_marketbook.loan_type = ssm."Asset_Name" and (loan_mapping_marketbook.is_deleted = false or loan_mapping_marketbook.is_deleted is null)
		left join loan_type_master loan_master_marketbook on loan_master_marketbook.id = loan_mapping_marketbook.master_loan_type_id and loan_master_marketbook.fund_type = 'PFLT'
		where ssm.source_file_id = :market_book_file_id)
	as ssm on lower(regexp_replace(ch."Issuer/Borrower Name", '[^a-zA-Z0-9]','', 'g')) = lower(regexp_replace(ssm."Issuer_Name", '[^a-zA-Z0-9]','', 'g')) and t2.master_loan_type = ssm.master_loan_type-- and ssm."Asset_Primary IDAssetID_Name" = ch."LoanX ID"
left join pflt_security_mapping sm on sm.cashfile_security_name = usbh."Security/Facility Name"
left join sf_sheet_securities_stats ss on ss."Security" = sm.master_comp_security_name
left join sf_sheet_pflt_borrowing_base pbb on pbb."Security" = ss."Security"
left join sf_sheet_borrower_stats bs on bs."Company" = ss."Family Name"
left join lien_type_mapping lien_mapping on lien_mapping.lien_type = ss."[SI] Credit Facility Lien Type" and (lien_mapping.is_deleted = false or lien_mapping.is_deleted is null)
left join lien_type_master lien_master on lien_master.id = lien_mapping.master_lien_type_id 
left join sf_sheet_master_ratings ssmr on ss."Family Name" = ssmr."[BN] Master Comps"
where (usbh.source_file_id= :cash_file_id AND ch.source_file_id= :cash_file_id AND (ssm.source_file_id is null or ssm.source_file_id = :market_book_file_id)) and
((sm.id is not null AND ss.source_file_id= :master_comp_file_id AND bs.source_file_id= :master_comp_file_id) or sm.id is null) and (ssmr.source_file_id = :master_rating_id or ssmr.source_file_id is null)) as td
    group by td.obligor_name, td.security_name, td.purchase_price, td.stretch_senior_loan, td.loan_type, td.current_moodys_rating,
	td.current_sp_rating, td.initial_fixed_charge_coverage_ratio, td.market_value, td.current_fixed_charge_coverage_ratio, td.current_interest_coverage_ratio,
	td.initial_debt_to_capitalization_ratio, td.initial_senior_debt_ebitda, td.initial_total_debt_ebitda, td.current_senior_debt_ebitda, td.current_total_debt_ebitda,
	td.initial_ttm_ebitda, td.current_ttm_ebitda, td.current_as_of_date, td.maturity_date, td.lien_type, td.fixed_rate, td.floor_obligation, td.floor, td.spread_incl_pik_pikable,
	td.interest_paid, td.obligor_industry, td.currency, td.obligor_country
	order by td.security_name'''), {'cash_file_id': cash_file_details.id, 'master_comp_file_id': master_comp_file_details.id, 'market_book_file_id': market_book_file_details.id, "master_rating_id": master_rating_details.id}).fetchall())
            df = cash_file
            if df.empty:
                raise Exception('Base data is empty')
            df["base_data_info_id"] = extracted_base_data_info.id
            df["company_id"] = master_comp_file_details.company_id
            df["report_date"] = master_comp_file_details.report_date
            # df.to_csv('file1.csv')
            df.to_sql("pflt_base_data", con=engine, if_exists='append', index=False, method='multi')

    except Exception as e:
        raise Exception(e)