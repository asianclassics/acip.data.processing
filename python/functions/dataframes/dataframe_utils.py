from functools import lru_cache

import pandas as pd
from difflib import SequenceMatcher
import httplib2
from requests_futures.sessions import FuturesSession
import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import RequestException, ConnectionError, Timeout
from urllib3.connection import HTTPSConnection
from urllib3.exceptions import ConnectTimeoutError


nlm_url = 'http://nlm.asianclassics.org/uv.html'
bdrc_iiif = 'http://iiifpres.bdrc.io/2.1.1'
bdrc_io = 'https://iiif.bdrc.io'
flag_check_url = False


def get_request(url):
    session = FuturesSession()
    session.mount('https://', HTTPAdapter(max_retries=0))
    return session.head(url, timeout=1)


def get_status_code(r):
    print(r.result())
    try:
        return r.result().status_code
    except (ConnectionError, ConnectTimeoutError, Timeout) as e:
        print('timed out prob', e)
        return 408  # Request Timeout
    except RequestException as e:
        print('generic exception', e)
        return 409


# extend data ###################################
# CREATE URL / CREATE PAGE NUMBERS
# ###############################################
# create URL endpoint for each title
# this URL should also have endpoint for each page
# final page param found inside the input text
# http://nlm.asianclassics.org/en/archives/doc/bdr:W1NLM89
# http://nlm.asianclassics.org/uv.html?manifest=http://iiifpres.bdrc.io/2.1.1/v:bdr:V1NLM89_I1NLM89_001/manifest#?cv=2
# f"{nlm_url}?manifest={bdrc_iiif}/v:bdr:{bdrc_id}/manifest#?cv={idx}"
def create_url(x, char):
    # grab all columns needed to create the URL
    # cols = ['this', 'that']
    if x:
        lst_bdrc = str(x).split(char, maxsplit=2)
        lst_bdrc.append(f"http://nlm.asianclassics.org/en/archives/doc/bdr:{lst_bdrc[0]}")
        return pd.Series(lst_bdrc)
    else:
        return pd.Series([])


# FutureSession allows for parallel processing...
@lru_cache(maxsize=None)
def check_url_status(url):
    session = FuturesSession()
    r = session.head(url, timeout=1)
    valid_url = True if r.result().status_code == 200 else False
    return valid_url


def create_urls(row):
    if isinstance(row['bdrc_id'], str) and len(str(row['bdrc_id'])) > 4 and row['start_page_absolute']:

        b = str(row['bdrc_id'])[1:]
        cv = row['start_page_absolute'] if isinstance(row['start_page_absolute'], int) else 1
        cv_end = row['end_page_absolute'] if isinstance(row['end_page_absolute'], int) else ''
        # url for title page within volume
        scan_url = f"{nlm_url}?manifest={bdrc_iiif}/v:bdr:V{b}_I{b}_001/manifest#?cv={cv}"
        # first image URL
        first_image_url = f"{bdrc_io}/bdr:V{b}_I{b}_001::I{b}_0010001.jpg/full/max/0/default.jpg"

        # download pdf link
        # https://iiif.bdrc.io/download/pdf/v:bdr:I1KG1719::1-
        # download_url = f"{bdrc_io}/download/pdf/v:bdr:I{b}_001::{cv}-{cv_end}"
        download_url = f"{bdrc_io}/download/pdf/v:bdr:I{b}_001::1-"

        # check validity of URL
        if flag_check_url:
            if check_url_status(first_image_url):
                return pd.Series([scan_url, first_image_url])
        else:
            return pd.Series([scan_url, first_image_url, download_url])

    return pd.Series([])


def split_by(x, char):
    return pd.Series(str(x).split(char))


def create_column_mapper(x_target_cols, y_input_cols, threshold=0.9):
    mapper = {}
    for x in x_target_cols:
        for y in y_input_cols:
            if similar_sequence(x, y) > threshold:
                mapper.update({y: x})

    return mapper


def clean_columns(data):
    # df = pd.DataFrame.from_records(worksheet_name.get_all_values())
    df = pd.DataFrame(data)
    df = df.rename(columns=df.iloc[0]).drop(df.index[0])
    df.columns = df.columns \
        .str.strip() \
        .str.replace(r'[^\x00-\x7f]', r'') \
        .str.lower() \
        .str.replace(r'[()#,\';]', r'') \
        .str.strip() \
        .str.replace(' ', '_')

    return df


def similar_sequence(a, b):
    return SequenceMatcher(None, a, b).ratio()
