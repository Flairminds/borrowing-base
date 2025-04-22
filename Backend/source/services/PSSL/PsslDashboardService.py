from datetime import datetime
import pickle
from flask import jsonify

from source.services.PSSL import pssl_calculation_initiator

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
        
        