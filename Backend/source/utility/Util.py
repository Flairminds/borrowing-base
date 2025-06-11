import re
from numerize import numerize
import locale
import pandas as pd
from sqlalchemy import text
from models import db

def remove_special_characters_and_spaces(input_string):
    input_string = input_string.lower()
    cleaned_string = re.sub(r'[^a-zA-Z0-9]', '', input_string)
    return cleaned_string

def remove_special_characters_and_spaces_in_df(df):
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.replace('[^a-zA-Z0-9]', '', regex=True)
    return df

def create_lookup(string):
    s = re.sub(r'[^a-zA-Z0-9\s]', '', string)
    s = s.replace(' ', '_')
    return s.lower()

def currency_to_float(value):
    """
        Convert a currency or shorthand number string (e.g. '$1,234.56', '€5.7M') to float.
        Returns None if conversion fails.
    """
    if not value:
        return None
    
    if not isinstance(value, str):
        return value
 
    # Remove currency symbols and commas
    cleaned = re.sub(r'[^\d.\-KMBTkmabt]', '', value)
 
    try:
        # Use numerize to handle suffixes like K, M, B, etc.
        return float(numerize.decimal(cleaned))
    except Exception:
        try:
            # Fallback to plain float if no suffix
            return float(cleaned.replace(',', ''))
        except Exception:
            return None
        
def float_to_numerized(value):
    """
    Converts a float or int to a numerized string (e.g., 1200 ➜ '1.2K').
    Args:
        value (float|int): The numeric value to convert.
    Returns:
        str: Numerized string.
    """
    try:
        if value is None:
            return "0"
        return numerize.numerize(float(value), 2)
    except Exception as e:
        print(e)
        return value
    
# Example
# float_to_currency(1234.56)               # ➜ '$1,234.56'
# float_to_currency(9876543.21, '€')       # ➜ '€9,876,543.21'
# float_to_currency(1000000, '₹', 'en_IN') # ➜ '₹10,00,000.00'
    
def float_to_currency(value, currency_symbol='$', locale_code='en_US.UTF-8'):
    """
    Convert a float to a formatted currency string.
    Args:
        value (float): Numeric value to convert.
        currency_symbol (str): Symbol to prepend (e.g., '$', '€').
        locale_code (str): Locale code for formatting, defaults to 'en_US.UTF-8'.
    Returns:
        str: Formatted currency string.
    """
    try:
        # Set locale
        locale.setlocale(locale.LC_ALL, locale_code)
        # Format with thousands separator and 2 decimal places
        formatted = locale.currency(value, symbol=False, grouping=True)
        return f"{currency_symbol}{formatted}"
    except Exception:
        # Fallback if locale setting fails
        return f"{currency_symbol}{value:,.2f}"
    
def numerized_to_currency(numerized_value, currency_symbol = '$'):
    """
    Adds a currency symbol to numerized string (e.g., '1.2K' ➜ '$1.2K').
    Args:
        numerized_value (str): Numerized string.
        currency_symbol (str): Currency Symbol.
    Returns:
        str: Numerized currency string.
    """
    try:
        if numerized_value is None:
            return "0"
        return f"{currency_symbol}{numerized_value}"
    except (TypeError, ValueError):
        return "0"
    
def currency_to_float_to_numerize_to_currency(value):
   return numerized_to_currency(float_to_numerized(currency_to_float(value)))

def excel_cell_format(writer, sheet_dfs, sheet_name, sheet_format, column_info):
    try:
        dataframe = sheet_dfs[sheet_name]
 
        if sheet_format == 'key_value':
            format_values = {}
            for column_lookup, column_name, data_type, unit, _ in column_info:
                if column_name not in dataframe.index:
                    continue
                    
                value = dataframe.loc[column_name]
                
                if data_type == 'date':
                    if isinstance(value, pd.Series):
                        if pd.api.types.is_datetime64tz_dtype(value):
                            value = value.dt.tz_localize(None)
                        value = pd.to_datetime(value, errors='coerce')
                    else:
                        try:
                            value = pd.to_datetime(value, errors='coerce')
                        except Exception:
                            value = pd.NaT
                    dataframe.loc[column_name] = value
                    format_values[column_name] = 'mm/dd/yyyy'
                    
                elif data_type == 'float':
                    if unit == 'percent':
                        format_values[column_name] = '0.00%'
                    elif unit == 'currency':
                        format_values[column_name] = '#,##0.00'
                    elif unit == 'decimal':
                        format_values[column_name] = '#,##0.00'

            key_col_name = dataframe.index.name if dataframe.index.name else 'Key'
            value_col_name = dataframe.name if dataframe.name else 'Value'
            excel_df = pd.DataFrame({key_col_name: dataframe.index, value_col_name: dataframe.values})
            excel_df.to_excel(writer, sheet_name=sheet_name, index=False)

            # Apply formatting
            if format_values:
                worksheet = writer.sheets[sheet_name]
                for row in range(2, len(excel_df) + 2):  # Start from row 2 (skip header)
                    key_cell = worksheet.cell(row=row, column=1)
                    if key_cell.value in format_values:
                        value_cell = worksheet.cell(row=row, column=2)
                        value_cell.number_format = format_values[key_cell.value]

        else:
            columns_in_db = [col[1] for col in column_info]
            columns_not_in_db = [col for col in dataframe.columns if col not in columns_in_db]
            final_columns = columns_in_db + columns_not_in_db

            dataframe = dataframe[[col for col in final_columns if col in dataframe.columns]]
            format_columns = {}
            for column_lookup, column_name, data_type, unit, _ in column_info:
                if column_name not in dataframe.columns:
                    continue

                elif data_type == 'date':
                    if pd.api.types.is_datetime64tz_dtype(dataframe[column_name]):
                        dataframe[column_name] = dataframe[column_name].dt.tz_localize(None)

                    dataframe[column_name] = pd.to_datetime(dataframe[column_name], errors='coerce')
                    dataframe[column_name] = dataframe[column_name].dt.strftime('%m/%d/%Y')                

                elif data_type == 'float':
                    if unit == 'percent':
                        format_columns[column_name] = '0.00%'
                    elif unit == 'currency':
                        format_columns[column_name] = '#,##0.00'
                    elif unit == 'decimal':
                        format_columns[column_name] = '#,##0.00'

            dataframe.to_excel(writer, sheet_name=sheet_name, index=False)
            if format_columns:
                worksheet = writer.sheets[sheet_name]
                
                # Apply formats to columns
                for col_name, number_format in format_columns.items():
                    col_idx = dataframe.columns.get_loc(col_name)
                    col_letter = chr(65 + col_idx) if col_idx < 26 else chr(64 + col_idx // 26) + chr(65 + col_idx % 26)
                    
                    # Skip header row and format all data rows
                    for row in range(2, len(dataframe) + 2):
                        cell = worksheet[f"{col_letter}{row}"]
                        cell.number_format = number_format

        return dataframe
            
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"