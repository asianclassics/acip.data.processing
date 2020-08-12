from python.config import conf_gs
from python.functions import authorize_google, get_sheet_data, create_page_numbers, get_drive_items
from pandas import DataFrame
import os
from googleapiclient.http import MediaFileUpload

# params ------------------------------------------------------
threshold = 0.99
test = True
flag_drive_upload = False
title_catalog_worksheets = []

# 1. Connectors ##################################
# connect to GS -----------------------------------------------
# authorize google, for google sheets and google drive
SHEETS, DRIVE = authorize_google(**conf_gs)


# 2. INPUT DATA -------------------------------------------------------------------------
# download catalog data from GoogleSheets to dataframe
title_catalog_worksheets, final_data = get_sheet_data(SHEETS, test=True, **conf_gs)

print(f"Title Catalogs: {title_catalog_worksheets}")

print(f"Final table has shape: {final_data.shape[0]}, {final_data.shape[1]} "
      f"and is type {isinstance(final_data, DataFrame)}")


# add pages --------------------------------------------------------
altered_data = create_page_numbers(final_data)
print(altered_data)
print(f"Writing table to MySQL: {altered_data.name} ({len(altered_data)} records)")


# 4. load into DRIVE -----------------------------------------------
folder_name = 'NLMCatalog_TextFiles'
driveId = "0AEv34UqlfkRPUk9PVA"  # TECH share drive
folder_query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder'"
upload_text_file_name = 'mongolia_catalog_altered'

folder_id = get_drive_items(DRIVE, folder_query, driveId)
if folder_id is None:
    quit()

print(folder_id)

# write the data frame to Google Drive
output_file = os.path.join(os.path.dirname(__file__), f"../data/{upload_text_file_name}.txt")
with open(output_file, 'w', encoding='utf-8') as outfile:
    for row_idx, row in enumerate(altered_data.itertuples(index=False, name='CatalogItem')):
        for idx, x in enumerate(row):
            outfile.write(f"{altered_data.columns[idx]}: {x}\n")
        outfile.write('\n=======================================================\n')
        # print(f'Writing row {row_idx}\r', end="")
        print("Progress {:2.1%}".format(row_idx / 10), end="\r")

if flag_drive_upload:
    # copy to drive
    file_metadata = {
        'name': f'{upload_text_file_name}.txt',
        'mimeType': 'text/plain',
        'parents': folder_id
    }

    media = MediaFileUpload(output_file, resumable=True)
    file = DRIVE.files().create(
        body=file_metadata,
        media_body=media,
        fields='id',
        supportsAllDrives=True
    ).execute()
    print(f"\nUploaded {upload_text_file_name}.txt with fileId: {file.get('id')}")
# #########################################################

# CLOSE CONNECTION -------------------------------------------------

# #########################################################

# gs_instance.write_listing(data=altered_data, ws='This_One', header=altered_data.columns)

# print(altered_data)
