import pandas as pd

from source.utility.ServiceResponse import ServiceResponse

percentage_map = {
    "PL BB Build": {
        "Rates Floating Cash Spread": {"is_conditional": False},
        "Rates Current LIBOR/Floor": {"is_conditional": False},
        "Leverage LTV Thru PCOF IV": {"is_conditional": False},
    },
    "PL BB Results": {
        "Concentration Limit": {
            "is_conditional": True,
            "percent_row_identifier": [
                "Max. Issuer Concentration (% BB)",
                "Max. Industry Concentration (Largest Industry, % BB)",
                "Max. Industry Concentration (2nd Largest Industry, % BB)",
                "Max. Industry Concentration (All Other Industries, % BB)",
                "Max. Contribution to BB with Maturity > 8 years",
                "Max. PIK, DIP",
                "Min. Cash, First Lien, and Cov-Lite",
                "Min. Senior Secured",
                "Min. Weighted Average Cash Fixed Coupon",
                "Min. Weighted Average Cash Floating Coupon",
                "Max. LTV Transactions",
                "Max. Third Party Finance Companies",
                "Max. Foreign Eligible Portfolio Investments",
                "Max. Affiliate Investments",
                "Max. Warehouse Assets",
                "Max. Preferred Stock",
            ],
        }
    },
    "Pricing": {"percent": {"is_conditional": False}},
    "Advance Rates": {"Advance Rate": {"is_conditional": False}},
    "Portfolio LeverageBorrowingBase": {
        "Unquoted": {
            "is_conditional": True,
            "percent_row_identifier": [
                "First Lien",
                "Warehouse First Lien",
                "Last Out",
                "Second Lien",
                "High Yield",
                "Mezzanine",
                "Cov-Lite",
                "PIK",
                "Preferred Stock",
                "Equity",
            ],
        },
        "Quoted": {
            "is_conditional": True,
            "percent_row_identifier": [
                "Cash",
                "Cash Equivalent",
                "LT US Debt",
                "First Lien",
                "Warehouse First Lien",
                "Last Out",
                "Second Lien",
                "High Yield",
                "Mezzanine",
                "Cov-Lite",
                "PIK",
                "Preferred Stock",
                "Equity",
            ],
        },
    },
    "Concentration Limits": {"Concentration Limit": {"is_conditional": False}},
    "Other Metrics": {
        "values": {
            "is_conditional": True,
            "percent_row_identifier": [
                "LTV",
                "Concentration Test Threshold 1",
                "Concentration Test Threshold 1",
                "Threshold 1 Advance Rate",
                "Threshold 2 Advance Rate",
            ],
        }
    },
}
    

class PCOF_WIA:
    @staticmethod
    def convert_to_table(df, sheet_name):
        try:
            table_dict = {sheet_name: {"columns": [], "data": []}}
            table_dict["sheets"] = [
                "PL BB Build",
                "Other Metrics",
                "Availability Borrower",
                "PL BB Results",
                "Subscription BB",
                "PL_BB_Results_Security",
                "Inputs Industries",
                "Pricing",
                "Portfolio LeverageBorrowingBase",
                "Obligors' Net Capital",
                "Advance Rates",
                "Concentration Limits",
                "Principle Obligations",
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

            return ServiceResponse.success(data=table_dict)
        
        except Exception as e:
            return ServiceResponse.error(message = "Internal Server Error")
            
