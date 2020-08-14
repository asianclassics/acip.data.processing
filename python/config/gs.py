# GOOGLE SHEETS
conf_gs = {
    "scope": ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'],
    "credentials": {
        "nlm": "config/credentials_nlm1.json",
        "nlm2": "config/credentials_nlm2.json",
    },
    "workbooks": {
        "mappings": {
            "key": "1P99VMc_61PNm9FCOSZo1sQvXQNUanJozV4ZTm3kxhWo",
            "normalized_accession": "1SLgnUq4ohrAODB-XNQ6oiVqQxxJmeR0IQPozSpW6xiw",
            "key_2": "185xp01hElVt35kHO5G_l4baXe5nz4yT1lMhTd0Ilg1k",
            "text_file_folder": "1aL-KxTspsyMBYT2-eKdAXVOCu1UJvx8l",
            "sheet_name": "Uuree-ACIP-Title-Level-Catalog"
        },
        "key": {
            "key": "1hPqe-Y2TWwMTAxIEXYvc8du_GMFUJQNPvZbJou7veAY",
        },
        "accessions": {
            "key": "1SLgnUq4ohrAODB-XNQ6oiVqQxxJmeR0IQPozSpW6xiw",
            "sheet_name": "<Munkhnyam> ACIP-Title-Level-Catalog"
        }
    },
    "collections": {
        "c1": "Works_1",
        "c2": "Works_2"
    },
    "starting_worksheet_name": "Branch_0",
    "worksheet_backup": "Backup",
    "read_mapping": "Mapping",
    "read_NLM_2": "BDRC links",
    "write_sheet_name": "RecursiveWorksNLM2",
    "existing_sheet_data": "___RecursiveWorks"
}

# primary keys in relevant google sheets, to be used to delete rows where that column is empty
p_keys_gs = {
    'SingleVolume': 'Work_RID',
    'MultiVolume': 'WorkRID',
    'Links': 'Work',
    'batch1': 'Work_RID',
    'Uuree': 'NLM_Catalog_#',
    'Munkhnyam': 'NLM_Catalog_#'
}

target_columns = [
    'nlm_catalog',
    'input_file_number',
    'languages_of_the_main_text',
    'other_languages_in_the_main_text',
    'full_title',
    'authors_name',
    'dates_of_the_author',
    'translator',
    'dates_of_the_translator',
    'editor',
    'dates_of_the_editor',
    'year_of_this_edition',
    'format_of_the_book',
    'cover_type',
    'condition_of_book',
    'readability_of_book',
    'volume',
    'page_numbers',
    'size_of_printed_area',
    'size_of_pages',
    'text_format',
    'publisher',
    'copyright_owner',
    'location_of_printing',
    'colophon'
]

minimal_target_columns = [
    'nlm_catalog',
    'input_file_number',
    'languages_of_the_main_text',
    'full_title',
    'authors_name',
    'page_numbers',
    'text_format',
    'colophon'
]