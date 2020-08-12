from __future__ import print_function
from os import path
import pandas as pd
from googleapiclient.http import MediaFileUpload
from python.functions import authorize_google, get_sheet_data, get_drive_items
from python.config import conf_gs


'''
GET DRIVE ITEMS
so far we have, 
1) downloaded the google sheet data into a pandas dataframe
2) processed GS data within df
2) searched for the drive folder that will hold our text files
3) listed the current files in that folder

TO DO
4) write each record in the dataframe to the text file, separated by '***********************************'
5) upload the file to google drive
'''

# 0. define query ######################################################################
# QUERY STRING EXAMPLES
# https://developers.google.com/drive/api/v3/search-files#query_string_examples
folder_name = 'NLMCatalog_TextFiles'
driveId = "0AEv34UqlfkRPUk9PVA"  # TECH share drive
folder_query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder'"
upload_text_file_name = 'mongolia_catalog_official'
# 1. CONNECT / AUTHORIZE ---------------------------------------------------------------
# authorize google, for google sheets and google drive
SHEETS, DRIVE = authorize_google(**conf_gs)

# 2. INPUT DATA -------------------------------------------------------------------------
# download catalog data from GoogleSheets to dataframe
title_catalog_worksheets, df = get_sheet_data(SHEETS, test=False, output_type='minimal', **conf_gs)
# print(df)
# quit()
# data to df
# df = pd.DataFrame(data)
# df = df.rename(columns=df.iloc[0]).drop(df.index[0])
# create mask, all columns you want to ignore
# mask = df.iloc[0].isin([None, ''])
# the ~ means reverse it
# df = df.loc[:, ~mask]
# df.drop(df.index[0:2], inplace=True)

print(df.columns)

# 3. OUTPUT DATA ------------------------------------------------------------------------
# find current output text files (if exist)
# search for the folder of interest and get its ID
folder_id = get_drive_items(DRIVE, folder_query, driveId)
if folder_id is None:
    quit()

print(folder_id)
# TO DO: check if file exists and how old it is...
# if found, then query to find files in that folder
# files_query = f"'{folder_id[0]}' in parents"
# get files
# directory_files = get_drive_items(DRIVE, files_query, driveId, flag_type='file')


# 4. OUTPUT ----------------------------------------
# write output to local file
output_file = path.join(path.dirname(__file__), f"../data/{upload_text_file_name}.txt")
with open(output_file, 'w', encoding='utf-8') as outfile:
    for row_idx, row in enumerate(df.itertuples(index=False, name='CatalogItem')):
        for idx, x in enumerate(row):
            outfile.write(f"{df.columns[idx]}: {x}\n")
        outfile.write('\n=======================================================\n')
        # print(f'Writing row {row_idx}\r', end="")
        print("Progress {:2.1%}".format(row_idx / 10), end="\r")

# copy to drive
# file_metadata = {
#     'name': f'{upload_text_file_name}.txt',
#     'mimeType': 'text/plain',
#     'parents': folder_id
# }
#
# media = MediaFileUpload(output_file, resumable=True)
# file = DRIVE.files().create(
#     body=file_metadata,
#     media_body=media,
#     fields='id',
#     supportsAllDrives=True
# ).execute()
# print(f"\nUploaded {upload_text_file_name}.txt with fileId: {file.get('id')}")
