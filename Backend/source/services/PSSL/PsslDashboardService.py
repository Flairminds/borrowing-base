from datetime import datetime
import pickle
from flask import jsonify
from numerize import numerize
import re
import pandas as pd

from source.services.PSSL import pssl_calculation_initiator
from models import BaseDataOtherInfo
from source.utility.Util import currency_to_float_to_numerize_to_currency

class PsslDashboardService:
    def get_bb_calculation(self, base_data_file, selected_assets, user_id):
        pssl_calculation_initiator.get_bb_calculation(base_data_file, selected_assets, user_id)

    def convert_to_card_table(self, availability_df, search_values):
        matched_rows = []
        for value in search_values:
            row_data = availability_df[availability_df["Terms"] == value]
            if not row_data.empty:
                row_values = row_data.values.tolist()
                matched_rows.extend(row_values)
        card_table = {
            "columns": [{"data": ["Term", "Value"]}],
            "Term": [{"data": row[0]} for row in matched_rows],
            "Value": [{"data": currency_to_float_to_numerize_to_currency(row[1])} for row in matched_rows],
        }
        return card_table

    def get_trend_graph(self, base_data_file_sorted, closing_date):
        pssl_trend_graph_response = {
            "trend_graph_data": [],
            "x_axis": ["Borrowing Base"],
        }

        for base_data_file in base_data_file_sorted:
            intermediate_calculation = pickle.loads(base_data_file.intermediate_calculation)
            portfolio_df = intermediate_calculation["Portfolio"]

            total_BB = portfolio_df["Adjusted Borrowing Value"].sum()
            
            result_dict = {"Borrowing Base": total_BB}

            result_dict["date"] = datetime.strftime(
                base_data_file.closing_date, "%Y-%m-%d"
            )
            pssl_trend_graph_response["trend_graph_data"].append(result_dict)

        # pflt_trnd_graph_response["x-axis"] = selected_rows_BB_df.columns.tolist()
        return jsonify(pssl_trend_graph_response), 200
    
    def get_adjusted_borrowing_value(self, availability_df):

        search_values = [
            "Adjusted Borrowing Value"
        ]

        return self.convert_to_card_table(availability_df, search_values)
    
    def get_availibilty(self):
        selected_keys = [
            "facility_amount",
            "current_advances_outstanding",
            "cash_on_deposit_in_principal_collections_account"
        ]
        latest_data = (
            BaseDataOtherInfo.query.filter(
                BaseDataOtherInfo.fund_type == "PSSL",
                BaseDataOtherInfo.extraction_info_id == 113
            ).first()
        )

        data_for_card = latest_data.other_info_list
    
        card_table = {
            "Term": [],
            "Value": [],
            "columns": [
                {
                    "data": ["Term", "Value"]
                }
            ]
        }

        for key in selected_keys:
            value = data_for_card.get(key)
            card_table["Term"].append({"data": key.replace('_', ' ').title()})
            card_table["Value"].append({"data": numerize.numerize(value)})

        return card_table
   
    def get_current_advances_outstanding_value(self, availability_df):
        curr_advance_data = availability_df.loc[availability_df["Terms"] == "Current Advances Outstanding", "Values"].values[0]
        curr_advance_data_without_dollar = int(re.sub(r"[^\d.]", "", curr_advance_data))
        card_table = {
            "Term": [
                {
                    "data": "Current Advances Outstanding"
                }
            ],
            "Value": [
                {
                    "data": numerize.numerize(curr_advance_data_without_dollar)
                }
            ],
            "columns": [
                {
                    "data": [
                        "Term",
                        "Value"
                    ]
                }
            ]
        }
        return card_table
    
    def get_pro_forma_advances_outstanding_value(self, availability_df):
        search_values = [
            "Current Advances Outstanding",
            "Advances Repaid",
            "Advances Requested"
        ]
        return self.convert_to_card_table(availability_df, search_values)
    
    def get_borrowing_value(self, availability_df):
        search_values = [
            "Adjusted Borrowing Value",
            "Excess Concentration Amount",
            "Approved Foreign Currency Reserve"
        ]
        return self.convert_to_card_table(availability_df, search_values)
    
    
    def get_card_overview(self, base_data_file, card_name, what_if_analysis):
        if what_if_analysis:
            intermediate_calculation = pickle.loads(what_if_analysis.intermediate_calculation)
        else:
            intermediate_calculation = pickle.loads(base_data_file.intermediate_calculation)

        portfolio_df = intermediate_calculation["Portfolio"]     
        availability_df = intermediate_calculation["Availability"]     
        facility_df = intermediate_calculation["Availability"]     
 
        # if card_name == "Adjusted Borrowing Value":
        #     card_table = self.get_adjusted_borrowing_value(availability_df)
        # if card_name == "Availability":
        #     card_table = self.get_availibilty()
        
        # if card_name == "Current Advances Outstanding":
        #     card_table = self.get_current_advances_outstanding_value(availability_df)

        if card_name == "Pro Forma Advances Outstanding":
            card_table = self.get_pro_forma_advances_outstanding_value(availability_df)

        if card_name == "Borrowing Base":
            card_table = self.get_borrowing_value(availability_df)
        

        return jsonify(card_table), 200
        
        