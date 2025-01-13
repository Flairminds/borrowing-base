from datetime import datetime, timezone
import json
import pickle
from flask import jsonify
import pandas as pd
from numerize import numerize

from models import db, UserConfig, WhatIfAnalysis
from source.services.PFLT.PfltBBCalculator import PfltBBCalculator

from source.services import Standard_File_Formater
from Exceptions.StdFileFormatException import StdFileFormatException


pfltBBCalculator = PfltBBCalculator()


class PfltDashboardService:
    def get_asset_list(self, base_data_file):
        asset_selection_table = {"columns": [], "data": []}

        included_assets = json.loads(base_data_file.included_excluded_assets_map)[
            "included_assets"
        ]
        user_config = UserConfig.query.filter_by(user_id=base_data_file.user_id).first()
        if not user_config:
            user_config = UserConfig(user_id=base_data_file.user_id)
            user_config.assets_selection_columns = json.dumps(
                {
                    base_data_file.fund_type: [
                        "Security Name",
                        "Obligor Name",
                        "Loan Type (Term / Delayed Draw / Revolver)",
                        "Lien Type (First Lien / Split First Lien / Split Lien / Second Lien / Tier 1 Split Lien / Tier 2 Split Lien)",
                        "Obligor Industry",
                    ]
                }
            )
            db.session.add(user_config)
            db.session.commit()
            db.session.refresh(user_config)
        else:
            assets_selection_columns = json.loads(user_config.assets_selection_columns)
            if not assets_selection_columns.get(base_data_file.fund_type):
                assets_selection_columns[base_data_file.fund_type] = [
                    "Security Name",
                    "Obligor Name",
                    "Loan Type (Term / Delayed Draw / Revolver)",
                    "Lien Type (First Lien / Split First Lien / Split Lien / Second Lien / Tier 1 Split Lien / Tier 2 Split Lien)",
                    "Obligor Industry",
                ]
                user_config.assets_selection_columns = json.dumps(
                    assets_selection_columns
                )
                db.session.add(user_config)
                db.session.commit()
                db.session.refresh(user_config)

        PFLT_assets_selection_columns = json.loads(
            user_config.assets_selection_columns
        )[base_data_file.fund_type]
        selected_columns_list = []
        for column in PFLT_assets_selection_columns:
            selected_columns_list.append(column)

        xl_df_map = pickle.loads(base_data_file.file_data)
        loan_list_df = xl_df_map["Loan List"]

        selected_column_loan_list_df = loan_list_df[selected_columns_list]
        selected_column_loan_list_df.fillna("")
        asset_selection_table["columns"] = [
            {"label": column, "key": column.replace(" ", "_")}
            for column in selected_column_loan_list_df.columns
        ]

        for index, row in selected_column_loan_list_df.iterrows():
            row_data = {}
            row_data["isIncluded"] = False
            for col, value in row.items():
                if col == "Security Name" and value in included_assets:
                    row_data["isIncluded"] = True
                if selected_column_loan_list_df.dtypes[col] in ["datetime64[ns]"]:
                    if not pd.isna(value):
                        # row_data[col.replace(" ", "_")] = value.strftime("%Y-%m-%d")
                        value = value.strftime("%Y-%m-%d")
                    else:
                        value = ""
                if col == "Purchase Price":
                    value = str(round(value * 100, 2)) + "%"
                row_data[col.replace(" ", "_")] = value
            asset_selection_table["data"].append(row_data)
            asset_selection_table["identifier"] = "Security_Name"
        return asset_selection_table

    def get_borrowing_base_table(self, borrowing_base_df):
        borrowing_base_card_rows = [
            "Aggregate Collateral Balance (without duplication) sum of (i)-(vi)",
            "(i) Aggregate Principal Balance of all Collateral Loans (other than Defaulted, Restructured, Haircut Ineligible, and Discount)",
            "(ii) Defaulted Collateral Loan Balance",
            "(iii) The aggregate purchase price of all Discount Loans that are Eligible Collateral Loans and not Defaulted, Haircut or Restructured",
            "(iv) The aggregate Unfunded Commitments of all Delayed Drawdown and Revolvers that are Eligible Loans",
            "(v) The Credit Improved Loan Balance",
            "(vi) The Haircut Collateral Loan Balance",
            "Excess Concentration Amount",
        ]
        borrowing_base_sheet_df = borrowing_base_df[
            borrowing_base_df[borrowing_base_df.columns[0]].isin(
                borrowing_base_card_rows
            )
        ]

        card_table = {
            column: [
                {
                    "data": (
                        "$" + numerize.numerize(cell)
                        if type(cell) == int or type(cell) == float
                        else cell
                    )
                }
                for cell in borrowing_base_sheet_df[column]
            ]
            for column in borrowing_base_sheet_df.columns.tolist()
        }
        card_table["columns"] = [{"data": borrowing_base_sheet_df.columns.tolist()}]
        return card_table

    def get_advance_outstandings_table(self, borrowing_base_df):
        borrowing_base_card_rows = [
            "Advances Outstanding at beginning of the Interest Accrual Period",
            "Advances/(Repayments) during the period through and including & TEXT",
            "Advances Outstanding as of & TEXT",
        ]
        borrowing_base_sheet_df = borrowing_base_df[
            borrowing_base_df[borrowing_base_df.columns[0]].isin(
                borrowing_base_card_rows
            )
        ]

        card_table = {
            column: [
                {
                    "data": (
                        "$" + numerize.numerize(cell)
                        if type(cell) == int or type(cell) == float
                        else cell
                    )
                }
                for cell in borrowing_base_sheet_df[column]
            ]
            for column in borrowing_base_sheet_df.columns.tolist()
        }
        card_table["columns"] = [{"data": borrowing_base_sheet_df.columns.tolist()}]
        return card_table

    def get_availability_table(self, borrowing_base_df):
        borrowing_base_card_rows = [
            "(A) Maximum Available Amount",
            "(B) Advances",
            "AVAILABILITY - (a) minus (b)",
        ]
        borrowing_base_sheet_df = borrowing_base_df[
            borrowing_base_df[borrowing_base_df.columns[0]].isin(
                borrowing_base_card_rows
            )
        ]

        card_table = {
            column: [
                {
                    "data": (
                        "$" + numerize.numerize(cell)
                        if type(cell) == int or type(cell) == float
                        else cell
                    )
                }
                for cell in borrowing_base_sheet_df[column]
            ]
            for column in borrowing_base_sheet_df.columns.tolist()
        }
        card_table["columns"] = [{"data": borrowing_base_sheet_df.columns.tolist()}]
        return card_table

    def get_total_credit_facility_balance(self, Credit_Balance_Projection_df):
        card_table = {
            column: [
                {
                    "data": (
                        "$" + numerize.numerize(cell)
                        if type(cell) == int or type(cell) == float
                        else cell
                    )
                }
                for cell in Credit_Balance_Projection_df[column]
            ]
            for column in Credit_Balance_Projection_df.columns.tolist()
        }
        card_table["columns"] = [
            {"data": Credit_Balance_Projection_df.columns.tolist()}
        ]
        return card_table

    def get_maximum_available_amount_table(self, borrowing_base_df):
        borrowing_base_card_rows = [
            "Facility Amount, less",
            "(A) Revolving Exposure, plus",
            "(A) Amount on deposit in the Revolving Reserve Account",
            "(A) Total of above 3",
            "(x) Borrowing Base, multipled by",
            "(y) Weighted Average Advance Rate, minus",
            "Foreign Currency Variability Reserve, minus",
            "(B) Revolving Exposure, plus",
            "(B) Cash on deposit in Principal Collection Subaccount",
            "(B) Amount on deposit in the Revolving Reserve Account",
            "(B) Total Of Above 5",
            "Aggregate Collateral Balance, minus",
            "Minimum Equity Amount, plus",
            "(C) Cash on deposit in Principal Collection Subaccount",
            "(C) Total of above 3",
        ]
        borrowing_base_sheet_df = borrowing_base_df[
            borrowing_base_df[borrowing_base_df.columns[0]].isin(
                borrowing_base_card_rows
            )
        ]

        card_table = {
            column: [
                {
                    "data": (
                        "$" + numerize.numerize(cell)
                        if type(cell) == int or type(cell) == float
                        else cell
                    )
                }
                for cell in borrowing_base_sheet_df[column]
            ]
            for column in borrowing_base_sheet_df.columns.tolist()
        }
        card_table["columns"] = [{"data": borrowing_base_sheet_df.columns.tolist()}]
        return card_table

    def get_card_overview(self, base_data_file, card_name):
        intermediate_calculation = pickle.loads(base_data_file.intermediate_calculation)

        borrowing_base_df = intermediate_calculation["Borrowing Base"]
        Credit_Balance_Projection_df = intermediate_calculation[
            "Credit Balance Projection"
        ]

        if card_name == "Borrowing Base":
            card_table = self.get_borrowing_base_table(borrowing_base_df)

        if card_name == "Maximum Available Amount":
            card_table = self.get_maximum_available_amount_table(borrowing_base_df)

        if card_name == "Advance Outstandings":
            card_table = self.get_advance_outstandings_table(borrowing_base_df)

        if card_name == "Availability":
            card_table = self.get_availability_table(borrowing_base_df)

        if card_name == "Total Credit Facility Balance":
            card_table = self.get_total_credit_facility_balance(
                Credit_Balance_Projection_df
            )

        return jsonify(card_table), 200

    def get_trend_graph(self, base_data_file_sorted, closing_date):
        pflt_trnd_graph_response = {
            "trend_graph_data": [],
            "x_axis": ["Borrowing Base", "Maximum Available Amount", "Availability"],
        }
        rows_to_extract = [
            "BORROWING BASE - (A) minus (B) minus (A)(iv)",
            "MAXIMUM AVAILABLE AMOUNT - Least of (A), (B) and (C)",
            "AVAILABILITY - (a) minus (b)",
        ]

        for base_data_file in base_data_file_sorted:
            intermediate_calculation = pickle.loads(
                base_data_file.intermediate_calculation
            )
            borrowing_base_df = intermediate_calculation["Borrowing Base"]
            selected_rows_BB_df = borrowing_base_df[
                borrowing_base_df["Terms"].isin(rows_to_extract)
            ]
            rename_dict = {
                "BORROWING BASE - (A) minus (B) minus (A)(iv)": "Borrowing Base",
                "MAXIMUM AVAILABLE AMOUNT - Least of (A), (B) and (C)": "Maximum Available Amount",
                "AVAILABILITY - (a) minus (b)": "Availability",
            }
            selected_rows_BB_df["Terms"] = selected_rows_BB_df["Terms"].replace(
                rename_dict
            )
            result_dict = dict(
                zip(selected_rows_BB_df.Terms, selected_rows_BB_df.Values)
            )

            result_dict["date"] = datetime.strftime(
                base_data_file.closing_date, "%Y-%m-%d"
            )
            pflt_trnd_graph_response["trend_graph_data"].append(result_dict)

        # pflt_trnd_graph_response["x-axis"] = selected_rows_BB_df.columns.tolist()
        return jsonify(pflt_trnd_graph_response), 200

    def calculate_bb(self, base_data_file, selected_assets, user_id):
        return (
            jsonify(
                pfltBBCalculator.get_bb_calculation(
                    base_data_file, selected_assets, user_id
                )
            ),
            200,
        )
    
    def validate_standard_file_format(self, excel_file, std_file_format):
        try:
            error_map, xl_sheet_df_map = Standard_File_Formater.validate_file(
                excel_file, std_file_format
            )
            error_map["Row Modifications"] = []
        except Exception as e:
            error_map = {"Error": f"An unexpected error occurred: {str(e)}"}

        if (
            (error_map["Sheet Modifications"])
            or (error_map["Column Modifications"])
            or (error_map["Data Format Modifications"])
            or error_map["Row Modifications"]
        ):
            raise StdFileFormatException(error_map)
        
        return xl_sheet_df_map
        
    def pflt_included_excluded_assets(self, xl_sheet_df_map):
        included_excluded_assets_map = {
            "included_assets": xl_sheet_df_map["Loan List"][
                "Security Name"
            ].tolist(),
            "excluded_assets": [],
        }

        return included_excluded_assets_map