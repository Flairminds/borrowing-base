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
	usbh."Security/Facility Name" as security_name,
	--ss."Security" as security_name,
	null as purchase_date,
	sum(ch."Par Amount (Deal Currency)"::float) as total_commitment,
	sum(ch."Principal Balance (Deal Currency)"::float) as outstanding_principal,
	case when pbb."Defaulted Collateral Loan at Acquisition" = 0 then 'N' when pbb."Defaulted Collateral Loan at Acquisition" = 1 then 'Y' else null end as defaulted_collateral_loan,
	case when pbb."Credit Improved Loan" = 0 then 'N' when pbb."Credit Improved Loan" = 1 then 'Y' else null end as credit_improved_loan,
	usbh."Original Purchase Price" as purchase_price,
	pbb."Stretch Senior (Y/N)" as stretch_senior_loan,
	ch."Issue Name" as loan_type,
	ch."Deal Issue (Derived) Rating - Moody's" as current_moodys_rating,
	ch."Deal Issue (Derived) Rating - S&P" as current_sp_rating,
	bs."[ACM] [C-ACM(AC] Closing Fixed Charge Coverage Ratio" as initial_fixed_charge_coverage_ratio,
	null as date_of_default,
	null as market_value
	/*bs."[ACM] [C-ACM(AC] Closing Fixed Charge Coverage Ratio" as "Current Fixed Charge Coverage Ratio",
	bs."[CM] [CLSO] 1st Lien Net Debt / EBITDA" as "Current Interest Coverage Ratio",
	bs."[ACM] [C-ACM(AC] Closing Debt to Capitalization" as "Initial Debt to Capitalization Ratio",
	bs."[ACM] [C-ACM(AC] 1st Lien Net Debt / EBITDA" as "Initial Senior Debt/EBITDA",
	bs."[ACM] [C-ACM(AC] HoldCo Net Debt / EBITDA" as "Initial Total Debt/EBITDA",
	pbb."Senior Debt"::float / pbb."LTM EBITDA"::float as "Current Senior Debt/EBITDA",
	pbb."Total Debt"::float / pbb."LTM EBITDA"::float as "Current Total Debt/EBITDA",
	pbb."Closing LTM EBITDA" as "Initial TTM EBITDA",
	pbb."Current LTM EBITDA" as "Current TTM EBITDA",
	ch."As Of Date" as "Current As of Date For Leverage and EBITDA",
	usbh."Maturity Date" as "Maturity Date",
	case
		when ss."[SI] Type of Rate" like 'Fixed Rate%' then 'Y'
		else 'N'
	end as "Fixed Rate (Y/N)",
	null as "Coupon incl. PIK and PIK'able (if Fixed)",
	case
		when ss."[SI] LIBOR Floor" is not null then 'Y'
		else 'N'
	end as "Floor Obligation (Y/N)",
	case
		when ss."[SI] LIBOR Floor" != 'NM' then ss."[SI] LIBOR Floor"::float
		else null
	end as "Floor",
	case
		when ss."[SI] Cash Spread to LIBOR" != 'NM' and ss."[SI] Cash Spread to LIBOR" is not null then ss."[SI] Cash Spread to LIBOR"::float + coalesce(ss."[SI] PIK Coupon"::float, 0)::float
		else null
	end as "Spread incl. PIK and PIK'able",
	null as "Base Rate",
	null as "For Revolvers/Delayed Draw, commitment or other unused fee",
	null as "PIK / PIK'able For Floating Rate Loans",
	null as "PIK / PIK'able For Fixed Rate Loans",
	null as "Interest Paid",
	bs."[ACM] [COI/LC] S&P Industry" as "Obligor Industry",
	ss."[SI] Currency" as "Currency (USD / CAD / AUD / EUR)",
	ss."[SI] Obligor Country" as "Obligor Country",
	case when pbb."DIP Loans" = 0 then 'N' when pbb."DIP Loans" = 1 then 'Y' else null end as "DIP Loan (Y/N)",
	case when pbb."Obligations w/ Warrants attached" = 0 then 'N' when pbb."Obligations w/ Warrants attached" = 1 then 'Y' else null end as "Warrants to Purchase Equity (Y/N)",
	case when pbb."Participations" = 0 then 'N' when pbb."Participations" = 1 then 'Y' else null end as "Parti-cipation (Y/N)",
	case when pbb."Convertible into Equity" = 0 then 'N' when pbb."Convertible into Equity" = 1 then 'Y' else null end as "Convertible to Equity (Y/N)",
	pbb."Equity Security" as "Equity Security (Y/N)",
	pbb."Subject of an Offer or Called for Redemption" as "At Acquisition - Subject to offer or called for redemption (Y/N)",
	pbb."Margin Stock" as "Margin Stock (Y/N)",
	pbb."Subject to Withholding Tax" as "Subject to withholding tax (Y/N)",
	pbb."Defaulted Collateral Loan at Acquisition" as "At Acquisition - Defaulted Collateral Loan",
	pbb."Zero Coupon Obligation" as "Zero Coupon Obligation (Y/N)",
	pbb."Covenant Lite" as "Covenant Lite (Y/N)",
	pbb."Structured Finance Obligation / finance lease" as "Structured Finance Obligation, finance lease or chattel paper (Y/N)",
	pbb."Material Non-Credit Related Risk" as "Material Non-Credit Related Risk (Y/N)",
	pbb."Primarily Secured by Real Estate" as "Primarily Secured by Real Estate, Construction Loan or Project Finance Loan (Y/N)",
	pbb."Interest Only Security" as "Interest Only Security (Y/N)",
	pbb."Satisfies Other Criteria(1)" as "Satisfies all Other Eligibility Criteria (Y/N)",
	null as "Excess Concentration Amount (HARD CODE on Last Day of Reinvestment Period)"*/
from pflt_us_bank_holdings usbh
left join pflt_client_Holdings ch on ch."Issuer/Borrower Name" = usbh."Issuer/Borrower Name"
	and ch."Current Par Amount (Issue Currency) - Settled" = usbh."Current Par Amount (Issue Currency) - Settled"
left join pflt_security_mapping sm on sm.cashfile_security_name = usbh."Security/Facility Name"
left join pflt_securities_stats ss on ss."Security" = sm.master_comp_security_name
left join pflt_pflt_borrowing_base pbb on pbb."Security" = ss."Security"
left join pflt_borrower_stats bs on bs."Company" = ss."Family Name"
where usbh.source_file_id= :cash_file_id AND ch.source_file_id= :cash_file_id AND ss.source_file_id= :master_comp_file_id AND pbb.source_file_id= :master_comp_file_id AND bs.source_file_id= :master_comp_file_id
    group by usbh."Issuer/Borrower Name", usbh."Security/Facility Name", pbb."Defaulted Collateral Loan at Acquisition",
	ss."Security", pbb."Credit Improved Loan", usbh."Original Purchase Price", pbb."Stretch Senior (Y/N)", ch."Issue Name",
	ch."Deal Issue (Derived) Rating - Moody's", ch."Deal Issue (Derived) Rating - S&P", bs."[ACM] [C-ACM(AC] Closing Fixed Charge Coverage Ratio",
	bs."[ACM] [C-ACM(AC] Closing Debt to Capitalization", pbb."Senior Debt", pbb."LTM EBITDA", pbb."Total Debt",
	pbb."Closing LTM EBITDA", pbb."Current LTM EBITDA", ch."As Of Date", usbh."Maturity Date", ss."[SI] Type of Rate",
	ss."[SI] LIBOR Floor", bs."[ACM] [COI/LC] S&P Industry", ss."[SI] Currency", ss."[SI] Obligor Country",
	pbb."DIP Loans", pbb."Obligations w/ Warrants attached", pbb."Participations", pbb."Convertible into Equity",
	pbb."Equity Security", pbb."Subject of an Offer or Called for Redemption", pbb."Margin Stock", pbb."Subject to Withholding Tax", pbb."Zero Coupon Obligation",
	pbb."Covenant Lite", pbb."Structured Finance Obligation / finance lease", pbb."Material Non-Credit Related Risk", pbb."Primarily Secured by Real Estate",
	pbb."Interest Only Security", pbb."Satisfies Other Criteria(1)", bs."[ACM] [C-ACM(AC] Closing Fixed Charge Coverage Ratio", bs."[ACM] [C-ACM(AC] 1st Lien Net Debt / EBITDA",
	bs."[CM] [CLSO] 1st Lien Net Debt / EBITDA", bs."[ACM] [C-ACM(AC] HoldCo Net Debt / EBITDA", ss."[SI] Cash Spread to LIBOR", ss."[SI] PIK Coupon"
order by usbh."Security/Facility Name"'''), {'cash_file_id': cash_file_details.id, 'master_comp_file_id':master_comp_file_details.id}).fetchall())
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