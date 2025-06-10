import pandas as pd
from datetime import datetime

from source.utility.ServiceResponse import ServiceResponse

percentage_map = {
    "Portfolio": {
        "Acquisition Price": {"is_conditional": False},
        "Spread": {"is_conditional": False},
    }
}

class PSSL_WIA:
    @staticmethod
    def convert_to_table(df, sheet_name):
        try:
            table_dict = {sheet_name: {"columns": [], "data": []}}
            table_dict["sheets"] = [
                "Portfolio",
                "VAE",
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
                            if(type(value) == datetime):
                                value = value.strftime("%Y-%m-%d")
                            row_data[col.replace(" ", "_")] = value

                table_dict[sheet_name]["data"].append(row_data)
            
            return ServiceResponse.success(data=table_dict)
        
        except Exception as e:
            return ServiceResponse.error(message = "Internal Server Error")
