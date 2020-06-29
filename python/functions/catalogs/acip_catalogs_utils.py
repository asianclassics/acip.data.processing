import re
import math
import pandas as pd
from difflib import SequenceMatcher
from functools import lru_cache

pattern_folio_split = '(\\d+)([AB]){1,2}|(?:INC(.*))'
pattern_inc = '(?:INC(.*))'

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

    
def create_column_mapper(x_target_cols, y_input_cols, threshold=0.9):
    mapper = {}
    for x in x_target_cols:
        for y in y_input_cols:
            if similar(x, y) > threshold:
                mapper.update({y: x})

    return mapper


def set_up_data_frame(worksheet_name):
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


# use: df['sum'], df['prod'], df['quot'] = zip(*map(sum_prod_quot, df['a'], df['b'], df['c']))
def calculate_pages(row):
    start_letter, start_n, end_letter, end_n = row['start_letter'], row['start_num'], row['end_letter'], row['end_num']
    updater = 1 if start_letter == 'B' else 0
    if start_n:
        start_page = 2*int(start_n) + updater
    updater = 1 if end_letter == 'B' else 0
    if end_n:
        end_page = 2*int(end_n) + updater
    return start_page, end_page


def get_side(row):
    if row['start_letter'] == 'B':
        return 1
    return 0
    # return 1 if letter == 'B' else 0


def get_absolute_folio(page):
    if page % 2 == 0:
        # it's B, formula: page/2
        calc = int(page/2)
        return f"{calc}B"
    else:
        # it's A, formula: page + 1 / 2
        calc = (int(page + 1) / 2)
        return f"{calc}A"


@lru_cache(maxsize=None)
def get_page_numbers(folio, start=False, previous_page=0):

    if isinstance(folio, float):
        if math.isnan(folio):
            print('nan bread', folio)
        return pd.Series([])  # 0, 'A'

    lst = re.split(pattern_folio_split, folio)
    lst = list(filter(None, lst))

    num, *letter = lst
    letter = letter[0] if letter else 'A'
    updater = 1 if letter[0] == 'A' else 0
    # here's the formula (2n - L) - previous_page (if B: L = 0 , if A: L = 1 )
    calc = (2*int(num) - updater) - previous_page

    # to find relative pages you need to subtract previous page from entire formula
    if start and previous_page == 0 and (int(num) > 1 or letter != 'A'):
        previous_page = calc - 1

    return calc, previous_page


@lru_cache(maxsize=None)
def extractor(column):
    if isinstance(column, float):
        if math.isnan(column):
            print('nan bread', column)
        return pd.Series([])  # 0, 'A'

    lst = re.split(pattern_folio_split, column)  # r'(\d+)([AB]?)'
    return list(filter(None, lst))


def split_pages(column):
    lst = ["".join(x) for x in re.findall(pattern_folio_split, column)]
    # print(f"split pages, {lst}, {column}")
    if lst:
        return lst
    else:
        return [None]


def extract_folio_pieces(row):
    # print('just entered', row['nlm_catalog'])
    # can pass in row (axis=1) or column (axis=0) as Series
    # if you pass in a single column, each value comes in as str
    # final_list = [''] * 9
    # force relative pages to take up columns in data frame
    relative_pages = ['', '']
    f_inc = ''

    if len(row['page_numbers']) < 2:  # or not row['nlm_catalog']:
        print('skip \n', row['nlm_catalog'], row)
        return pd.Series([''] * 9)

    f_start, *f_end = split_pages(row['page_numbers'].strip())
    # print(f_start)
    if f_end:
        f_end, *f_inc = f_end
        if len(f_end) > 5:
            f_inc = f_end
            f_end = None
    else:
        f_end = None

    if f_start is not None and f_end is not None:
        start_lst = extractor(f_start)
        end_lst = extractor(f_end)

        start_page_absolute, previous_page_num = get_page_numbers(f_start, start=True)
        end_page_absolute, *_ = get_page_numbers(f_end)

        if previous_page_num > 0:
            start_page_relative, *_ = get_page_numbers(f_start, start=True, previous_page=previous_page_num)
            end_page_relative, *_ = get_page_numbers(f_end, start=False, previous_page=previous_page_num)
            relative_pages = [start_page_relative, end_page_relative]

        absolute_pages = [start_page_absolute, end_page_absolute]

        final_list = start_lst + end_lst + absolute_pages + relative_pages + f_inc
        return pd.Series(final_list)


# transform folio numbers into pages
# page numbers continue across titles
# so within one volume there are many titles
# each title is assigned folio numbers that begin with 1A (generally)
# but if it's the 2nd title in a volume, then the 1A actually starts after the 3B from the previous title
def create_page_numbers(d):
    # grab all relevant columns
    cols = ['nlm_catalog', 'page_numbers']
    data = pd.DataFrame(d[cols])

    # split catalog into volume ID and title number (vol order)
    data[['vol', 'vol_order']] = data['nlm_catalog'].apply(split_by, args="-")

    # split the folio numbers into their parts (number and letter)
    data[[
        'start_num', 'start_letter', 'end_num', 'end_letter',
        'start_page', 'end_page', 'relative_start', 'relative_end', 'notes'
    ]] = data.apply(lambda x: extract_folio_pieces(x) if x['page_numbers'] else print('no page numbers'), axis=1)

    # data.apply(lambda x: extract_folio_pieces(x) if x['page_numbers']
    # else pd.Series(['', '', '', '', '', '', '', '', '']), axis=1)
    print('did i make it?')
    data.sort_values('nlm_catalog')

    data.fillna('', inplace=True)
    data.name = 'title_catalogs'

    print(data.shape[0], data.shape[1])
    print(data.iloc[5:9])

    return data

