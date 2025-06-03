from datetime import datetime
from itertools import zip_longest
from flask import (
    Flask,
    request,
    jsonify,
    render_template,
    send_from_directory,
    session,
    send_file,
    make_response,
)
import pandas as pd
from numerize import numerize

from models import db, Fund, ConcentrationTest, FundConcentrationTest
from source.config import Config


def get_concentration_test_master_list_function():
    try:
        data = request.get_json()
        fund_name = data.get("fund_name")
        fund = Fund.query.filter_by(fund_name=fund_name).first()
        fund_tests = (
            db.session.query(
                ConcentrationTest.test_name,
                ConcentrationTest.description,
                ConcentrationTest.mathematical_formula,
                ConcentrationTest.columns,
                FundConcentrationTest.limit_percentage,
                FundConcentrationTest.show_on_dashboard,
                FundConcentrationTest.id,
            )
            .join(FundConcentrationTest)
            .filter(FundConcentrationTest.fund_id == fund.id)
            .all()
        )

        test_list = []
        for test in fund_tests:
            limit_percentage = test.limit_percentage
            if test.test_name not in [
                
                "Max. Weighted Average Maturity (Years)",
                "Max. Weighted Average Leverage thru Borrower",
            ]:
                limit_percentage = test.limit_percentage * 100
            if limit_percentage == 0:
                limit_percentage = ""
            test_list.append(
                {
                    "fund_test_id": test.id,
                    "test_name": test.test_name,
                    "description": test.description,
                    "mathematical_formula": test.mathematical_formula,
                    "columns": test.columns,
                    "limit_percentage": limit_percentage,
                    "show_on_dashboard": test.show_on_dashboard,
                    "eligible_funds": list(
                        Config().data["fund_std_col_map"][test.test_name].keys()
                    ),
                }
            )

        return (
            jsonify(
                {
                    "error_status": False,
                    "columns": [
                        {"key": "test_name", "title": "Concentration Test"},
                        {"key": "description", "title": "Description "},
                        {
                            "key": "mathematical_formula",
                            "title": "Mathematical Formula",
                        },
                        # {"key": "columns", "title": "Columns"},
                        {"key": "limit_percentage", "title": "Concentration Limit"},
                        {"key": "eligible_funds", "title": "Applicable Funds"},
                        {"key": "show_on_dashboard", "title": "Show On Dashboard"},
                    ],
                    "data": test_list,
                }
            ),
            200,
        )
    except Exception as e:
        return (
            jsonify(
                {
                    "error": str(e),
                    "error_type": str(type(e).__name__),
                    "error_file_details": f"error on line {e.__traceback__.tb_lineno} inside {__file__}",
                }
            ),
            500,
        )


def change_conc_test_config_function():
    try:
        data = request.get_json()
        test_changes = data["changes"]

        for test in test_changes:
            test_id = test["fund_test_id"]
            limit_percentage = test.get("limit_percentage")
            show_on_dashboard = test.get("show_on_dashboard")

            fund_test = FundConcentrationTest.query.filter_by(id=test_id).first()
            cocentration_test = ConcentrationTest.query.filter_by(
                id=fund_test.test_id
            ).first()
            if cocentration_test.test_name in [
                
                "Max. Weighted Average Maturity (Years)",
                "Max. Weighted Average Leverage thru Borrower",
            ]:
                if limit_percentage:
                    fund_test.limit_percentage = float(limit_percentage)
            else:
                if limit_percentage:
                    fund_test.limit_percentage = int(limit_percentage) / 100
            if show_on_dashboard is not None:
                fund_test.show_on_dashboard = show_on_dashboard

            db.session.add(fund_test)
            db.session.commit()

        return jsonify(
            {
                "error_status": False,
                "message": "Concentration test config updated successfully",
            }
        )
    except Exception as e:
        return (
            jsonify(
                {
                    "error": str(e),
                    "error_type": str(type(e).__name__),
                    "error_file_details": f"error on line {e.__traceback__.tb_lineno} inside {__file__}",
                }
            ),
            500,
        )


# def apply_concentration_test_function():
#     try:
#         data = request.get_json()
#         fund_std_col_map = Config.data["fund_std_col_map"]
#         print(fund_std_col_map)
#         return jsonify({"MSG": "Check console"})
#     except Exception as e:
#         return (
#             jsonify(
#                 {
#                     "error": str(e),
#                     "error_type": str(type(e).__name__),
#                     "error_file_details": f"error on line {e.__traceback__.tb_lineno} inside {__file__}",
#                 }
#             ),
#             500,
#         )


class ConcentrationTestExecutor:
    def __init__(self, calculated_df_map, fund_name):
        self.calculated_df_map = calculated_df_map
        self.fund_name = fund_name
        self.fund_std_col_map = Config().data["fund_std_col_map"]
        self.test_library = {
            "Max. Industry Concentration (% BB)": self.execute_Max_Industry_Concentration_percent_BB,
            "Min. Eligible Issuers (#)": self.execute_Min_Eligible_Issuers,
            "Number of Issuers": self.execute_number_of_issuers,
            "Second Lien and Split Lien": self.execute_Second_Lien_and_Split_Lien,
            "Second Lien": self.execute_Second_Lien,
            "DIP Collateral Loans": self.execute_DIP_Collateral_Loans,
            "Max. LTV Transactions": self.execute_Max_LTV_Transactions,
            "Max. Foreign Eligible Portfolio Investments": self.execute_Max_Foreign_Eligible_Portfolio_Investments,
            "Max. Warehouse Assets": self.execute_Max_Warehouse_Assets,
            "Max. Contribution to BB with Maturity > 8 years": self.Max_Contribution_to_BB_with_Maturity_greater_than_8_years,
            "Max. Industry Concentration (Largest Industry, % BB)": self.Max_Industry_Concentration_Largest_Industry_percent_BB,
            "Max. Industry Concentration (2nd Largest Industry, % BB)": self.Max_Industry_Concentration_2nd_Largest_Industry_percent_BB,
            "First Lien Three Largest Obligors (each)": self.first_lien_three_largest_obligors_each,
            "Other Obligors": self.other_obligors,
            "Third Largest Industry": self.third_largest_industry,
            "Other Industry": self.other_industry,
            "Largest Industry": self.largest_industry,
            "Second Largest Industry": self.second_largest_industry,
            "EBITDA < $10MM": self.ebitda_less_than_10MM,
            "DIP Loans": self.dip_loans,
            "DDTL and Revolving Loans": self.ddtl_revolving_loans,
            "Pay Less Frequently than Quarterly": self.pay_less_frequently_than_quarterly,
            "Loans denominated in Approved Foreign Currency": self.loans_denominated_in_approved_foreign_currency,
            "Loans to Obligors domiciled in Approved Foreign Country": self.loans_to_obligors_domiciled_in_approved_foreign_country,
            "Cov-Lite": self.cov_lite,
            "Tier 3 Obligors (Measured at Inclusion)": self.tier_3_obligors_measured_at_inclusion,
            "Second Lien Loans": self.second_lien_loans,
            "First Lien Last Out": self.first_lien_last_out,
            "Loans with Remaining Maturity > 6 Years": self.loans_with_remaining_maturity_gt_6_years,
            "Recurring Revenue Loans": self.recurring_revenue_loans,
            "Fixed Rate Loans": self.fixed_rate_loans,
            "Max. Weighted Average Leverage thru Borrower": self.max_weighted_average_leverage_thru_borrower,
            "Min. Cash, First Lien, and Cov-Lite": self.min_cash_first_lien_cov_lite,
            "Min. Senior Secured": self.min_senior_secured,
            "Min. Weighted Average Cash Fixed Coupon": self.min_weighted_average_cash_fixed_coupon,
            "Min. Weighted Average Cash Floating Coupon": self.min_weighted_average_cash_floating_coupon,
            "Max. Third Party Finance Companies": self.max_third_party_finance_companies,
            "Max. Affiliate Investments": self.max_affiliate_investments,
            "Max. PIK, DIP": self.max_pik_dip,
            "Max. Issuer Concentration (% BB)": self.max_issuer_concentration_percent_bb,
            "Max. Weighted Average Maturity (Years)": self.max_weighted_average_maturity_years,
            "Partial PIK Loan": self.partial_pik_loan,
            "Discount Collateral Loans": self.discount_collateral_loans,
            "Credit Improved Loans": self.credit_improved_loans,
            "Warrants to Purchase Equity Securities": self.warrants_to_purchase_equity_securities,
            "LBO Loan": self.lbo_loan,
            "Participation Interests": self.participation_interests,
            "Eligible Covenant Lite Loans": self.eligible_covenant_lite_loans,
            "Top 5 Obligors": self.top_5_bligors,
            "LTM EBITDA < 15,000,000": self.ltm_ebitda_lt_15MM,
            "LTM EBITDA >= 5,000,000 but < 7,500,000": self.ltm_ebitda_gt_5MM_lt_7_5MM,
            "Leverage Limitations": self.leverage_limitations,
            "Max. Industry Concentration (All Other Industries, % BB)": self.max_industry_concentration_all_other_industries
        }

    def get_applicable_limit(self, limit_percent, total_bb, min_limit):
        if min_limit is not None:
            applicable_test_limit = max(limit_percent * total_bb, min_limit)
        else:
            applicable_test_limit = limit_percent * total_bb
        return applicable_test_limit

    def update_conc_test_df(self, test_name, test_required_col_df, actual, show_on_dashboard, concentration_test_df):
        total_bb = test_required_col_df["Borrowing Base"].sum()

        applicable_test_limit = self.get_applicable_limit(limit_percent=self.limit_percent, total_bb=total_bb, min_limit=self.min_limit)

        if actual > applicable_test_limit:
            result = "Fail"
        else:
            result = "Pass"

        row_data = {
            "Concentration Tests": [test_name],
            "Concentration Limit": [applicable_test_limit],
            "Actual": [actual],
            "Result": [result],
            "Show on dashboard": [show_on_dashboard],
            "Absolute Limit": [self.min_limit],
            "Percent Limit": [self.limit_percent]
        }
        row_df = pd.DataFrame(row_data)
        concentration_test_df = pd.concat([concentration_test_df, row_df], ignore_index=True)
        return concentration_test_df

    def get_kth_largest_percent_BB(self, test_required_col_df, k):
        percent_BB_list = test_required_col_df["Percetage Borrowing Base"].tolist()
        percent_BB_list.sort(reverse=True)
        return percent_BB_list[k - 1]
    
    def get_kth_largest_BB(self, test_required_col_df, k):
        percent_BB_list = test_required_col_df["Borrowing Base"].tolist()
        percent_BB_list.sort(reverse=True)
        return percent_BB_list[k - 1]

    def is_pass(self, limit, actual, comparison_type):
        if actual != actual:
            actual = 0
        if comparison_type == 'LessEqual':
            return actual <= limit
        if comparison_type == 'Greater':
            return actual > limit
        if comparison_type == 'GreaterEqual':
            return actual >= limit
        if comparison_type == 'Equal':
            return actual == limit
        return False

    def get_standard_column_names(self, test_name):
        # get standard column for the fund
        test_mapping = self.fund_std_col_map.get(test_name, {})
        fund_columns = test_mapping.get(self.fund_name, {})
        return fund_columns

    def get_dataframe_column(self, sheet_name, column_name):
        dataframe = self.calculated_df_map.get(sheet_name)
        return dataframe[column_name].tolist()

    def execute_Max_Industry_Concentration_percent_BB(
        self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type
    ):
        test_required_col_df = (
            test_required_col_df.groupby("Industry")
            .agg({"Borrowing Base": "sum"})
            .reset_index()
        )
        max_bb = test_required_col_df["Borrowing Base"].max()
        actual_percent = max_bb / test_required_col_df["Borrowing Base"].sum()
        rounded_actual = round(actual_percent, 3)
        if rounded_actual <= self.limit_percent:
            result = "Pass"
        else:
            result = "Fail"
        row_data = {
            "Concentration Tests": [test_name],
            "Concentration Limit": [self.limit_percent],
            "Actual": [rounded_actual],
            "Result": [result],
            "Show on dashboard": [show_on_dashboard]
        }
        row_df = pd.DataFrame(row_data)
        concentration_test_df = pd.concat(
            [concentration_test_df, row_df], ignore_index=True
        )
        return concentration_test_df

    def execute_Min_Eligible_Issuers(
        self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type):
        actual = test_required_col_df["Eligible Issuer"].max()
        if self.is_pass(actual=actual, limit=self.limit_percent, comparison_type=comparison_type):
            result = result = "Pass"
        else:
            result = "Fail"
        row_data = {
            "Concentration Tests": [test_name],
            "Concentration Limit": [self.limit_percent],
            "Actual": [actual],
            "Result": [result],
            "Show on dashboard": [show_on_dashboard]
        }
        row_df = pd.DataFrame(row_data)
        concentration_test_df = pd.concat(
            [concentration_test_df, row_df], ignore_index=True
        )
        return concentration_test_df

    def execute_number_of_issuers(
        self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type
    ):
        actual = test_required_col_df["Eligible Issuer"].max()
        if self.is_pass(actual=actual, limit=self.limit_percent, comparison_type=comparison_type):
            result = result = "Pass"
        else:
            result = "Fail"
        row_data = {
            "Concentration Tests": [test_name],
            "Concentration Limit": [self.limit_percent],
            "Actual": [actual],
            "Result": [result],
            "Show on dashboard": [show_on_dashboard]
        }
        row_df = pd.DataFrame(row_data)
        concentration_test_df = pd.concat(
            [concentration_test_df, row_df], ignore_index=True
        )
        return concentration_test_df

    def execute_Second_Lien_and_Split_Lien(
        self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type
    ):
        total_borrowing_base = test_required_col_df.loc[
            test_required_col_df["Terms"]
            == "Concentration Test Amount",
            "Values",
        ].iloc[0]

        applicable_limit = total_borrowing_base * self.limit_percent

        actual = test_required_col_df["Second Lien and Split Lien"].sum()

        if self.is_pass(limit=applicable_limit, actual=actual, comparison_type=comparison_type) :
            result = "Pass"
        else:
            result = "Fail"
        row_data = {
            "Concentration Tests": [test_name],
            "Concentration Limit": [applicable_limit],
            "Actual": [actual],
            "Result": [result],
            "Show on dashboard": [show_on_dashboard]
        }
        row_df = pd.DataFrame(row_data)
        concentration_test_df = pd.concat(
            [concentration_test_df, row_df], ignore_index=True
        )
        return concentration_test_df

    def execute_Second_Lien(
        self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type
    ):
        total_borrowing_base = test_required_col_df.loc[test_required_col_df["Terms"] == "Concentration Test Amount", "Values"].iloc[0]

        applicable_limit = total_borrowing_base * self.limit_percent

        actual = test_required_col_df["Second Lien"].sum() / total_borrowing_base 
        
        if self.is_pass(limit=applicable_limit, actual=actual, comparison_type=comparison_type) :
            result = "Pass"
        else:
            result = "Fail"
        row_data = {
            "Concentration Tests": [test_name],
            "Concentration Limit": [applicable_limit],
            "Actual": [actual],
            "Result": [result],
            "Show on dashboard": [show_on_dashboard]
        }
        row_df = pd.DataFrame(row_data)
        concentration_test_df = pd.concat(
            [concentration_test_df, row_df], ignore_index=True
        )
        return concentration_test_df
    
    def execute_DIP_Collateral_Loans(
        self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type
    ):
        total_borrowing_base = test_required_col_df.loc[
            test_required_col_df["Terms"]
            == "BORROWING BASE - (A) minus (B) minus (A)(iv)",
            "Values",
        ].iloc[0]

        actual = (
            test_required_col_df["DIP Collateral Loans"].sum() / total_borrowing_base
        )
        if actual < self.limit_percent:
            result = "Pass"
        else:
            result = "Fail"
        row_data = {
            "Concentration Tests": [test_name],
            "Concentration Limit": [self.limit_percent],
            "Actual": [actual],
            "Result": [result],
            "Show on dashboard": [show_on_dashboard]
        }
        row_df = pd.DataFrame(row_data)
        concentration_test_df = pd.concat(
            [concentration_test_df, row_df], ignore_index=True
        )
        return concentration_test_df

    def execute_Max_LTV_Transactions(
        self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type
    ):
        total_bb = test_required_col_df["Borrowing Base"].sum()
        actual = test_required_col_df[test_required_col_df["LTV Transaction"] == "Yes"]["Borrowing Base"].sum()
        actual_percent = actual / total_bb

        if self.is_pass(actual=actual_percent, limit=self.limit_percent, comparison_type=comparison_type):
            result = result = "Pass"
        else:
            result = "Fail"

        row_data = {
            "Concentration Tests": [test_name],
            "Concentration Limit": [self.limit_percent],
            "Actual": [actual_percent],
            "Result": [result],
            "Show on dashboard": [show_on_dashboard]
        }
        row_df = pd.DataFrame(row_data)
        concentration_test_df = pd.concat(
            [concentration_test_df, row_df], ignore_index=True
        )
        return concentration_test_df

    def execute_Max_Foreign_Eligible_Portfolio_Investments(
        self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type
    ):
        approved_foreign_jurisdiction_df = (
            test_required_col_df.groupby("Approved Foreign Jurisdiction")
            .agg({"Borrowing Base": "sum"})
            .reset_index()
        )
        yes_sum = 0
        for index, row in approved_foreign_jurisdiction_df.iterrows():
            if row["Approved Foreign Jurisdiction"] == "Yes":
                yes_sum = row["Borrowing Base"]

        actual = yes_sum / approved_foreign_jurisdiction_df["Borrowing Base"].sum()

        if self.is_pass(actual=actual, limit=self.limit_percent, comparison_type=comparison_type):
            result = result = "Pass"
        else:
            result = "Fail"

        row_data = {
            "Concentration Tests": [test_name],
            "Concentration Limit": [self.limit_percent],
            "Actual": [actual],
            "Result": [result],
            "Show on dashboard": [show_on_dashboard]
        }
        row_df = pd.DataFrame(row_data)
        concentration_test_df = pd.concat(
            [concentration_test_df, row_df], ignore_index=True
        )
        return concentration_test_df

    def execute_Max_Warehouse_Assets(
        self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type
    ):
        warehouse_assetn_df = (
            test_required_col_df.groupby("Warehouse Asset")
            .agg({"Borrowing Base": "sum"})
            .reset_index()
        )
        yes_sum = 0
        for index, row in warehouse_assetn_df.iterrows():
            if row["Warehouse Asset"] == "Yes":
                yes_sum = row["Borrowing Base"]

        actual = yes_sum / warehouse_assetn_df["Borrowing Base"].sum()

        rounded_actual = round(actual, 3)
        if self.is_pass(actual=actual, limit=self.limit_percent, comparison_type=comparison_type):
            result = result = "Pass"
        else:
            result = "Fail"

        row_data = {
            "Concentration Tests": [test_name],
            "Concentration Limit": [self.limit_percent],
            "Actual": [rounded_actual],
            "Result": [result],
            "Show on dashboard": [show_on_dashboard]
        }
        row_df = pd.DataFrame(row_data)
        concentration_test_df = pd.concat(
            [concentration_test_df, row_df], ignore_index=True
        )
        return concentration_test_df

    def Max_Contribution_to_BB_with_Maturity_greater_than_8_years(
        self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type
    ):
        detemination_date = test_required_col_df.loc[
            test_required_col_df["Terms"] == "Date of determination:", "Values"
        ].values[0]

        current_date = pd.to_datetime(datetime.now())

        test_required_col_df['Maturity Date'] = pd.to_datetime(test_required_col_df['Maturity Date'])
        # Calculate the difference between 'Maturity Date' and the current date in days
        test_required_col_df["Tenor"] = (
            test_required_col_df["Maturity Date"] - detemination_date
        ).dt.days / 365.0
        # test_required_col_df["Tenor"] = (test_required_col_df["Maturity Date"] - detemination_date) / 365

        actual = 0
        sum_of_BB = 0
        bb_sum = test_required_col_df["Borrowing Base"].sum()
        for index, row in test_required_col_df.iterrows():
            if row["Tenor"] > 8:
                actual = sum_of_BB + row["Borrowing Base"] / bb_sum
        
        rounded_actual = round(actual, 3)
        if self.is_pass(actual=actual, limit=self.limit_percent, comparison_type=comparison_type):
            result = result = "Pass"
        else:
            result = "Fail"

        row_data = {
            "Concentration Tests": [test_name],
            "Concentration Limit": [self.limit_percent],
            "Actual": [rounded_actual],
            "Result": [result],
            "Show on dashboard": [show_on_dashboard]
        }
        row_df = pd.DataFrame(row_data)
        concentration_test_df = pd.concat(
            [concentration_test_df, row_df], ignore_index=True
        )
        return concentration_test_df

    def Max_Industry_Concentration_Largest_Industry_percent_BB(
        self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type
    ):
        test_required_col_df = (
            test_required_col_df.groupby("Industry")
            .agg({"Borrowing Base": "sum"})
            .reset_index()
        )
        test_required_col_df = test_required_col_df[test_required_col_df["Industry"] != "Total"]
        BB_sum = test_required_col_df["Borrowing Base"].sum()
        test_required_col_df["Percetage Borrowing Base"] = (
            test_required_col_df["Borrowing Base"] / BB_sum
        )

        # check after demo
        if test_required_col_df.empty:
            return concentration_test_df
        actual = self.get_kth_largest_percent_BB(test_required_col_df, 1)
        rounded_actual = round(actual, 3)
        if self.is_pass(actual=actual, limit=self.limit_percent, comparison_type=comparison_type):
            result = result = "Pass"
        else:
            result = "Fail"

        row_data = {
            "Concentration Tests": [test_name],
            "Concentration Limit": [self.limit_percent],
            "Actual": [rounded_actual],
            "Result": [result],
            "Show on dashboard": [show_on_dashboard]
        }
        row_df = pd.DataFrame(row_data)
        concentration_test_df = pd.concat(
            [concentration_test_df, row_df], ignore_index=True
        )
        return concentration_test_df

    def Max_Industry_Concentration_2nd_Largest_Industry_percent_BB(
        self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type
    ):
        test_required_col_df = (
            test_required_col_df.groupby("Industry")
            .agg({"Borrowing Base": "sum"})
            .reset_index()
        )
        test_required_col_df = test_required_col_df[test_required_col_df["Industry"] != "Total"]
        BB_sum = test_required_col_df["Borrowing Base"].sum()
        test_required_col_df["Percetage Borrowing Base"] = (
            test_required_col_df["Borrowing Base"] / BB_sum
        )

        # check after demo
        if test_required_col_df.empty:
            return concentration_test_df

        actual = self.get_kth_largest_percent_BB(test_required_col_df, 2)
        rounded_actual = round(actual, 3)
        if self.is_pass(actual=actual, limit=self.limit_percent, comparison_type=comparison_type):
            result = result = "Pass"
        else:
            result = "Fail"

        row_data = {
            "Concentration Tests": [test_name],
            "Concentration Limit": [self.limit_percent],
            "Actual": [rounded_actual],
            "Result": [result],
            "Show on dashboard": [show_on_dashboard]
        }
        row_df = pd.DataFrame(row_data)
        concentration_test_df = pd.concat(
            [concentration_test_df, row_df], ignore_index=True
        )
        return concentration_test_df

    def first_lien_three_largest_obligors_each(self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type):
        test_required_col_df = test_required_col_df[test_required_col_df["Loan Type"] == "First Lien"]
        test_required_col_df = test_required_col_df.sort_values(by='Borrowing Base', ascending=False)
        total_bb = test_required_col_df["Borrowing Base"].sum()
        total_exess = test_required_col_df["Exess"].sum()
        applicable_test_limit = max(self.limit_percent * total_bb, self.min_limit)
        test_required_col_df = test_required_col_df.head(3)

        # test_passed = (test_required_col_df['Borrowing Base'] <= applicable_test_limit).all()
        if total_exess > 0:
            result = "Fail"
        else:
            result = "Pass"

        # if test_passed:
        #     result = "Pass"
        # else:
        #     result = "Fail"
        actual = (total_bb - total_exess) / total_bb
        rounded_actual = round(actual, 3)
        row_data = {
            "Concentration Tests": [test_name],
            "Concentration Limit": [self.limit_percent],
            "Actual": [rounded_actual],
            "Result": [result],
            "Show on dashboard": [show_on_dashboard]
        }
        row_df = pd.DataFrame(row_data)
        concentration_test_df = pd.concat([concentration_test_df, row_df], ignore_index=True)
        return concentration_test_df

    def other_obligors(self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type):
        test_required_col_df = test_required_col_df.sort_values(by='Borrowing Base', ascending=False)
        total_bb = test_required_col_df["Borrowing Base"].sum()
        total_exess = test_required_col_df["Excess"].sum()
        test_required_col_df = test_required_col_df.iloc[3:4]
        applicable_test_limit = max(self.limit_percent * total_bb, self.min_limit)
        actual = test_required_col_df["Revised Value"].sum()

        # test_passed = (test_required_col_df['Borrowing Base'] <= applicable_test_limit).all()

        if actual > applicable_test_limit:
                result = "Fail"
        else:
            result = "Pass"

        row_data = {
            "Concentration Tests": [test_name],
            "Concentration Limit": [applicable_test_limit],
            "Actual": [actual],
            "Result": [result],
            "Show on dashboard": [show_on_dashboard],
            "Absolute Limit": [self.min_limit],
            "Percent Limit": [self.limit_percent]
        }
        row_df = pd.DataFrame(row_data)
        concentration_test_df = pd.concat([concentration_test_df, row_df], ignore_index=True)
        return concentration_test_df

    def third_largest_industry(self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type):
        test_required_col_df = test_required_col_df.sort_values(by='Borrowing Base', ascending=False)
        total_bb = test_required_col_df["Borrowing Base"].sum()
        # total_exess = test_required_col_df["Excess"].sum()
        # test_required_col_df = test_required_col_df.iloc[3:]
        applicable_test_limit = max(self.limit_percent * total_bb, self.min_limit)

        # test_passed = (test_required_col_df['Borrowing Base'] <= applicable_test_limit).all()

        test_required_col_df = (
            test_required_col_df.groupby("Industry")
            .agg({"Borrowing Base": "sum"})
            .reset_index()
        )
        # test_required_col_df["Percetage Borrowing Base"] = (
        #     test_required_col_df["Borrowing Base"] / BB_sum
        # )

        # check after demo
        if test_required_col_df.empty:
            return concentration_test_df
        actual = self.get_kth_largest_BB(test_required_col_df, 3) # 3rd largest borrowing base value for an industry

        if actual > applicable_test_limit:
            result = "Fail"
        else:
            result = "Pass"

        row_data = {
            "Concentration Tests": [test_name],
            "Concentration Limit": [applicable_test_limit],
            "Actual": [actual],
            "Result": [result],
            "Show on dashboard": [show_on_dashboard],
            "Absolute Limit": [self.min_limit],
            "Percent Limit": [self.limit_percent]
        }
        row_df = pd.DataFrame(row_data)
        concentration_test_df = pd.concat([concentration_test_df, row_df], ignore_index=True)
        return concentration_test_df

    def other_industry(self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type):
        test_required_col_df = test_required_col_df.sort_values(by='Borrowing Base', ascending=False)
        total_bb = test_required_col_df["Borrowing Base"].sum()
        # total_exess = test_required_col_df["Excess"].sum()
        # test_required_col_df = test_required_col_df.iloc[3:]
        applicable_test_limit = max(self.limit_percent * total_bb, self.min_limit)

        # test_passed = (test_required_col_df['Borrowing Base'] <= applicable_test_limit).all()

        test_required_col_df = (
            test_required_col_df.groupby("Industry")
            .agg({"Borrowing Base": "sum"})
            .reset_index()
        )
        # test_required_col_df["Percetage Borrowing Base"] = (
        #     test_required_col_df["Borrowing Base"] / BB_sum
        # )

        # check after demo
        if test_required_col_df.empty:
            return concentration_test_df
        actual = self.get_kth_largest_BB(test_required_col_df, 4) # all other than top 3 industries as df is sorted (desc) order of bb value.

        if actual > applicable_test_limit:
            result = "Fail"
        else:
            result = "Pass"

        row_data = {
            "Concentration Tests": [test_name],
            "Concentration Limit": [applicable_test_limit],
            "Actual": [actual],
            "Result": [result],
            "Show on dashboard": [show_on_dashboard],
            "Absolute Limit": [self.min_limit],
            "Percent Limit": [self.limit_percent]
        }
        row_df = pd.DataFrame(row_data)
        concentration_test_df = pd.concat([concentration_test_df, row_df], ignore_index=True)
        return concentration_test_df

    def largest_industry(self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type):
        test_required_col_df = test_required_col_df.sort_values(by='Borrowing Base', ascending=False)
        total_bb = test_required_col_df["Borrowing Base"].sum()
        # total_exess = test_required_col_df["Excess"].sum()
        # test_required_col_df = test_required_col_df.iloc[3:]
        applicable_test_limit = max(self.limit_percent * total_bb, self.min_limit)

        # test_passed = (test_required_col_df['Borrowing Base'] <= applicable_test_limit).all()

        test_required_col_df = (
            test_required_col_df.groupby("Industry")
            .agg({"Borrowing Base": "sum"})
            .reset_index()
        )
        # test_required_col_df["Percetage Borrowing Base"] = (
        #     test_required_col_df["Borrowing Base"] / BB_sum
        # )

        # check after demo
        if test_required_col_df.empty:
            return concentration_test_df
        actual = self.get_kth_largest_BB(test_required_col_df, 1) # largest borrowing base value for an industry

        if actual > applicable_test_limit:
            result = "Fail"
        else:
            result = "Pass"

        row_data = {
            "Concentration Tests": [test_name],
            "Concentration Limit": [applicable_test_limit],
            "Actual": [actual],
            "Result": [result],
            "Show on dashboard": [show_on_dashboard],
            "Absolute Limit": [self.min_limit],
            "Percent Limit": [self.limit_percent]
        }
        row_df = pd.DataFrame(row_data)
        concentration_test_df = pd.concat([concentration_test_df, row_df], ignore_index=True)
        return concentration_test_df

    def second_largest_industry(self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type):
        test_required_col_df = test_required_col_df.sort_values(by='Borrowing Base', ascending=False)
        total_bb = test_required_col_df["Borrowing Base"].sum()
        # total_exess = test_required_col_df["Excess"].sum()
        # test_required_col_df = test_required_col_df.iloc[3:]
        applicable_test_limit = max(self.limit_percent * total_bb, self.min_limit)

        # test_passed = (test_required_col_df['Borrowing Base'] <= applicable_test_limit).all()

        test_required_col_df = (
            test_required_col_df.groupby("Industry")
            .agg({"Borrowing Base": "sum"})
            .reset_index()
        )
        # test_required_col_df["Percetage Borrowing Base"] = (
        #     test_required_col_df["Borrowing Base"] / BB_sum
        # )

        # check after demo
        if test_required_col_df.empty:
            return concentration_test_df
        actual = self.get_kth_largest_BB(test_required_col_df, 2) # 2nd largest borrowing base value for an industry

        if actual > applicable_test_limit:
            result = "Fail"
        else:
            result = "Pass"

        row_data = {
            "Concentration Tests": [test_name],
            "Concentration Limit": [applicable_test_limit],
            "Actual": [actual],
            "Result": [result],
            "Show on dashboard": [show_on_dashboard],
            "Absolute Limit": [self.min_limit],
            "Percent Limit": [self.limit_percent]
        }
        row_df = pd.DataFrame(row_data)
        concentration_test_df = pd.concat([concentration_test_df, row_df], ignore_index=True)
        return concentration_test_df

    def ebitda_less_than_10MM(self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type):
        try:
            actual = test_required_col_df.loc[test_required_col_df["Permitted TTM EBITDA (USD)"] < 10000000, "Revised Value"].sum()

            total_bb = test_required_col_df["Borrowing Base"].sum()

            applicable_test_limit = max(self.limit_percent * total_bb, self.min_limit)

            if actual > applicable_test_limit:
                result = "Fail"
            else:
                result = "Pass"

            row_data = {
                "Concentration Tests": [test_name],
                "Concentration Limit": [applicable_test_limit],
                "Actual": [actual],
                "Result": [result],
                "Show on dashboard": [show_on_dashboard],
                "Absolute Limit": [self.min_limit],
                "Percent Limit": [self.limit_percent]
            }
            row_df = pd.DataFrame(row_data)
            concentration_test_df = pd.concat([concentration_test_df, row_df], ignore_index=True)
            return concentration_test_df
        except Exception as e:
            raise Exception()
        
    def dip_loans(self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type):
        actual = test_required_col_df.loc[test_required_col_df["DIP Loan"] == "Yes", "Revised Value"].sum()

        concentration_test_df = self.update_conc_test_df(actual=actual, concentration_test_df=concentration_test_df, test_name=test_name, show_on_dashboard=show_on_dashboard, test_required_col_df=test_required_col_df)

        return concentration_test_df
    
    def ddtl_revolving_loans(self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type):
        actual = test_required_col_df[(test_required_col_df['Revolver'] == 'Yes') | (test_required_col_df['DDTL'] == 'Yes')]['Revised Value'].sum()

        concentration_test_df = self.update_conc_test_df(actual=actual, concentration_test_df=concentration_test_df, test_name=test_name, show_on_dashboard=show_on_dashboard, test_required_col_df=test_required_col_df)

        return concentration_test_df

    def pay_less_frequently_than_quarterly(self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type):
        actual = test_required_col_df[test_required_col_df['Paid Less than Qtrly'] == 'Yes']['Revised Value'].sum()

        concentration_test_df = self.update_conc_test_df(actual=actual, concentration_test_df=concentration_test_df, test_name=test_name, show_on_dashboard=show_on_dashboard, test_required_col_df=test_required_col_df)
        return concentration_test_df
    
    def loans_denominated_in_approved_foreign_currency(self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type):
        actual = test_required_col_df[test_required_col_df['Approved Currency'] != 'USD']['Revised Value'].sum()

        concentration_test_df = self.update_conc_test_df(actual=actual, concentration_test_df=concentration_test_df, test_name=test_name, show_on_dashboard=show_on_dashboard, test_required_col_df=test_required_col_df)
        return concentration_test_df
    
    def loans_to_obligors_domiciled_in_approved_foreign_country(self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type):
        actual = test_required_col_df[test_required_col_df['Approved Country'] != "United States"]['Revised Value'].sum()

        concentration_test_df = self.update_conc_test_df(actual=actual, concentration_test_df=concentration_test_df, test_name=test_name, show_on_dashboard=show_on_dashboard, test_required_col_df=test_required_col_df)
        return concentration_test_df
    
    def cov_lite(self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type):
        actual = test_required_col_df[test_required_col_df['Cov-Lite'] == "Yes"]['Revised Value'].sum()

        concentration_test_df = self.update_conc_test_df(actual=actual, concentration_test_df=concentration_test_df, test_name=test_name, show_on_dashboard=show_on_dashboard, test_required_col_df=test_required_col_df)
        return concentration_test_df
    
    def tier_3_obligors_measured_at_inclusion(self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type):
        actual = test_required_col_df[(test_required_col_df['Eligibility Check'] == 'Yes') & (test_required_col_df['Tier'] == 'Tier 3')]['Revised Value'].sum()

        concentration_test_df = self.update_conc_test_df(actual=actual, concentration_test_df=concentration_test_df, test_name=test_name, show_on_dashboard=show_on_dashboard, test_required_col_df=test_required_col_df)
        return concentration_test_df

    def second_lien_loans(self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type):
        actual = test_required_col_df[test_required_col_df['Loan Type'] == 'Second Lien']['Revised Value'].sum()
        concentration_test_df = self.update_conc_test_df(actual=actual, concentration_test_df=concentration_test_df, test_name=test_name, show_on_dashboard=show_on_dashboard, test_required_col_df=test_required_col_df)
        return concentration_test_df
    
    def first_lien_last_out(self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type):
        actual = test_required_col_df[test_required_col_df['Loan Type'] == 'Last Out']['Revised Value'].sum()
        concentration_test_df = self.update_conc_test_df(actual=actual, concentration_test_df=concentration_test_df, test_name=test_name, show_on_dashboard=show_on_dashboard, test_required_col_df=test_required_col_df)
        return concentration_test_df
    
    def loans_with_remaining_maturity_gt_6_years(self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type):
        actual = test_required_col_df[test_required_col_df['Remaining Term'] > 6]['Revised Value'].sum()
        concentration_test_df = self.update_conc_test_df(actual=actual, concentration_test_df=concentration_test_df, test_name=test_name, show_on_dashboard=show_on_dashboard, test_required_col_df=test_required_col_df)
        return concentration_test_df

    def recurring_revenue_loans(self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type):
        actual = test_required_col_df[test_required_col_df['Loan Type'] == "Recurring Revenue"]['Revised Value'].sum()
        concentration_test_df = self.update_conc_test_df(actual=actual, concentration_test_df=concentration_test_df, test_name=test_name, show_on_dashboard=show_on_dashboard, test_required_col_df=test_required_col_df)
        return concentration_test_df
    
    def fixed_rate_loans(self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type):
        actual = test_required_col_df[test_required_col_df['Is Fixed Rate'] == "Yes"]['Revised Value'].sum()
        concentration_test_df = self.update_conc_test_df(actual=actual, concentration_test_df=concentration_test_df, test_name=test_name, show_on_dashboard=show_on_dashboard, test_required_col_df=test_required_col_df)
        return concentration_test_df

    def max_weighted_average_leverage_thru_borrower(self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type):
        try:
            test_required_col_df["Product"] = test_required_col_df["Leverage"] * test_required_col_df["Percent Adj. Elig. Amount"]
            sum_product = test_required_col_df["Product"].sum()
            actual = sum_product
            test_required_col_df.drop(labels='Product', axis=1, inplace=True)
            if self.is_pass(actual=actual, limit=self.limit_percent, comparison_type=comparison_type):
                result = result = "Pass"
            else:
                result = "Fail"
            row_data = {
                "Concentration Tests": [test_name],
                "Concentration Limit": [self.limit_percent],
                "Actual": [actual],
                "Result": [result],
                "Show on dashboard": [show_on_dashboard],
                "Absolute Limit": [self.min_limit],
                "Percent Limit": [self.limit_percent]
            }
            row_df = pd.DataFrame(row_data)
            concentration_test_df = pd.concat([concentration_test_df, row_df], ignore_index=True)
            return concentration_test_df
        except Exception as e:
            raise Exception(e)

    def min_cash_first_lien_cov_lite(self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type):
        try:
            total_bb = test_required_col_df["Borrowing Base"].sum()
            test_required_col_df = test_required_col_df[test_required_col_df["Investment Type"].isin(["Cash", "First Lien", "Cov-Lite", "Warehouse First Lien"])]
            group_total = test_required_col_df["Borrowing Base"].sum()

            actual = group_total / total_bb

            if self.is_pass(actual=actual, limit=self.limit_percent, comparison_type=comparison_type):
                result = result = "Pass"
            else:
                result = "Fail"
            row_data = {
                "Concentration Tests": [test_name],
                "Concentration Limit": [self.limit_percent],
                "Actual": [actual],
                "Result": [result],
                "Show on dashboard": [show_on_dashboard],
                "Absolute Limit": [self.min_limit],
                "Percent Limit": [self.limit_percent]
            }
            row_df = pd.DataFrame(row_data)
            concentration_test_df = pd.concat([concentration_test_df, row_df], ignore_index=True)
            return concentration_test_df            
        except Exception as e:
            raise Exception(e)

    def min_senior_secured(self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type):
        try:
            total_bb = test_required_col_df["Borrowing Base"].sum()
            test_required_col_df = test_required_col_df[test_required_col_df["Investment Type"].isin(["Cash", "First Lien", "Last Out", "Second Lien", "Cov-Lite", "Warehouse First Lien"])]
            group_total = test_required_col_df["Borrowing Base"].sum()

            actual = group_total / total_bb

            if self.is_pass(actual=actual, limit=self.limit_percent, comparison_type=comparison_type):
                result = result = "Pass"
            else:
                result = "Fail"
            row_data = {
                "Concentration Tests": [test_name],
                "Concentration Limit": [self.limit_percent],
                "Actual": [actual],
                "Result": [result],
                "Show on dashboard": [show_on_dashboard],
                "Absolute Limit": [self.min_limit],
                "Percent Limit": [self.limit_percent]
            }
            row_df = pd.DataFrame(row_data)
            concentration_test_df = pd.concat([concentration_test_df, row_df], ignore_index=True)
            return concentration_test_df            
        except Exception as e:
            raise Exception(e)

    def min_weighted_average_cash_fixed_coupon(self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type):
        try:
            actual = test_required_col_df[test_required_col_df["Investment Name"] != "Cash"]["Weighted Fixed"].sum()

            if self.is_pass(actual=actual, limit=self.limit_percent, comparison_type=comparison_type):
                result = result = "Pass"
            else:
                result = "Fail"

            row_data = {
                "Concentration Tests": [test_name],
                "Concentration Limit": [self.limit_percent],
                "Actual": [actual],
                "Result": [result],
                "Show on dashboard": [show_on_dashboard],
                "Absolute Limit": [self.min_limit],
                "Percent Limit": [self.limit_percent]
            }
            row_df = pd.DataFrame(row_data)
            concentration_test_df = pd.concat([concentration_test_df, row_df], ignore_index=True)
            return concentration_test_df            
        except Exception as e:
            raise Exception(e)

    def min_weighted_average_cash_floating_coupon(self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type):
        try:
            actual = test_required_col_df[test_required_col_df["Investment Name"] != "Cash"]["Weighted Floating"].sum()

            if self.is_pass(actual=actual, limit=self.limit_percent, comparison_type=comparison_type):
                result = result = "Pass"
            else:
                result = "Fail"

            row_data = {
                "Concentration Tests": [test_name],
                "Concentration Limit": [self.limit_percent],
                "Actual": [actual],
                "Result": [result],
                "Show on dashboard": [show_on_dashboard],
                "Absolute Limit": [self.min_limit],
                "Percent Limit": [self.limit_percent]
            }
            row_df = pd.DataFrame(row_data)
            concentration_test_df = pd.concat([concentration_test_df, row_df], ignore_index=True)
            return concentration_test_df            
        except Exception as e:
            raise Exception(e)

    def max_third_party_finance_companies(self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type):
        try:
            total_bb = test_required_col_df["Borrowing Base"].sum()
            actual = test_required_col_df[test_required_col_df["Third Party Finance Company"] == "Yes"]["Borrowing Base"].sum()
            actual_percent = actual / total_bb

            if self.is_pass(actual=actual_percent, limit=self.limit_percent, comparison_type=comparison_type):
                result = result = "Pass"
            else:
                result = "Fail"

            row_data = {
                "Concentration Tests": [test_name],
                "Concentration Limit": [self.limit_percent],
                "Actual": [actual_percent],
                "Result": [result],
                "Show on dashboard": [show_on_dashboard],
                "Absolute Limit": [self.min_limit],
                "Percent Limit": [self.limit_percent]
            }
            row_df = pd.DataFrame(row_data)
            concentration_test_df = pd.concat([concentration_test_df, row_df], ignore_index=True)
            return concentration_test_df            
        except Exception as e:
            raise Exception(e)

    def max_affiliate_investments(self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type):
        try:
            actual = test_required_col_df[test_required_col_df["Affiliate Investment"] == "Yes"]["Borrowing Base"].sum()

            if self.is_pass(actual=actual, limit=self.limit_percent, comparison_type=comparison_type):
                result = result = "Pass"
            else:
                result = "Fail"

            row_data = {
                "Concentration Tests": [test_name],
                "Concentration Limit": [self.limit_percent],
                "Actual": [actual],
                "Result": [result],
                "Show on dashboard": [show_on_dashboard],
                "Absolute Limit": [self.min_limit],
                "Percent Limit": [self.limit_percent]
            }
            row_df = pd.DataFrame(row_data)
            concentration_test_df = pd.concat([concentration_test_df, row_df], ignore_index=True)
            return concentration_test_df            
        except Exception as e:
            raise Exception(e)

    def max_pik_dip(self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type):
        try:
            total_bb = test_required_col_df["Borrowing Base"].sum()
            test_required_col_df = test_required_col_df[test_required_col_df["Adjusted Type"].isin(["PIK", "DIP"])]
            group_total = test_required_col_df["Borrowing Base"].sum()

            actual = group_total / total_bb

            if self.is_pass(actual=actual, limit=self.limit_percent, comparison_type=comparison_type):
                result = result = "Pass"
            else:
                result = "Fail"
            row_data = {
                "Concentration Tests": [test_name],
                "Concentration Limit": [self.limit_percent],
                "Actual": [actual],
                "Result": [result],
                "Show on dashboard": [show_on_dashboard],
                "Absolute Limit": [self.min_limit],
                "Percent Limit": [self.limit_percent]
            }
            row_df = pd.DataFrame(row_data)
            concentration_test_df = pd.concat([concentration_test_df, row_df], ignore_index=True)
            return concentration_test_df            
        except Exception as e:
            raise Exception(e)

    def max_issuer_concentration_percent_bb(self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type):
        try:
            actual = test_required_col_df["Issuer Concentration"].max()
            if self.is_pass(actual=actual, limit=self.limit_percent, comparison_type=comparison_type):
                result = result = "Pass"
            else:
                result = "Fail"
            row_data = {
                "Concentration Tests": [test_name],
                "Concentration Limit": [self.limit_percent],
                "Actual": [actual],
                "Result": [result],
                "Show on dashboard": [show_on_dashboard],
                "Absolute Limit": [self.min_limit],
                "Percent Limit": [self.limit_percent]
            }
            row_df = pd.DataFrame(row_data)
            concentration_test_df = pd.concat([concentration_test_df, row_df], ignore_index=True)
            return concentration_test_df            
        except Exception as e:
            raise Exception(e)

    def max_weighted_average_maturity_years(self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type):
        try:
            test_required_col_df["Product"] = test_required_col_df["Tenor"] * test_required_col_df["Concentration % Adj. Elig. Amount (excluding cash)"]
            actual = test_required_col_df["Product"].sum()
            test_required_col_df.drop(labels='Product', axis=1, inplace=True)

            if self.is_pass(actual=actual, limit=self.limit_percent, comparison_type=comparison_type):
                result = result = "Pass"
            else:
                result = "Fail"
            row_data = {
                "Concentration Tests": [test_name],
                "Concentration Limit": [self.limit_percent],
                "Actual": [actual],
                "Result": [result],
                "Show on dashboard": [show_on_dashboard],
                "Absolute Limit": [self.min_limit],
                "Percent Limit": [self.limit_percent]
            }
            row_df = pd.DataFrame(row_data)
            concentration_test_df = pd.concat([concentration_test_df, row_df], ignore_index=True)
            return concentration_test_df            
        except Exception as e:
            raise Exception(e)

    def partial_pik_loan(self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type):
        try:
            actual = test_required_col_df.loc[test_required_col_df["Partial PIK Loan"] == "Yes", "Revised Value"].sum()
            concentration_test_df = self.update_conc_test_df(actual=actual, concentration_test_df=concentration_test_df, test_name=test_name, show_on_dashboard=show_on_dashboard, test_required_col_df=test_required_col_df)
            return concentration_test_df
        except Exception as e:
            raise Exception(e)

    def discount_collateral_loans(self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type):
        try:
            actual = test_required_col_df.loc[test_required_col_df["Discount Collateral Loans"] == "Yes", "Revised Value"].sum()
            concentration_test_df = self.update_conc_test_df(actual=actual, concentration_test_df=concentration_test_df, test_name=test_name, show_on_dashboard=show_on_dashboard, test_required_col_df=test_required_col_df)
            return concentration_test_df
        except Exception as e:
            raise Exception(e)

    def credit_improved_loans(self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type):
        try:
            actual = test_required_col_df.loc[test_required_col_df["Credit Improved Loans"] == "Yes", "Revised Value"].sum()
            concentration_test_df = self.update_conc_test_df(actual=actual, concentration_test_df=concentration_test_df, test_name=test_name, show_on_dashboard=show_on_dashboard, test_required_col_df=test_required_col_df)
            return concentration_test_df
        except Exception as e:
            raise Exception(e)

    def warrants_to_purchase_equity_securities(self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type):
        try:
            actual = test_required_col_df.loc[test_required_col_df["Warrants to Purchase Equity"] == "Yes", "Revised Value"].sum()
            concentration_test_df = self.update_conc_test_df(actual=actual, concentration_test_df=concentration_test_df, test_name=test_name, show_on_dashboard=show_on_dashboard, test_required_col_df=test_required_col_df)
            return concentration_test_df
        except Exception as e:
            raise Exception(e)

    def lbo_loan(self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type):
        try:
            actual = test_required_col_df.loc[test_required_col_df["LBO Loan"] == "Yes", "Revised Value"].sum()
            concentration_test_df = self.update_conc_test_df(actual=actual, concentration_test_df=concentration_test_df, test_name=test_name, show_on_dashboard=show_on_dashboard, test_required_col_df=test_required_col_df)
            return concentration_test_df
        except Exception as e:
            raise Exception(e)

    def participation_interests(self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type):
        try:
            actual = test_required_col_df.loc[test_required_col_df["Participation Interests"] == "Yes", "Revised Value"].sum()
            concentration_test_df = self.update_conc_test_df(actual=actual, concentration_test_df=concentration_test_df, test_name=test_name, show_on_dashboard=show_on_dashboard, test_required_col_df=test_required_col_df)
            return concentration_test_df
        except Exception as e:
            raise Exception(e)

    def eligible_covenant_lite_loans(self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type):
        try:
            actual = test_required_col_df.loc[test_required_col_df["Eligible Covenant Lite Loans"] == "Yes", "Revised Value"].sum()
            concentration_test_df = self.update_conc_test_df(actual=actual, concentration_test_df=concentration_test_df, test_name=test_name, show_on_dashboard=show_on_dashboard, test_required_col_df=test_required_col_df)
            return concentration_test_df
        except Exception as e:
            raise Exception(e)

    def top_5_bligors(self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type):
        try:
            actual = test_required_col_df["Revised Value"].sum()
            concentration_test_df = self.update_conc_test_df(actual=actual, concentration_test_df=concentration_test_df, test_name=test_name, show_on_dashboard=show_on_dashboard, test_required_col_df=test_required_col_df)
            return concentration_test_df
        except Exception as e:
            raise Exception(e)

    def ltm_ebitda_lt_15MM(self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type):
        try:
            actual = test_required_col_df["LTM EBITDA < 15,000,000"].sum()
            concentration_test_df = self.update_conc_test_df(actual=actual, concentration_test_df=concentration_test_df, test_name=test_name, show_on_dashboard=show_on_dashboard, test_required_col_df=test_required_col_df)
            return concentration_test_df
        except Exception as e:
            raise Exception(e)

    def ltm_ebitda_gt_5MM_lt_7_5MM(self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type):
        try:
            actual = test_required_col_df["LTM EBITDA >= 5,000,000 but < 7,500,000"].sum()
            concentration_test_df = self.update_conc_test_df(actual=actual, concentration_test_df=concentration_test_df, test_name=test_name, show_on_dashboard=show_on_dashboard, test_required_col_df=test_required_col_df)
            return concentration_test_df
        except Exception as e:
            raise Exception(e)

    def leverage_limitations(self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type):
        try:
            actual = test_required_col_df["Leverage Limitations"].sum()
            concentration_test_df = self.update_conc_test_df(actual=actual, concentration_test_df=concentration_test_df, test_name=test_name, show_on_dashboard=show_on_dashboard, test_required_col_df=test_required_col_df)
            return concentration_test_df
        except Exception as e:
            raise Exception(e)

    def max_industry_concentration_all_other_industries(self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard, comparison_type):
        test_required_col_df = (
            test_required_col_df.groupby("Industry")
            .agg({"Borrowing Base": "sum"})
            .reset_index()
        )
        test_required_col_df = test_required_col_df[test_required_col_df["Industry"] != "Total"]
        BB_sum = test_required_col_df["Borrowing Base"].sum()
        test_required_col_df["Percetage Borrowing Base"] = (
            test_required_col_df["Borrowing Base"] / BB_sum
        )

        # check after demo
        if test_required_col_df.empty:
            return concentration_test_df
        actual = self.get_kth_largest_percent_BB(test_required_col_df, 3)
        rounded_actual = round(actual, 3)
        if self.is_pass(actual=actual, limit=self.limit_percent, comparison_type=comparison_type):
            result = result = "Pass"
        else:
            result = "Fail"

        row_data = {
            "Concentration Tests": [test_name],
            "Concentration Limit": [self.limit_percent],
            "Actual": [rounded_actual],
            "Result": [result],
            "Show on dashboard": [show_on_dashboard]
        }
        row_df = pd.DataFrame(row_data)
        concentration_test_df = pd.concat(
            [concentration_test_df, row_df], ignore_index=True
        )
        return concentration_test_df

    def executeConentrationTest(self):

        # find all applicable tests for given fund
        fund_tests = (
            db.session.query(
                ConcentrationTest.id,
                ConcentrationTest.test_name,
                ConcentrationTest.description,
                ConcentrationTest.mathematical_formula,
                ConcentrationTest.columns,
                ConcentrationTest.comparison_type,
                FundConcentrationTest.limit_percentage,
                FundConcentrationTest.min_limit,
                FundConcentrationTest.show_on_dashboard,
            )
            .join(FundConcentrationTest)
            .join(Fund)
            .filter(Fund.fund_name == self.fund_name)
            .all()
        )

        # create empty dataframe with given names to store result
        concentration_test_df = pd.DataFrame(
            columns=["Concentration Tests", "Concentration Limit", "Actual", "Result"]
        )

        for test in fund_tests:
            print("test.test_name is :- ", test.test_name)
            fund_column_names = self.get_standard_column_names(test.test_name)

            test_data = {}
            for column_key, column_info in fund_column_names.items():
                sheet_name = column_info["Sheet Name"]
                column_name = column_info["Column Name"]
                test_data[column_key] = self.get_dataframe_column(
                    sheet_name, column_name
                )
            self.limit_percent = test.limit_percentage
            self.min_limit = test.min_limit
            test_required_col_df = pd.DataFrame(
                zip_longest(*test_data.values(), fillvalue=None),
                columns=test_data.keys(),
            )

            if test.test_name in self.test_library.keys():
                concentration_test_df = self.test_library[test.test_name](
                    test.test_name, test_required_col_df, concentration_test_df, test.show_on_dashboard, test.comparison_type
                )
            else:
                row_data = {
                    "Concentration Tests": [test.test_name], 
                    "Concentration Limit": [self.limit_percent], 
                    "Actual": [0], 
                    "Result": ["Fail"]
                }
                row_df = pd.DataFrame(row_data)
                pd.concat([concentration_test_df, row_df], ignore_index=True)
                concentration_test_df
                

        return concentration_test_df


class ConcentraionTestFormatter:
    def __init__(self, concentration_test_df):
        self.concentration_test_df = concentration_test_df

    def convert_to_std_table_format(self):
        rows_to_keep = [
            "Min. Eligible Issuers (#)",
            "Number of Issuers",
            "Max. Weighted Average Maturity (Years)",
            "Max. Weighted Average Leverage thru Borrower",
            "Largest Industry",
            "Second Largest Industry",
            "Third Largest Industry",
            "EBITDA < $10MM",
            "Other Obligors",
            "Other Industry",
            "DIP Loans",
            "DDTL and Revolving Loans",
            "Pay Less Frequently than Quarterly",
            "Loans denominated in Approved Foreign Currency",
            "Loans to Obligors domiciled in Approved Foreign Country",
            "Cov-Lite",
            "Tier 3 Obligors (Measured at Inclusion)",
            "Second Lien Loans",
            "First Lien Last Out",
            "Loans with Remaining Maturity > 6 Years",
            "Recurring Revenue Loans",
            "Fixed Rate Loans",
            "Max. Weighted Average Leverage thru Borrower",
            "Partial PIK Loan",
            "Discount Collateral Loans",
            "Credit Improved Loans",
            "Warrants to Purchase Equity Securities",
            "LBO Loan",
            "Participation Interests",
            "Eligible Covenant Lite Loans",
            "Top 5 Obligors",
            "LTM EBITDA < 15,000,000",
            "LTM EBITDA >= 5,000,000 but < 7,500,000",
            "Leverage Limitations",
            "Second Lien and Split Lien"
        ]
        concentration_tests = []
        concentration_limits = []
        actuals = []
        results = []

        conc_test_df_copy = self.concentration_test_df.copy()
        self.concentration_test_df = conc_test_df_copy

        self.concentration_test_df = self.concentration_test_df[self.concentration_test_df["Show on dashboard"] == True] 

        self.concentration_test_df = self.concentration_test_df[["Concentration Tests", "Concentration Limit", "Actual", "Result"]]
        

        self.concentration_test_df[["Concentration Limit", "Actual"]] = self.concentration_test_df[["Concentration Limit", "Actual"]].fillna(0)
        for index, row in self.concentration_test_df.iterrows():
            concentration_tests.append({"data": row["Concentration Tests"]})
            if row["Concentration Tests"] in rows_to_keep:
                concentration_limits.append({"data": numerize.numerize(row["Concentration Limit"]) if row["Concentration Limit"] is not None else "0"})
                actuals.append({"data": numerize.numerize(row["Actual"]) if row["Actual"] is not None else "0"})
            else:
                concentration_limits.append(
                    {"data": "{:,.01f}%".format(row["Concentration Limit"] * 100)}
                )
                actuals.append({"data": "{:,.01f}%".format(row["Actual"] * 100)})
            results.append({"data": row["Result"]})

        concentration_test_data = {
            "Concentration Test": concentration_tests,
            "Concentration Limit": concentration_limits,
            "Actual": actuals,
            "Result": results,
            "columns": [
                {
                    "data": [
                        "Concentration Test",
                        "Concentration Limit",
                        "Actual",
                        "Result",
                    ]
                }
            ],
        }
        return concentration_test_data
