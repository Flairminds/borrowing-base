from datetime import datetime
import pickle
from flask import jsonify
from numerize import numerize
import re

from source.services.PSSL import pssl_calculation_initiator
from models import BaseDataOtherInfo

class PsslDashboardService:
    def get_bb_calculation(self, base_data_file, selected_assets, user_id):
        pssl_calculation_initiator.get_bb_calculation(base_data_file, selected_assets, user_id)

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
    
    def get_borrowing_base_value(self, portfolio_df):
        total_bb = portfolio_df["Adjusted Borrowing Value"].sum()

        card_table = {
            "Term": [
                {
                    "data": "Borrowing Base"
                }
            ],
            "Value": [
                {
                    "data": numerize.numerize(total_bb)
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
    
    def get_card_overview(self, base_data_file, card_name, what_if_analysis):
        if what_if_analysis:
            intermediate_calculation = pickle.loads(what_if_analysis.intermediate_calculation)
        else:
            intermediate_calculation = pickle.loads(base_data_file.intermediate_calculation)

        portfolio_df = intermediate_calculation["Portfolio"]     
        availability_df = intermediate_calculation["Availability"]     
        facility_df = intermediate_calculation["Availability"]     
 
        if card_name == "Borrowing Base":
            card_table = PsslDashboardService.get_borrowing_base_value(self, portfolio_df)
        if card_name == "Availability":
            card_table = PsslDashboardService.get_availibilty(self)
        
        if card_name == "Current Advances Outstanding":
            card_table = PsslDashboardService.get_current_advances_outstanding_value(self, availability_df)
        

        return jsonify(card_table), 200
        
        