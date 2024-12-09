# import pandas as pd
# data = pd.ExcelFile(r"D:\Flairminds\Figma Borrowing Base\10.31.2023_PCOF_IV_Borrowing_Base_Basedata.xlsx")

# Dictionary = dict()
# for i in data.sheet_names:
#     Dictionary[i] = {}
#     sheet= pd.read_excel(r"D:\Flairminds\Figma Borrowing Base\10.31.2023_PCOF_IV_Borrowing_Base_Basedata.xlsx",sheet_name= f'{i}')
#     dtypes_json = dict(zip(sheet.columns,sheet.dtypes))
#     Dictionary[i] = str(dtypes_json)


# #######################################################

import pandas as pd
import json


def excel_to_json(excel_file):
    # Read Excel file
    xls = pd.ExcelFile(excel_file)

    json_data = {}

    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name)

        columns_data = {}
        for col_name, col_dtype in zip(df.columns, df.dtypes):
            columns_data[col_name] = str(col_dtype)

        json_data[sheet_name] = columns_data

    return json_data


excel_file_path = r"D:\Flairminds\Figma Borrowing Base\10.31.2023_PCOF_IV_Borrowing_Base_Basedata.xlsx"

# Convert Excel data to JSON
json_data = excel_to_json(excel_file_path)
