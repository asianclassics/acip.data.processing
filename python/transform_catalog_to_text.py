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
'''

# QUERY STRING EXAMPLES
# https://developers.google.com/drive/api/v3/search-files#query_string_examples
folder_name = 'Conferences'
folder_query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder'"

# authorize google, for google sheets and google drive
sheets_service, drive_service = authorize_google(**conf_gs)

# get sheet data
data = get_sheet_data(sheets_service, **conf_gs)
# data to df
df = pd.DataFrame(data)
df = df.rename(columns=df.iloc[0]).drop(df.index[0])
print(df)


# search for the folder of interest and get its ID
folder_id = get_drive_items(drive_service, folder_query)
if len(folder_id) != 1:
    print('folder not found')
    quit()


# if found, then create query to find files in that folder
files_query = f"'{folder_id[0]}' in parents"

# get files
directory_files = get_drive_items(drive_service, files_query)





