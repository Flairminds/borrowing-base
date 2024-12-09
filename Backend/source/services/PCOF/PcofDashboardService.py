from datetime import datetime, timezone
import pickle
import json
from flask import jsonify
from numerize import numerize
import pandas as pd


from models import db, UserConfig, BaseDataFile, WhatIfAnalysis
from source.services.PCOF.PcofBBCalculator import PcofBBCalculator

from source.services import Standard_File_Formater
from Exceptions.StdFileFormatException import StdFileFormatException
from source.services.PCOF import utility as PCOFUtility

pcofBBCalculator = PcofBBCalculator()


class PcofDashboardService:
    def get_asset_list(self, base_data_file):
        asset_selection_table = {"columns": [], "data": []}

        included_assets = json.loads(base_data_file.included_excluded_assets_map)[
            "included_assets"
        ]
        sheet_df_dict = pickle.loads(base_data_file.file_data)
        df_PL_BB_Build = sheet_df_dict["PL BB Build"]
        selected_columns_list = ["Is Eligible Issuer"]
        user_config = UserConfig.query.filter_by(user_id=base_data_file.user_id).first()
        if not user_config:
            user_config = UserConfig(user_id=base_data_file.user_id)
            user_config.assets_selection_columns = json.dumps(
                {
                    base_data_file.fund_type: [
                        "Investment Name",
                        "Investment Investment Type",
                        "Investment Par",
                        "Investment Industry",
                        "Investment Closing Date",
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
                    "Investment Name",
                    "Investment Investment Type",
                    "Investment Par",
                    "Investment Industry",
                    "Investment Closing Date",
                ]
                user_config.assets_selection_columns = json.dumps(
                    assets_selection_columns
                )
                db.session.add(user_config)
                db.session.commit()
                db.session.refresh(user_config)

        PCOF_assets_selection_columns = json.loads(
            user_config.assets_selection_columns
        )[base_data_file.fund_type]
        for column in PCOF_assets_selection_columns:
            selected_columns_list.append(column)
        selected_column_df_PL_BB_Build = df_PL_BB_Build[selected_columns_list]
        eligible_assets_mask = (
            selected_column_df_PL_BB_Build["Is Eligible Issuer"] == "Yes"
        )
        eligible_assets_df = selected_column_df_PL_BB_Build[eligible_assets_mask]
        eligible_assets_df.fillna("", inplace=True)

        selected_columns_list.remove("Is Eligible Issuer")
        eligible_assets_df = eligible_assets_df[selected_columns_list]
        # find columns containing null values  (fillna('') does not fills NaT values)
        columns_with_nulls = eligible_assets_df.columns[
            eligible_assets_df.isnull().any()
        ]
        # replace all null values with ''
        for col in columns_with_nulls:
            eligible_assets_df[col] = eligible_assets_df[col].astype(str).fillna("")

        asset_selection_table["columns"] = [
            {"label": column, "key": column.replace(" ", "_")}
            for column in eligible_assets_df.columns
        ]

        for index, row in eligible_assets_df.iterrows():
            row_data = {}
            row_data["isIncluded"] = False
            for col, value in row.items():
                if col == "Investment Name" and value in included_assets:
                    row_data["isIncluded"] = True
                if isinstance(value, (int, float)):
                    if col in [
                        "Rates Current LIBOR/Floor",
                        "Rates Fixed Coupon",
                        "Rates Floating Cash Spread",
                        "Leverage LTV Thru PCOF IV",
                    ]:
                        row_data[col.replace(" ", "_")] = "{:,.01f}%".format(
                            value * 100
                        )
                    elif col in [
                        "Financials LTM Revenue ($MMs)",
                        "Financials LTM EBITDA ($MMs)",
                        "Leverage Revolver Commitment",
                        "Leverage Total Enterprise Value",
                        "Leverage Total Leverage",
                        "Leverage PCOF IV Leverage",
                        "Leverage Attachment Point",
                    ]:
                        row_data[col.replace(" ", "_")] = numerize.numerize(value, 2)
                    else:
                        row_data[col.replace(" ", "_")] = "$" + numerize.numerize(
                            value, 2
                        )
                elif isinstance(value, datetime):
                    row_data[col.replace(" ", "_")] = value.strftime("%Y-%m-%d")
                else:
                    row_data[col.replace(" ", "_")] = value
            asset_selection_table["data"].append(row_data)
            asset_selection_table["identifier"] = "Investment_Name"
        return jsonify(asset_selection_table)

    def number_formatting_for_availablity(self, df_Availability_Borrower):
        df_Availability_Borrower.fillna(0, inplace=True)

        def convert_to_numeric(value):
            if isinstance(value, str):
                # Remove any non-numeric characters before converting to float
                value = float(value.replace(",", "").replace("$", "").replace("%", ""))
            return value

        df_Availability_Borrower.at[1, "B"] = str(
            pd.to_datetime(df_Availability_Borrower.at[1, "B"]).date()
        )
        df_Availability_Borrower.at[2, "B"] = str(
            pd.to_datetime(df_Availability_Borrower.at[2, "B"]).date()
        )

        for index in [4, 5, 6, 7, 8, 9, 12, 13, 16, 17, 18, 19, 22]:
            df_Availability_Borrower.at[index, "B"] = "$" + numerize.numerize(
                convert_to_numeric(df_Availability_Borrower.at[index, "B"])
            )

        for index in [10, 14, 15, 20, 21]:
            df_Availability_Borrower.at[index, "B"] = "{:,.01f}%".format(
                convert_to_numeric(df_Availability_Borrower.at[index, "B"]) * 100
            )

        return df_Availability_Borrower

    def convert_to_card_table(self, df_Availability_Borrower, search_values):
        matched_rows = []
        for value in search_values:
            row_data = df_Availability_Borrower[df_Availability_Borrower["A"] == value]
            if not row_data.empty:
                row_values = row_data.values.tolist()
                matched_rows.extend(row_values)
        card_table = {
            "columns": [{"data": ["Term", "Value"]}],
            "Term": [{"data": matched_row[0]} for matched_row in matched_rows],
            "Value": [{"data": matched_row[1]} for matched_row in matched_rows],
        }
        return card_table

    def get_obligator_net_capital_table(self, obligator_copy):
        obligations = obligator_copy["Principal Obligations"].tolist()
        currency = obligator_copy["Currency"].tolist()
        amount = obligator_copy["Amount"].tolist()
        spotrate = obligator_copy["Spot Rate"].tolist()
        dollarequivalent = obligator_copy["Dollar Equivalent"].tolist()
        obligators_net_capital = {
            "columns": [
                {
                    "data": [
                        "Obligation",
                        "Currency",
                        "Amount",
                        "Spot rate",
                        "Dollar equivalent",
                    ]
                }
            ],
            "Obligation": [{"data": val} for val in obligations],
            "Currency": [{"data": val} for val in currency],
            "Amount": [
                {"data": "$" + numerize.numerize(round(val, 2))} for val in amount
            ],
            "Spot rate": [
                {"data": "{:.2f}%".format(round(val, 2))} for val in spotrate
            ],
            "Dollar equivalent": [
                {"data": "$" + numerize.numerize(round(val, 2))}
                for val in dollarequivalent
            ],
        }
        return obligators_net_capital

    def get_total_bb_table(self, df_Availability_Borrower):
        search_values = ["Total Borrowing Base"]
        return self.convert_to_card_table(df_Availability_Borrower, search_values)

    def get_leverage_bb_table(self, df_Availability_Borrower):
        search_values = [
            "Portfolio > 8 Eligible Issuers?",
            "FMV of Portfolio",
            "Effective Advance Rate on FMV of Portfolio",
            "Portfolio Leverage Borrowing Base (as calculated)",
            "Maximum Advance Rate on PL Borrowing Base",
            "Portfolio Leverage Borrowing Base",
        ]
        return self.convert_to_card_table(df_Availability_Borrower, search_values)

    def get_subscription_bb_table(self, df_Availability_Borrower):
        search_values = [
            "Revolving Closing Date",
            "Date of determination:",
            "Months since Revolving Closing Date",
            "Commitment Period (3 years from Final Closing Date, as defined in LPA)",
            "Uncalled Capital Commitments",
            "Subscription Borrowing Base",
            "Effective Advance Rate on Total Uncalled Capital",
            "Months since Revolving Closing Date",
        ]
        return self.convert_to_card_table(df_Availability_Borrower, search_values)

    def get_availability_card_table(self, df_Availability_Borrower):
        search_values = [
            "Subscription Borrowing Base",
            "Portfolio Leverage Borrowing Base",
            "Total Borrowing Base",
            "(b) Facility Size",
            "Lesser of (a) and (b)",
            "Outstandings",
            "Net Debt Availbility",
            "Gross BB Utilization",
            "Facility Utilization ",
        ]
        return self.convert_to_card_table(df_Availability_Borrower, search_values)

    def get_card_overview(self, base_data_file, card_name):
        intermediate_calculation = pickle.loads(base_data_file.intermediate_calculation)

        df_Availability_Borrower = intermediate_calculation["df_Availability_Borrower"]
        df_principle_obligations = intermediate_calculation["df_principle_obligations"]

        obligator_copy = df_principle_obligations.copy().fillna(0)
        df_Availability_Borrower = df_Availability_Borrower.copy()
        df_Availability_Borrower = self.number_formatting_for_availablity(
            df_Availability_Borrower
        )

        if card_name == "Obligors net capital":
            card_table = self.get_obligator_net_capital_table(obligator_copy)

        if card_name == "Total BB":
            card_table = self.get_total_bb_table(df_Availability_Borrower)

        if card_name == "Leverage BB":
            card_table = self.get_leverage_bb_table(df_Availability_Borrower)

        if card_name == "Subscription BB":
            card_table = self.get_subscription_bb_table(df_Availability_Borrower)

        if card_name == "Availability":
            card_table = self.get_availability_card_table(df_Availability_Borrower)

        return jsonify(card_table)

    def get_trend_graph(self, base_data_file_sorted, closing_date):
        calc_df_Availability_Borrower = [
            aval.intermediate_calculation for aval in base_data_file_sorted
        ]

        # Initialize lists for storing values
        subscription_borrowing_base_values = []
        portfolio_leverage_borrowing_base_values = []
        total_borrowing_base_values = []

        rows_to_extract = [
            "Subscription Borrowing Base",
            "Portfolio Leverage Borrowing Base",
            "Total Borrowing Base",
        ]

        for pickle_file in calc_df_Availability_Borrower:
            data = pickle.loads(pickle_file)
            if "df_Availability_Borrower" in data:
                df = data["df_Availability_Borrower"]
                row_values = df.loc[df["A"].isin(rows_to_extract), "B"].tolist()
                subscription_borrowing_base_values.append(row_values[0])
                portfolio_leverage_borrowing_base_values.append(row_values[1])
                total_borrowing_base_values.append(row_values[2])

        trend_graph_data = [
            {
                "date": closing_date,
                "Tot BB": total_bb,
                "Sub BB": subscription_bb,
                "Lev BB": leverage_bb,
            }
            for closing_date, subscription_bb, leverage_bb, total_bb in zip(
                closing_date,
                subscription_borrowing_base_values,
                portfolio_leverage_borrowing_base_values,
                total_borrowing_base_values,
            )
        ]
        trend_graph_response = {
            "trend_graph_data": trend_graph_data,
            "x_axis": ["Tot BB", "Sub BB", "Lev BB"],
        }
        return jsonify(trend_graph_response), 200

    def calculate_bb(self, base_data_file, selected_assets, user_id):
        return (
            jsonify(
                pcofBBCalculator.get_bb_calculation(
                    base_data_file, selected_assets, user_id
                )
            ),
            200,
        )
    
    def pcof_validate_file(self, excel_file, fund_type):
        try:
            error_map, xl_sheet_df_map = Standard_File_Formater.validate_file(
                    excel_file, fund_type
                )
            error_map["Row Modifications"] = []
        except Exception as e:
            error_map = {"Error": f"An unexpected error occurred: {str(e)}"}

        # if Cash asset is not in dataframe
        if "PL BB Build" in xl_sheet_df_map.keys():
            df_PL_BB_Build = xl_sheet_df_map["PL BB Build"]

            if "Cash" not in df_PL_BB_Build["Investment Name"].tolist():
                error_map["Row Modifications"].append(
                    "<b>Cash</b> asset is not present in <b>PL BB Build</b> sheet"
                )

        if (
            (error_map["Sheet Modifications"])
            or (error_map["Column Modifications"])
            or (error_map["Data Format Modifications"])
            or error_map["Row Modifications"]
        ):
            raise StdFileFormatException(error_map)
        
        return xl_sheet_df_map
    
    def pcof_included_excluded_assets(self, xl_sheet_df_map):
        included_excluded_assets_map = (
            PCOFUtility.get_included_excluded_assets_map_json(
                xl_sheet_df_map["PL BB Build"]
            )
        )
        return included_excluded_assets_map
