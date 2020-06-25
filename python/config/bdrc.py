# BDRC
conf_bdrc = {
    "indices_of_interest": ["W", "T", "P", "G"],
    "indices_to_denormalize": ["T", "P", "G", "W"],
    "es_index_prefix": "_bdrc_",
    "languages_main": ["en", "bo-x-ewts"],
    "language_main": "bo-x-ewts",
    "language_secondary": "en",
    "endpoint": "http://purl.bdrc.io/resource/",
    "presentation_endpoint": "http://iiifpres.bdrc.io/2.1.1",
    "file_type": ".jsonld",
    "works": [
        "bdr:W22677",
        "bdr:W1GS135873",
        "bdr:W1KG5200",
        "bdr:W22344",
        "bdr:W1GS135531",
        "bdr:W1KG1132",
        "bdr:W1KG10720",
        "bdr:W1KG1279",
        "bdr:W1KG14700"
    ],
    "test_works": [
        "bdr:W14260",
        "bdr:P5061",
        "bdr:P6161",
        "bdr:W14260",
        "bdr:P6161",
        "bdr:W1KG14700"
    ],
    "test_dupes": [
        "bdr:W14260",
        "bdr:P5061",
        "bdr:W14260"
    ]
}
