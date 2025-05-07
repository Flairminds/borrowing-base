import re
from numerize import numerize
import locale

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
        return numerize.numerize(float(value))
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