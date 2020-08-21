from python.config import conf_gs, conf_es
from elasticsearch import helpers, Elasticsearch
from operator import itemgetter
from python.functions import authorize_google, get_sheet_data, \
    create_page_numbers, get_drive_items, text_output_to_single_file, dataframe_doc_generator
from pandas import DataFrame
import os
from googleapiclient.http import MediaFileUpload

# params ------------------------------------------------------
threshold = 0.99
# flags
output_type = 'elastic'  # drive, elastic options
flag_test = False
# vars
title_catalog_worksheets = []
df_sort_key = 'nlm_catalog'

output_data_folder = os.path.join(os.path.dirname(__file__), "../data")
upload_text_file_name = 'mongolia_catalog_altered'
output_file_path = os.path.join(os.path.dirname(__file__), f"../data/{upload_text_file_name}.txt")

protocol, user, secret, host, port = itemgetter(
        'protocol', 'user', 'secret', 'host', 'port')(conf_es['cloud'])

# 1. Connectors ##################################
# connect to GS -----------------------------------------------
# authorize google, for google sheets and google drive
SHEETS, DRIVE = authorize_google(**conf_gs)


# 2. INPUT DATA -------------------------------------------------------------------------
# download catalog data from GoogleSheets to data frame
title_catalog_worksheets, final_data = get_sheet_data(SHEETS, test=flag_test, **conf_gs)

final_data.sort_values(df_sort_key)

print(f"Title Catalogs: {title_catalog_worksheets}")

print(f"Combined tables have shape: {final_data.shape[0]}, {final_data.shape[1]} "
      f"and is type data frame {isinstance(final_data, DataFrame)}")


# add pages --------------------------------------------------------
altered_data = create_page_numbers(final_data)
# print(altered_data)
# print(f"Writing table to MySQL: {altered_data.name} ({len(altered_data)} records)")

# PROPER WAY to get BDRC IIIF url would be to use our GenerateDocument class
# but BDRC schema has changed, so must update before using
# print(altered_data['bdrc_id'].iloc[10])
# b = GenerateDocument(altered_data['bdrc_id'].iloc[10], conf_bdrc, 1, 1, fetch_iiif=True)
# print(b.document)
# quit()

altered_data.to_csv(os.path.join(output_data_folder, "test_output.csv"))

if output_type == 'drive':
    print(f"Sending to google drive...")
    # 4. load into DRIVE -----------------------------------------------
    drive_folder_name = 'NLMCatalog_TextFiles'
    driveId = "0AEv34UqlfkRPUk9PVA"  # TECH share drive
    folder_query = f"name = '{drive_folder_name}' and mimeType = 'application/vnd.google-apps.folder'"

    folder_id = get_drive_items(DRIVE, folder_query, driveId)
    if folder_id is None:
        quit()

    print(folder_id)

    # write the data frame to a text file
    if not text_output_to_single_file(altered_data, output_file_path):
        print('problem creating text file')
        quit()

    if not flag_test:
        # copy to drive
        file_metadata = {
            'name': f'{upload_text_file_name}.txt',
            'mimeType': 'text/plain',
            'parents': folder_id
        }

        media = MediaFileUpload(output_file_path, resumable=True)
        file = DRIVE.files().create(
            body=file_metadata,
            media_body=media,
            fields='id',
            supportsAllDrives=True
        ).execute()
        print(f"\nUploaded {upload_text_file_name}.txt with fileId: {file.get('id')}")

elif output_type == 'elastic':
    print(f"Sending to elastic...")
    es_url = f"{protocol}://{user}:{secret}@{host}:{port}"
    es = Elasticsearch([es_url])
    try:
        helpers.bulk(
            es,
            dataframe_doc_generator(altered_data),
            chunk_size=1000
        )
    except helpers.BulkIndexError as bulk_e:
        print(f"Bulk error {bulk_e}")
        pass
    except helpers.errors as e:
        print(e)
        pass
# #########################################################

# CLOSE CONNECTION -------------------------------------------------

# #########################################################

# gs_instance.write_listing(data=altered_data, ws='This_One', header=altered_data.columns)

# print(altered_data)
