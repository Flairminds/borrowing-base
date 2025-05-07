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

from models import db, Fund, ConcentrationTest, FundConcentrationTest, BaseDataFile
import pickle
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
        }

    def get_kth_largest_percent_BB(self, test_required_col_df, k):
        percent_BB_list = test_required_col_df["Percetage Borrowing Base"].tolist()
        percent_BB_list.sort(reverse=True)
        return percent_BB_list[k - 1]

    def get_standard_column_names(self, test_name):
        # get standard column for the fund
        test_mapping = self.fund_std_col_map.get(test_name, {})
        fund_columns = test_mapping.get(self.fund_name, {})
        return fund_columns

    def get_dataframe_column(self, sheet_name, column_name):
        dataframe = self.calculated_df_map.get(sheet_name)
        return dataframe[column_name].tolist()

    def execute_Max_Industry_Concentration_percent_BB(
        self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard
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
        self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard
    ):
        actual = test_required_col_df["Eligible Issuer"].max()
        if actual >= self.limit_percent:
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

    def execute_number_of_issuers(
        self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard
    ):
        actual = test_required_col_df["Eligible Issuer"].max()
        if actual == self.limit_percent:
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

    def execute_Second_Lien_and_Split_Lien(
        self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard
    ):
        total_borrowing_base = test_required_col_df.loc[
            test_required_col_df["Terms"]
            == "BORROWING BASE - (A) minus (B) minus (A)(iv)",
            "Values",
        ].iloc[0]

        actual = (
            test_required_col_df["Second Lien and Split Lien"].sum()
            / total_borrowing_base
        )
        if actual > self.limit_percent:
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

    def execute_Second_Lien(
        self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard
    ):
        total_borrowing_base = test_required_col_df.loc[
            test_required_col_df["Terms"]
            == "BORROWING BASE - (A) minus (B) minus (A)(iv)",
            "Values",
        ].iloc[0]

        actual = test_required_col_df["Second Lien"].sum() / total_borrowing_base
        if actual > self.limit_percent:
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

    def execute_DIP_Collateral_Loans(
        self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard
    ):
        total_borrowing_base = test_required_col_df.loc[
            test_required_col_df["Terms"]
            == "BORROWING BASE - (A) minus (B) minus (A)(iv)",
            "Values",
        ].iloc[0]

        actual = (
            test_required_col_df["DIP Collateral Loans"].sum() / total_borrowing_base
        )
        if actual > self.limit_percent:
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
        self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard
    ):
        ltv_transaction_grouped_df = (
            test_required_col_df.groupby("LTV Transaction")
            .agg({"Borrowing Base": "sum"})
            .reset_index()
        )
        yes_sum = 0
        for index, row in ltv_transaction_grouped_df.iterrows():
            if row["LTV Transaction"] == "Yes":
                yes_sum = row["Borrowing Base"]

        actual = yes_sum / ltv_transaction_grouped_df["Borrowing Base"].sum()
        rounded_actual = round(actual, 3)
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

    def execute_Max_Foreign_Eligible_Portfolio_Investments(
        self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard
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

        if actual <= self.limit_percent:
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

    def execute_Max_Warehouse_Assets(
        self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard
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

    def Max_Contribution_to_BB_with_Maturity_greater_than_8_years(
        self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard
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

    def Max_Industry_Concentration_Largest_Industry_percent_BB(
        self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard
    ):
        test_required_col_df = (
            test_required_col_df.groupby("Industry")
            .agg({"Borrowing Base": "sum"})
            .reset_index()
        )
        BB_sum = test_required_col_df["Borrowing Base"].sum()
        test_required_col_df["Percetage Borrowing Base"] = (
            test_required_col_df["Borrowing Base"] / BB_sum
        )

        # check after demo
        if test_required_col_df.empty:
            return concentration_test_df
        actual = self.get_kth_largest_percent_BB(test_required_col_df, 1)
        rounded_actual = round(actual, 3)
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

    def Max_Industry_Concentration_2nd_Largest_Industry_percent_BB(
        self, test_name, test_required_col_df, concentration_test_df, show_on_dashboard
    ):
        test_required_col_df = (
            test_required_col_df.groupby("Industry")
            .agg({"Borrowing Base": "sum"})
            .reset_index()
        )
        BB_sum = test_required_col_df["Borrowing Base"].sum()
        test_required_col_df["Percetage Borrowing Base"] = (
            test_required_col_df["Borrowing Base"] / BB_sum
        )

        # check after demo
        if test_required_col_df.empty:
            return concentration_test_df

        actual = self.get_kth_largest_percent_BB(test_required_col_df, 2)
        rounded_actual = round(actual, 3)
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

    def executeConentrationTest(self):

        # find all applicable tests for given fund
        fund_tests = (
            db.session.query(
                ConcentrationTest.id,
                ConcentrationTest.test_name,
                ConcentrationTest.description,
                ConcentrationTest.mathematical_formula,
                ConcentrationTest.columns,
                FundConcentrationTest.limit_percentage,
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
            # if test.show_on_dashboard:
                fund_column_names = self.get_standard_column_names(test.test_name)

                test_data = {}
                for column_key, column_info in fund_column_names.items():
                    sheet_name = column_info["Sheet Name"]
                    column_name = column_info["Column Name"]
                    test_data[column_key] = self.get_dataframe_column(
                        sheet_name, column_name
                    )
                self.limit_percent = test.limit_percentage
                test_required_col_df = pd.DataFrame(
                    zip_longest(*test_data.values(), fillvalue=None),
                    columns=test_data.keys(),
                )

                concentration_test_df = self.test_library[test.test_name](
                    test.test_name, test_required_col_df, concentration_test_df, test.show_on_dashboard
                )

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
            "Largest Industry"
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
