import pandas as pd
from sqlalchemy import text
from models import db, PfltBaseData, PfltBaseDataMapping


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

def soi_mapping(engine, extracted_base_data_info, master_comp_file_details, cash_file_details):
    try:
        with engine.connect() as connection:
            cash_file = pd.DataFrame(connection.execute(text('''select distinct
	usbh."Issuer/Borrower Name" as obligor_name,
	--usbh."Security/Facility Name" as security_name,
	ss."Security" as security_name,
	--usbh."Purchase Date"::date as purchase_date,
	sum(ch."Par Amount (Deal Currency)"::float) as total_commitment,
	sum(ch."Principal Balance (Deal Currency)"::float) as outstanding_principal,
	case when pbb."Defaulted Collateral Loan at Acquisition" = 0 then 'No' when pbb."Defaulted Collateral Loan at Acquisition" = 1 then 'Yes' else null end as defaulted_collateral_loan,
	case when pbb."Credit Improved Loan" = 0 then 'No' when pbb."Credit Improved Loan" = 1 then 'Yes' else null end as credit_improved_loan,
	case when avg(usbh."Original Purchase Price"::float) is not null then avg(usbh."Original Purchase Price"::float) else null end as purchase_price,
	pbb."Stretch Senior (Y/N)" as stretch_senior_loan,
	ch."Issue Name" as loan_type,
	ch."Deal Issue (Derived) Rating - Moody's" as current_moodys_rating,
	ch."Deal Issue (Derived) Rating - S&P" as current_sp_rating,
	bs."[ACM] [C-ACM(AC] Closing Fixed Charge Coverage Ratio" as initial_fixed_charge_coverage_ratio,
	null as date_of_default,
	100 as market_value,
	bs."[ACM] [C-ACM(AC] Closing Fixed Charge Coverage Ratio" as current_fixed_charge_coverage_ratio,
	bs."[CM] [CLSO] 1st Lien Net Debt / EBITDA" as current_interest_coverage_ratio,
	bs."[ACM] [C-ACM(AC] Closing Debt to Capitalization" as initial_debt_to_capitalization_ratio,
	bs."[ACM] [C-ACM(AC] 1st Lien Net Debt / EBITDA" as initial_senior_debt_ebitda,
	bs."[ACM] [C-ACM(AC] HoldCo Net Debt / EBITDA" as initial_total_debt_ebitda,
	pbb."Senior Debt"::float / pbb."LTM EBITDA"::float as current_senior_debt_ebitda,
	pbb."Total Debt"::float / pbb."LTM EBITDA"::float as current_total_debt_ebitda,
	pbb."Closing LTM EBITDA"::float * 1000000 as initial_ttm_ebitda,
	pbb."Current LTM EBITDA"::float * 1000000 as current_ttm_ebitda,
	ch."As Of Date" as current_as_of_date,
	usbh."Maturity Date" as maturity_date,
	ss."[SI] Credit Facility Lien Type" as lien_type,
	case when pbb."Eligible Covie Lite (1L, Issue > $250mm, B3 / B-)" = 0 then 'No' when pbb."Eligible Covie Lite (1L, Issue > $250mm, B3 / B-)" = 1 then 'Yes' else null end as eligible_covenant_lite,
	case when ss."[SI] Type of Rate" like 'Fixed Rate%' then 'Yes' else 'No' end as fixed_rate,
	0 as coupon_incl_pik_pikable,
	case when ss."[SI] LIBOR Floor" is not null then 'Yes' else 'No' end as floor_obligation,
	case when ss."[SI] LIBOR Floor" != 'NM' then ss."[SI] LIBOR Floor"::float else null end as floor,
	case when ss."[SI] Cash Spread to LIBOR" != 'NM' and ss."[SI] Cash Spread to LIBOR" is not null then ss."[SI] Cash Spread to LIBOR"::float + coalesce(ss."[SI] PIK Coupon"::float, 0)::float else null end as spread_incl_pik_pikable,
	0 as base_rate,
	0 as for_unused_fee,
	0 as pik_pikable_for_floating_rate_loans,
	0 as pik_pikable_for_fixed_rate_loans,
	case when ch."Payment Period" = '3 Months' then 'Quarterly' when  ch."Payment Period" = '1 Month' then 'Monthly' when ch."Payment Period" = '6 Months' then 'Half-Yearly' else null end as interest_paid,
	bs."[ACM] [COI/LC] S&P Industry" as obligor_industry,
	ss."[SI] Currency" as currency,
	ss."[SI] Obligor Country" as obligor_country,
	case when pbb."DIP Loans" = 0 then 'No' when pbb."DIP Loans" = 1 then 'Yes' else null end as dip_loan,
	case when pbb."Obligations w/ Warrants attached" = 0 then 'No' when pbb."Obligations w/ Warrants attached" = 1 then 'Yes' else null end as warrants_to_purchase_equity,
	case when pbb."Participations" = 0 then 'No' when pbb."Participations" = 1 then 'Yes' else null end as participation,
	case when pbb."Convertible into Equity" = 0 then 'No' when pbb."Convertible into Equity" = 1 then 'Yes' else null end as convertible_to_equity,
	case when pbb."Equity Security" = 0 then 'No' when pbb."Equity Security" = 1 then 'Yes' else null end as equity_security,
	case when pbb."Subject of an Offer or Called for Redemption" = 0 then 'No' when pbb."Subject of an Offer or Called for Redemption" = 1 then 'Yes' else null end as at_acquisition_offer_or_redemption,
	case when pbb."Margin Stock" = 0 then 'No' when pbb."Margin Stock" = 1 then 'Yes' else null end as margin_stock,
	case when pbb."Subject to Withholding Tax" = 0 then 'No' when pbb."Subject to Withholding Tax" = 1 then 'Yes' else null end as subject_to_withholding_tax,
	case when pbb."Defaulted Collateral Loan at Acquisition" = 0 then 'No' when pbb."Defaulted Collateral Loan at Acquisition" = 1 then 'Yes' else null end as at_acquisition_defaulted_loan,
	case when pbb."Zero Coupon Obligation" = 0 then 'No' when pbb."Zero Coupon Obligation" = 1 then 'Yes' else null end as zero_coupon_obligation,
	case when pbb."Covenant Lite" = 0 then 'No' when pbb."Covenant Lite" = 1 then 'Yes' else null end as covenant_lite,
	case when pbb."Structured Finance Obligation / finance lease" = 0 then 'No' when pbb."Structured Finance Obligation / finance lease" = 1 then 'Yes' else null end as structured_finance_obligation,
	case when pbb."Material Non-Credit Related Risk" = 0 then 'No' when pbb."Material Non-Credit Related Risk" = 1 then 'Yes' else null end as material_non_credit_related_risk,
	case when pbb."Primarily Secured by Real Estate" = 0 then 'No' when pbb."Primarily Secured by Real Estate" = 1 then 'Yes' else null end as primarily_secured_by_real_estate_or_loan,
	case when pbb."Interest Only Security" = 0 then 'No' when pbb."Interest Only Security" = 1 then 'Yes' else null end as interest_only_security,
	case when pbb."Satisfies Other Criteria(1)" = 0 then 'No' when pbb."Satisfies Other Criteria(1)" = 1 then 'Yes' else null end as satisfies_all_other_eligibility_criteria,
	null as excess_concentration_amount
from pflt_us_bank_holdings usbh
left join pflt_client_Holdings ch on ch."Issuer/Borrower Name" = usbh."Issuer/Borrower Name"
	and ch."Current Par Amount (Issue Currency) - Settled" = usbh."Current Par Amount (Issue Currency) - Settled"
left join pflt_security_mapping sm on sm.cashfile_security_name = usbh."Security/Facility Name"
left join pflt_securities_stats ss on ss."Security" = sm.master_comp_security_name
left join pflt_pflt_borrowing_base pbb on pbb."Security" = ss."Security"
left join pflt_borrower_stats bs on bs."Company" = ss."Family Name"
where (usbh.source_file_id= :cash_file_id AND ch.source_file_id= :cash_file_id) and
((sm.id is not null AND ss.source_file_id= :master_comp_file_id AND pbb.source_file_id= :master_comp_file_id AND bs.source_file_id= :master_comp_file_id) or sm.id is null)
    group by usbh."Issuer/Borrower Name", usbh."Security/Facility Name", pbb."Defaulted Collateral Loan at Acquisition",
	ss."Security", pbb."Credit Improved Loan", pbb."Stretch Senior (Y/N)", ch."Issue Name",
	ch."Deal Issue (Derived) Rating - Moody's", ch."Payment Period", ch."Deal Issue (Derived) Rating - S&P", bs."[ACM] [C-ACM(AC] Closing Fixed Charge Coverage Ratio",
	bs."[ACM] [C-ACM(AC] Closing Debt to Capitalization", pbb."Senior Debt", pbb."LTM EBITDA", pbb."Total Debt",
	pbb."Closing LTM EBITDA", pbb."Current LTM EBITDA", ch."As Of Date", usbh."Maturity Date", ss."[SI] Type of Rate",
	ss."[SI] LIBOR Floor", bs."[ACM] [COI/LC] S&P Industry", ss."[SI] Credit Facility Lien Type", ss."[SI] Currency", ss."[SI] Obligor Country",
	pbb."DIP Loans", pbb."Obligations w/ Warrants attached", pbb."Participations", pbb."Convertible into Equity", pbb."Eligible Covie Lite (1L, Issue > $250mm, B3 / B-)",
	pbb."Equity Security", pbb."Subject of an Offer or Called for Redemption", pbb."Margin Stock", pbb."Subject to Withholding Tax", pbb."Zero Coupon Obligation",
	pbb."Covenant Lite", pbb."Structured Finance Obligation / finance lease", pbb."Material Non-Credit Related Risk", pbb."Primarily Secured by Real Estate",
	pbb."Interest Only Security", pbb."Satisfies Other Criteria(1)", bs."[ACM] [C-ACM(AC] Closing Fixed Charge Coverage Ratio", bs."[ACM] [C-ACM(AC] 1st Lien Net Debt / EBITDA",
	bs."[CM] [CLSO] 1st Lien Net Debt / EBITDA", bs."[ACM] [C-ACM(AC] HoldCo Net Debt / EBITDA", ss."[SI] Cash Spread to LIBOR", ss."[SI] PIK Coupon"
order by security_name'''), {'cash_file_id': cash_file_details.id, 'master_comp_file_id':master_comp_file_details.id}).fetchall())
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