from datetime import datetime
import pickle


def generate_pflt_trendgraph(base_data_file_sorted):
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
        intermediate_calculation = pickle.loads(base_data_file.intermediate_calculation)
        borrowing_base_df = intermediate_calculation["Borrowing Base"]
        selected_rows_BB_df = borrowing_base_df[
            borrowing_base_df["Terms"].isin(rows_to_extract)
        ]
        rename_dict = {
            "BORROWING BASE - (A) minus (B) minus (A)(iv)": "Borrowing Base",
            "MAXIMUM AVAILABLE AMOUNT - Least of (A), (B) and (C)": "Maximum Available Amount",
            "AVAILABILITY - (a) minus (b)": "Availability",
        }
        selected_rows_BB_df["Terms"] = selected_rows_BB_df["Terms"].replace(rename_dict)
        result_dict = dict(zip(selected_rows_BB_df.Terms, selected_rows_BB_df.Values))

        result_dict["date"] = datetime.strftime(base_data_file.closing_date, "%Y-%m-%d")
        pflt_trnd_graph_response["trend_graph_data"].append(result_dict)

    # pflt_trnd_graph_response["x-axis"] = selected_rows_BB_df.columns.tolist()
    return pflt_trnd_graph_response
