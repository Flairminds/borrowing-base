from datetime import datetime
import pandas as pd

def excel_to_df(excel):
    sheet_df_map = pd.read_excel(excel, sheet_name=None, na_values=["N/A"])
    return sheet_df_map


def update_to_std_sheet(std_sheet, xl_sheet_df_map, std_file_format):
    matched_index = [xl_sheet.lower() for xl_sheet in xl_sheet_df_map.keys()].index(
        std_sheet.lower()
    )
    xl_sheet_name = [xl_sheet for xl_sheet in xl_sheet_df_map.keys()][matched_index]
    xl_sheet_df_map[std_sheet] = xl_sheet_df_map[xl_sheet_name]
    del xl_sheet_df_map[xl_sheet_name]
    return xl_sheet_df_map


def find_missing_sheets(xl_sheet_df_map, std_file_format):
    sheet_modifications = []

    for std_sheet in std_file_format.keys():
        if std_sheet.lower() in [
            xl_sheet.strip().lower() for xl_sheet in xl_sheet_df_map.keys()
        ]:
            if std_sheet not in xl_sheet_df_map.keys():
                xl_sheet_df_map = update_to_std_sheet(std_sheet, xl_sheet_df_map)
        else:
            sheet_modifications.append(
                f"<b>{std_sheet}</b> is not present in uploaded file"
            )

    return xl_sheet_df_map, sheet_modifications


def update_column_name(df, std_column, std_file_format):
    matched_index = [column.lower() for column in df.columns].index(std_column.lower())
    replacable_column = df.columns[matched_index]

    df.rename(columns={replacable_column: std_column}, inplace=True)
    return df


def find_error_row(df, std_column, std_dtype):
    series = df[std_column]
    error_rows_list = []
    for index, value in series.items():
        xl_col_dtype = type(value)
        # if xl_col_dtype == 'float64' or xl_col_dtype == 'int64':
        if xl_col_dtype == int or xl_col_dtype == float:
            if value != value:  # to check nan value
                error_rows_list.append(index)
            else:
                xl_col_dtype = "Number"
                if xl_col_dtype != std_dtype:
                    error_rows_list.append(index)

        if xl_col_dtype == str:
            xl_col_dtype = "object"
            if xl_col_dtype != std_dtype:
                error_rows_list.append(index)

        if xl_col_dtype == datetime:
            xl_col_dtype = "datetime64[ns]"
            if xl_col_dtype != std_dtype:
                error_rows_list.append(index)
    return error_rows_list


def find_dtype_error(df, std_sheet_name, std_column, std_dtype):
    xl_col_dtype = df[std_column].dtype
    if xl_col_dtype == "float64" or xl_col_dtype == "int64":
        xl_col_dtype = "Number"

    if xl_col_dtype != std_dtype:
        return f"{std_column} of {std_sheet_name} must be {std_dtype}"
    return None


def find_missing_columns(
    df, std_sheet_name, xl_sheet_df_map, error_map, std_file_format
):
    missing_columns = []
    std_seleced_sheet_data = std_file_format[std_sheet_name]
    for std_column in std_seleced_sheet_data.keys():
        if std_column.lower() in [column.lower() for column in df.columns]:
            if std_column not in df.columns:
                updated_dframe = update_column_name(df, std_column, std_file_format)
                xl_sheet_df_map[std_sheet_name] = updated_dframe

            # finding datatype error
            dtype_error = find_dtype_error(
                df,
                std_sheet_name,
                std_column,
                std_file_format[std_sheet_name][std_column],
            )
            if dtype_error is not None:
                # check for error row
                error_row_list = find_error_row(
                    df, std_column, std_file_format[std_sheet_name][std_column]
                )

                dtype_error_msg = f"<div><b>{std_column}</b> column of <b>{std_sheet_name}</b> sheet must be in <b>{std_file_format[std_sheet_name][std_column]}</b> format.</div> "

                if error_row_list:
                    dtype_error_msg += (
                        "<div>Please check values corresponding to following rows"
                    )
                    for error_row_id in error_row_list:
                        row_name = df[df.columns[0]].iloc[error_row_id]
                        dtype_error_msg += f"<ul style='list-style-type:disc;'><li><b>{row_name}</b></li></ul>"
                        if (
                            error_row_list.index(error_row_id)
                            != len(error_row_list) - 1
                        ):
                            dtype_error_msg += " ,"
                    dtype_error_msg += "</div>"

                error_map["Data Format Modifications"].append(dtype_error_msg)
        else:
            error_map["Column Modifications"].append(
                f"<b>{std_column}</b> is not present in {std_sheet_name}"
            )

    return missing_columns, xl_sheet_df_map


def validate_file(excel, std_file_format):
    error_map = {
        "Sheet Modifications": [],
        "Column Modifications": [],
        "Data Format Modifications": [],
    }
    xl_sheet_df_map = excel_to_df(excel)

    # find missing sheets
    xl_sheet_df_map, sheet_modifications = find_missing_sheets(
        xl_sheet_df_map, std_file_format
    )
    error_map["Sheet Modifications"] = sheet_modifications

    # find missing cols and check datatype
    for sheet_name in xl_sheet_df_map.keys():
        if sheet_name in std_file_format.keys():
            missing_columns, xl_sheet_df_map = find_missing_columns(
                xl_sheet_df_map[sheet_name],
                sheet_name,
                xl_sheet_df_map,
                error_map,
                std_file_format,
            )

    return error_map, xl_sheet_df_map
