import pandas as pd

percentage_map = {
    "Loan List": {
        "Purchase Value": {"is_conditional": False},
        "Market Value": {"is_conditional": False},
        "Debt to Capitalization Ratio": {"is_conditional": False},
        "Coupon incl. PIK and PIK'able (if Fixed)": {"is_conditional": False},
        "Floor": {"is_conditional": False},
        "Spread incl. PIK and PIK'able": {"is_conditional": False},
        "Base Rate": {"is_conditional": False},
        "For Revolvers/Delayed Draw, commitment or other unused fee": {"is_conditional": False},
        "PIK / PIK'able For Floating Rate Loans": {"is_conditional": False},
        "PIK / PIK'able For Fixed Rate Loans": {"is_conditional": False},
    },
}
    
class PFLT_WIA:
    @staticmethod
    def convert_to_table(df, sheet_name):
        table_dict = {sheet_name: {"columns": [], "data": []}}
        table_dict["sheets"] = [
            "Loan List",
            "Inputs",
            "Cash Balance Projections",
            "Credit Balance Projection"
        ]
        table_dict[sheet_name]["columns"] = [
            {"label": column, "key": column.replace(" ", "_")} for column in df.columns
        ]

        for index, row in df.iterrows():
            row_data = {}

            for col, value in row.items():
                if df.dtypes[col] in ["datetime64[ns]"]:
                    if value is pd.NaT:
                        row_data[col.replace(" ", "_")] = ""
                    else:
                        # row_data[col.replace(' ', '_')] = value.strftime("%Y-%m-%d")
                        value = value.strftime("%Y-%m-%d")
                        row_data[col.replace(" ", "_")] = value  # .strftime("%Y-%m-%d")
                elif df.dtypes[col] in ["int64"]:
                    if value != value:
                        row_data[col.replace(" ", "_")] = ""
                    else:
                        if sheet_name in percentage_map.keys():
                            if col in percentage_map[sheet_name].keys():
                                if percentage_map[sheet_name][col]["is_conditional"]:
                                    if (
                                        row[row[0]]
                                        in percentage_map[sheet_name][col][
                                            "percent_row_identifier"
                                        ]
                                    ):
                                        value = "{:,.01f}%".format(value * 100)
                                else:
                                    value = "{:,.01f}%".format(value * 100)
                            else:
                                value = "{:,.0f}".format(value)
                        row_data[col.replace(" ", "_")] = value  #'{:,}'.format(value)
                elif df.dtypes[col] in ["float64"]:
                    if value != value:
                        row_data[col.replace(" ", "_")] = ""
                    else:
                        if sheet_name in percentage_map.keys():
                            if col in percentage_map[sheet_name].keys():
                                if percentage_map[sheet_name][col]["is_conditional"]:
                                    if (
                                        row[0]
                                        in percentage_map[sheet_name][col][
                                            "percent_row_identifier"
                                        ]
                                    ):
                                        value = "{:,.01f}%".format(value * 100)
                                else:
                                    value = "{:,.01f}%".format(value * 100)
                            else:
                                value = "{:,.0f}".format(value)
                        # row_data[col.replace(' ', '_')] = '{:.2f}%'.format(value)
                        row_data[col.replace(" ", "_")] = value
                else:
                    if value != value:
                        row_data[col.replace(" ", "_")] = ""
                    else:
                        row_data[col.replace(" ", "_")] = value

            table_dict[sheet_name]["data"].append(row_data)
        return table_dict
