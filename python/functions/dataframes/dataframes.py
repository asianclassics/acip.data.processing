import pandas as pd
from difflib import SequenceMatcher


def clean_columns(worksheet_name):
    df = pd.DataFrame.from_records(worksheet_name.get_all_values())
    df = df.rename(columns=df.iloc[0]).drop(df.index[0])
    df.columns = df.columns \
        .str.strip() \
        .str.replace(r'[^\x00-\x7f]', r'') \
        .str.lower() \
        .str.replace(r'[()#,\';]', r'') \
        .str.strip() \
        .str.replace(' ', '_')

    return df


# extend data ###################################
# CREATE URL / CREATE PAGE NUMBERS
# ###############################################
# create URL endpoint for each title
# this URL should also have endpoint for each page
# final page param found inside the input text
def create_url(d):
    # grab all columns needed to create the URL
    # cols = ['this', 'that']
    return None


def split_by(x, char):
    return pd.Series(str(x).split(char))


def create_column_mapper(x_target_cols, y_input_cols, threshold=0.9):
    mapper = {}
    for x in x_target_cols:
        for y in y_input_cols:
            if similar_sequence(x, y) > threshold:
                mapper.update({y: x})

    return mapper


def similar_sequence(a, b):
    return SequenceMatcher(None, a, b).ratio()
