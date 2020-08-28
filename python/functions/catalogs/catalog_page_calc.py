import re
import math
from tqdm import tqdm
from collections import Counter
from functools import lru_cache
from python.functions.dataframes.dataframe_utils import split_by, create_url, create_urls
from warnings import simplefilter
from pandas import DataFrame, Series
import numpy as np
simplefilter(action='ignore', category=FutureWarning)  # just to suppress pandas Panel FutureWarning


pattern_folio_split = '(\\d+)([AB]){1,2}|(?:INC(.*))'
pattern_inc = '(?:INC(.*))'
stateful_vars = Counter()
stateful_vars['rows_skipped'] = 0


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


@lru_cache()
def get_page_numbers_alt(folio, previous_page=0):

    if folio is None:
        # add logging
        stateful_vars['rows_skipped'] += 1
        return None

    # check if we can make a number out of the folio, if not return empty series
    if isinstance(folio, float):
        if math.isnan(folio):
            print('nan bread', folio)
        # add logging
        stateful_vars['rows_skipped'] += 1
        return Series([])  # 0, 'A'

    # create a list from the folio
    lst = re.split(pattern_folio_split, folio)
    lst = list(filter(None, lst))

    # set up the calculation
    num, *letter = lst
    letter = letter[0] if letter else 'A'
    updater = 1 if letter[0] == 'A' else 0

    # make the calculation for relative page, which is always how it's presented
    # for instance vol_order 002 will have folios 1A-4B, etc...
    # here's the formula (2n - L) - previous_page (if B: L = 0 , if A: L = 1 )
    calc = (2 * int(num) - updater) + previous_page

    # must add something when a page is starting from previous title's page
    # ie. when within a vol you have title folios like this: 1A-4B, 4B-9A, etc
    # instead of each title starting 'relatively' at 1A
    # to find relative pages you need to subtract previous page from entire formula
    # if start and previous_page == 0 and (int(num) > 1 or letter != 'A'):
    #     previous_page = calc - 1

    return calc


# @lru_cache(maxsize=None)
def extractor(column):
    if isinstance(column, float):
        if math.isnan(column):
            print('nan bread', column)
        # add logging
        stateful_vars['rows_skipped'] += 1
        return Series([])  # 0, 'A'

    lst = re.split(pattern_folio_split, column)  # r'(\d+)([AB]?)'
    return list(filter(None, lst))


def split_pages(column):
    lst = ["".join(x) for x in re.findall(pattern_folio_split, column)]
    # print(f"split pages, {lst}, {column}")
    if lst:
        return lst
    else:
        return [None]


def extract_folio_pieces(folios):
    start_lst = []
    end_lst = []
    f_inc = ''
    f_start, *f_end = split_pages(folios.strip())
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

    return f_start, f_end, start_lst, end_lst, f_inc


def process_folio_pieces(row):
    # print('just entered', row['nlm_catalog'], row['prev_folios'], row['folios'])
    # can pass in row (axis=1) or column (axis=0) as Series
    # if you pass in a single column, each value comes in as str
    # final_list = [''] * 9

    if not row['folios'] or len(row['folios']) < 2:
        # log something
        stateful_vars['rows_skipped'] += 1
        return Series([''] * 9)

    f_start, f_end, start_lst, end_lst, f_inc = extract_folio_pieces(row['folios'])

    # get relative page numbers for all rows
    start_page_relative = get_page_numbers_alt(f_start) if f_start is not None else 0
    end_page_relative = get_page_numbers_alt(f_end) if f_end is not None else 0
    relative_pages = [f"p{start_page_relative}-p{end_page_relative}"]
    start_page_absolute = start_page_relative
    end_page_absolute = end_page_relative
    absolute_pages = relative_pages

    # at this point we have each piece needed
    # now we need to get absolute page numbers if vol_order > 1
    if stateful_vars['last_vol'] == row['vol']:
        start_page_absolute = start_page_relative + stateful_vars['last_abs_page']
        end_page_absolute = end_page_relative + stateful_vars['last_abs_page']
        absolute_pages = [f"p{start_page_absolute}-p{end_page_absolute}"]

    # rows to remember for next iteration
    stateful_vars['last_vol'] = row['vol']
    stateful_vars['last_abs_page'] = end_page_absolute
    stateful_vars['first_abs_page'] = start_page_absolute

    final_list = relative_pages + absolute_pages + [start_page_absolute] + [end_page_absolute] + [f_inc]
    return Series(final_list)


# transform folio numbers into pages
# page numbers continue across titles
# so within one volume there are many titles
# each title is assigned folio numbers that begin with 1A (generally)
# but if it's the 2nd title in a volume, then the 1A actually starts after the 3B from the previous title
def create_page_numbers(d):
    # initialize progress bar for pandas using tqdm
    tqdm.pandas()
    # grab all relevant columns
    cols = ['nlm_catalog', 'input_file_number', 'page_numbers', 'authors_name', 'full_title', 'colophon']
    data = DataFrame(d[cols]).rename(columns={"page_numbers": "folios"})
    data.sort_values('nlm_catalog', inplace=True)

    # split catalog into volume ID and title number (vol order)
    data[['vol', 'vol_order']] = data['nlm_catalog'].apply(split_by, args="-")

    # create IIIF url for each catalog record
    data[[
        'bdrc_id', 'bdrc_image_id', 'nlm_url'
          ]] = data['input_file_number'].apply(create_url, args="-")

    # if you need to add the previous rows value to current row for a specific column
    # data[['prev_folios']] = data['folios'].shift()

    # main processing step for folios
    # create both relative and absolute page ranges
    # relative: page range within only that specific title
    # absolute: page range within volume
    data[[
        'relative_pages', 'approx_page_range', 'start_page_absolute', 'end_page_absolute', 'notes'
    ]] = data.progress_apply(lambda x: process_folio_pieces(x), axis=1)

    # this is a hack, to get more reliable URLs use GenerateDocument (but first split out Update)
    data[['scan_url', 'first_image_url', 'download_url']] = data.progress_apply(lambda x: create_urls(x), axis=1)

    # fast implementation of url code check
    # data[['status_code']] = data['first_image_url'].apply(get_request).apply(get_status_code)

    # data.rename({
    #     'nlm_catalog': 'catno',
    #     'bdrc_id': 'librarynumber',
    #     'authors_name': 'author-tibetan',
    #     'full_title': 'title-tibetan'
    # }, inplace=True)

    final_columns = ['nlm_catalog', 'bdrc_id', 'folios',
                     'approx_page_range', 'scan_url', 'download_url',
                     'authors_name', 'full_title', 'colophon'
                     ]

    # rearrange column order
    data = DataFrame(data[final_columns]).rename(columns={
        'nlm_catalog': 'catno',
        'bdrc_id': 'librarynumber',
        'approx_page_range': 'approx-page-range',
        'scan_url': 'url-scan',
        'download_url': 'url-download',
        'authors_name': 'author-tibetan',
        'full_title': 'title-tibetan'
    })

    data['collection'] = 'mongolia'
    data['catno'].replace('', np.nan, inplace=True)
    data.dropna(axis=0, subset=['catno'], inplace=True)
    data.fillna('', inplace=True)
    data.name = 'title_catalogs'

    print(f"rows skipped during processing, {stateful_vars['rows_skipped']} /// ADD LOGGING FOR THIS.")
    print(data.shape[0], data.shape[1])

    return data


# prev_start, prev_end, prev_start_lst, prev_end_lst, prev_inc = extract_folio_pieces(row['prev_folios'])
# now do calc but starting from absolute position...
# prev page number is the prev_end calc
# previous_page_num = get_page_numbers_alt(prev_end)
#
# start_page_absolute = get_page_numbers_alt(f_start, previous_page=previous_page_num)
# end_page_absolute = get_page_numbers_alt(f_end, previous_page=previous_page_num)
# absolute_pages = [start_page_absolute, end_page_absolute]
# if int(row['vol_order']) > 1 and row['vol'] == stateful_vars['last_vol']:
#
#     print(stateful_vars)
#     print(row['nlm_catalog'], row['vol_order'])
