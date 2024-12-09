import pandas as pd

std_file_format = {
    "Availability Borrower": {"A": "object", "B": "object"},
    "Principle Obligations": {
        "Principal Obligations": "object",
        "Currency": "object",
        "Amount": "Number",
        "Spot Rate": "Number",
        "Dollar Equivalent": "Number",
    },
    "Subscription BB": {
        "Investor": "object",
        "Master/Feeder": "Number",
        "Ultimate Investor Parent": "Number",
        "Designation": "object",
        "Commitment": "Number",
        "Capital Called": "Number",
    },
    "PL BB Build": {
        "Investment Name": "object",
        "Issuer": "object",
        "Investment Investment Type": "object",
        "Investment Industry": "object",
        "Investment Closing Date": "datetime64[ns]",
        "Investment Maturity": "datetime64[ns]",
        "Investment Par": "Number",
        "Investment Cost": "Number",
        "Investment External Valuation": "Number",
        "Investment Internal Valuation": "Number",
        "Rates Fixed Coupon": "Number",
        "Rates Floating Cash Spread": "Number",
        "Rates Current LIBOR/Floor": "Number",
        "Rates PIK": "Number",
        "Rates Fixed / Floating": "object",
        "Classifications Quoted / Unquoted": "object",
        "Classifications Warehouse Asset": "object",
        "Classifications Warehouse Asset Inclusion Date": "Number",
        "Classifications Warehouse Asset Expected Rating": "Number",
        "Classifications Approved Foreign Jurisdiction": "Number",
        "Classifications LTV Transaction": "object",
        "Classifications Noteless Assigned Loan": "object",
        "Classifications Undelivered Note": "object",
        "Classifications Structured Finance Obligation": "object",
        "Classifications Third Party Finance Company": "object",
        "Classifications Affiliate Investment": "object",
        "Classifications Defaulted / Restructured": "object",
        "Financials LTM Revenue ($MMs)": "Number",
        "Financials LTM EBITDA ($MMs)": "Number",
        "Leverage Revolver Commitment": "Number",
        "Leverage Total Enterprise Value": "Number",
        "Leverage Total Leverage": "Number",
        "Leverage PCOF IV Leverage": "Number",
        "Leverage Attachment Point": "Number",
        "Leverage Total Capitalization": "Number",
        "Leverage LTV Thru PCOF IV": "Number",
        "Final Eligibility Override": "Number",
        "Final Comment": "Number",
        "Concentration Adjustment": "Number",
        "Concentration Comment": "Number",
        "Borrowing Base Other Adjustment": "Number",
        "Borrowing Base Industry Concentration": "Number",
        "Borrowing Base Comment": "Number",
        "Is Eligible Issuer": "object",
    },
    "PL BB Results": {"Concentration Tests": "object", "Concentration Limit": "Number"},
    "PL_BB_Results_Concentrations": {
        "Concentration Tests": "object",
        "Concentration Limit": "Number",
    },
    "PL_BB_Results_Security": {"Security": "object"},
    "Obligors' Net Capital": {"Obligors' Net Capital": "object", "Values": "Number"},
    "Pricing": {"Pricing": "object", "percent": "Number"},
    "Advance Rates": {"Investor Type": "object", "Advance Rate": "Number"},
    "Portfolio LeverageBorrowingBase": {
        "Investment Type": "object",
        "Unquoted": "Number",
        "Quoted": "Number",
    },
    "Concentration Limits": {
        "Investors": "object",
        "Rank": "Number",
        "Concentration Limit": "Number",
    },
    "Inputs Industries": {"Industries": "object"},
    "Other Metrics": {"Other Metrics": "object", "values": "Number"},
}


def excel_to_json(excel_file):
    # Read Excel file
    xls = pd.ExcelFile(excel_file)

    json_data = {}

    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name)

        columns_data = {}
        for col_name, col_dtype in zip(df.columns, df.dtypes):
            columns_data[col_name.lower()] = str(col_dtype)

        json_data[sheet_name] = columns_data

    return json_data


def find_file_format_change(excel_file):
    json_xls = excel_to_json(excel_file)
    error_map = {
        "Sheet Modifications": [],
        "Column Modifications": [],
        "Data Format Modifications": [],
    }
    # error_map = {}
    # with open('standard_file_format.json', 'r') as file:
    #     std_file_format = file.read()
    # std_file_format = eval(std_file_format)
    # std_file_sheets = std_file_format.keys()
    std_file_sheets = std_file_format.keys()
    for std_sheet in std_file_sheets:
        if std_sheet in json_xls.keys():
            std_sheet_data = std_file_format[std_sheet]
            for std_column, _ in std_sheet_data.items():
                lower_case_xls_columns = [
                    json_xls_column.lower()
                    for json_xls_column in json_xls[std_sheet].keys()
                ]

                if std_column.lower() in lower_case_xls_columns:
                    json_file_dtype = ""
                    if std_column not in json_xls[std_sheet].keys():
                        json_file_dtype = json_xls[std_sheet][std_column.lower()]
                        if json_file_dtype == "int64" or json_file_dtype == "float64":
                            json_file_dtype = "Number"
                    else:
                        json_file_dtype = json_xls[std_sheet][std_column]
                        if json_file_dtype == "int64" or json_file_dtype == "float64":
                            json_file_dtype = "Number"
                    if std_sheet_data[std_column] != json_file_dtype:
                        # send required datatype also
                        # error_map['data_type_error'].append(f"'{std_column}' column does not match with datatype of '{std_column}' column in '{std_sheet}' sheet of standard file format. Required datatyp of {std_column} must be {std_sheet_data[std_column]}")

                        # Or
                        error_map["Data Format Modifications"].append(
                            f"'{std_column}' column of '{std_sheet}' sheet must be {std_sheet_data[std_column]}"
                        )

                        # lis_of_datatype_error.append({sheet_name : column_name : datatype})
                else:
                    error_map["Column Modifications"].append(
                        f"'{std_column}' column is not present in '{std_sheet}' sheet of standard file format"
                    )
        else:
            error_map["Sheet Modifications"].append(
                f"'{std_sheet}' sheet is not present in uploaded file"
            )

        # for i in lis_of_datatype_error:
        #     series  = pd.read_excel(sheet_name)['columns']
        #     for s in series:
        #         if type(s)!=i[2]:
        #             s.index

    return error_map


def rename_columns(excel_file):
    dictionary = dict()
    # with open('standard_file_format.json', 'r') as file:
    #     std_file_format = file.read()
    # std_file_format = eval(std_file_format)
    data = pd.read_excel(excel_file, sheet_name=None)
    for key, value in std_file_format.items():
        table_variable = data[key]
        table_variable.columns
        value
        for j in table_variable.columns:
            for k in value:
                if j.lower() == k.lower():
                    table_variable.rename({j: k}, axis=1, inplace=True)
        table_variable
        dictionary[key] = table_variable
    return dictionary
