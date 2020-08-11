from __future__ import print_function
import pandas as pd
from python.functions import authorize_google, get_sheet_data, get_drive_items
from python.config import conf_gs

'''
GET DRIVE ITEMS
so far we have, 
1) downloaded the google sheet data into a pandas dataframe
2) searched for the drive folder that will hold our text files
3) listed the current files in that folder

TO DO
4) write each record in the dataframe to the text file, separated by '***********************************'
5) upload the file to google drive


Here's stackoverflow code for v2 javascript, can use as pseudocode

function saveToTextfile() {
  var ss = SpreadsheetApp.getActive();
  var sheet = ss.getActiveSheet();
  var range = sheet.getRange(1, 1, sheet.getLastRow(), sheet.getLastColumn());
  var rows = range.getValues();
  var folder = DriveApp.getFoldersByName("folderName").next();
  var files = folder.getFiles();
  while(files.hasNext()) files.next().setTrashed(true);
  rows.forEach(function(row, index) {
    folder.createFile("row" + index + ".txt", row.join(", "));
  });
}
'''

# 0. define query ######################################################################
# QUERY STRING EXAMPLES
# https://developers.google.com/drive/api/v3/search-files#query_string_examples
folder_name = 'Conferences'
folder_query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder'"

# 1. CONNECT / AUTHORIZE ---------------------------------------------------------------
# authorize google, for google sheets and google drive
SHEETS, DRIVE = authorize_google(**conf_gs)

# 2. INPUT DATA -------------------------------------------------------------------------
# download catalog data from GoogleSheets to dataframe
data = get_sheet_data(SHEETS, **conf_gs)
# data to df
df = pd.DataFrame(data)
df = df.rename(columns=df.iloc[0]).drop(df.index[0])
# print(df)

# create mask, all columns you want to ignore
mask = df.iloc[0].isin([None, ''])
# the ~ means reverse it
df = df.loc[:, ~mask]
df.drop(df.index[0:2], inplace=True)
print(df)

quit()

# 3. OUTPUT DATA ------------------------------------------------------------------------
# find current output text files (if exist)
# search for the folder of interest and get its ID
folder_id = get_drive_items(DRIVE, folder_query)

# if len(folder_id) < 0:
#     print('folder not found, check folder name variable...')
#     quit()
# elif len(folder_id) > 0:
#     print('folder name is not unique, check google drive...')
#     quit()
# else:
#     print(f'Found folder {folder_id[-1]}')

if folder_id is None:
    quit()

# if found, then create query to find files in that folder
files_query = f"'{folder_id[0]}' in parents"

# get files
directory_files = get_drive_items(DRIVE, files_query, flag_type='file')
print(directory_files)


