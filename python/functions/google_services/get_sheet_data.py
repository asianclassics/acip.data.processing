from functools import reduce
import pandas as pd
from python.config.gs import target_columns, minimal_target_columns
from python.functions.dataframes.dataframe_utils import clean_columns, create_column_mapper

dict_keys = ['properties', 'title']
acip_wks = []
threshold = 0.99


def get_sheet_data(service, test=True, output_type='standard', **kwargs):
    if test:
        spreadsheet_name = kwargs["workbooks"]["mappings"]["key_2"]
    else:
        spreadsheet_name = kwargs["workbooks"]["mappings"]["normalized_accession"]
    target_cols = minimal_target_columns
    if output_type == 'standard':
        target_cols = target_columns
    # Call the Sheets API
    sheet = service.spreadsheets()

    if test:
        acip_wks.append('ACIP_Title_Test')
    else:
        sheets_meta = service.spreadsheets().get(spreadsheetId=spreadsheet_name).execute()
        sheets = sheets_meta.get('sheets', '')

        for s in sheets:
            current_sheet = reduce(dict.get, dict_keys, s)
            if 'acip-title-level-catalog' in current_sheet.lower():
                acip_wks.append(current_sheet)

    data_list = []
    for name in acip_wks:
        sheet_range = f'{name}!A1:Z'
        # get data, transform to data frame
        result = sheet.values().get(spreadsheetId=spreadsheet_name,
                                    range=sheet_range,
                                    majorDimension="ROWS").execute()
        data = result.get('values', [])

        data = clean_columns(data)
        # map out new column names
        m = create_column_mapper(target_cols, list(data.columns), threshold=threshold)
        new_cols = list(m.values())
        data = data.rename(columns=m)
        data = data[new_cols]  # only keep column names that match target

        # print(f"{name}: {data.shape[0]}, {data.shape[1]}")
        data_list.append(data)
        del data

    final_data = pd.concat(data_list)
    del data_list

    return acip_wks, final_data
