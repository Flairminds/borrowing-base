import re

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