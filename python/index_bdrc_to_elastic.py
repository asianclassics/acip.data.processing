import os
from python.classes import ElasticSearch, GoogleSheets, GenerateDocument
from python.config import conf_es, conf_bdrc, conf_gs, conf_ssh
from python.functions import get_listing_by_type, configure_logger, get_xml

configure_logger()

# Current Directory
current_dir = os.getcwd()

# ES --------------------------------------------------------
environment = "cloud"
es_instance = ElasticSearch(conf_es, environment)

# GS --------------------------------------------------------
# once we've indexed the data, we write the _resources (next branch) to GS for reference
# authorize GS and get workbook
gs_instance = GoogleSheets(conf_gs)
# XML -------------------------------------------------------
# when Travis uploads, run the get_xml function from _utils to download from server
xml_path = get_xml(conf_ssh)
# xml_path = os.path.join(current_dir, 'data', 'synced-202002070015.xml')

# variables -------------------------------------------------
# these vars affect how docs are indexed
# collection: NLM collection (project phase)
# index_version: index name prefix (1 >> v1, etc)
# distance: 0 for NLM works, 1 for associated (from _resources)
# which_collection = 2
# distance = 2
index_version = 1
collections = [2]
distances = [1, 2]

# flags -----------------------------------------------------
INDEX_JSON = True
WORK_TYPE_RESOURCES = True

for collection in collections:
    for distance in distances:
        print(f"\nStarting on collection: {collection} with distance of: {distance}...")
        # indexing ---------------------------------------------------
        # es_instance.recreate_indices(es_index_version=index_version)
        # returns listing of items NOT currently indexed in ES, and ES listing
        # this returns listing of items NOT currently indexed in ES, and ES listing
        quit()
        if WORK_TYPE_RESOURCES:
            [current_listing, es_collection] = get_listing_by_type('resources', es_instance, es_index_version=index_version,
                                                               filter_by_collection=collection,
                                                               filter_by_distance=distance-1)
        else:
            [current_listing, es_collection] = get_listing_by_type('xml', es_instance,
                                                                   file=xml_path, es_index_version=index_version)

        # [current_listing, es_collection] = get_listing_by_type(
        #       'gs', es_instance, instance=gs_instance, gs_key="Works_1")

        if len(current_listing) == 0:
            print(f"Nothing to index for c: {collection} / d: {distance}")
            continue

        print(f"c: {collection} / d: {distance} => {len(current_listing)} {current_listing}")

        # document this round of indexing ---------------------------------
        this_branch = f"Branch_c0{collection}_d0{distance}"
        gs_instance.write_listing(data=current_listing, ws=this_branch)  # write to GS, in case error

        full_listing = []
        for i, d in enumerate(current_listing):
            document_instance = GenerateDocument(d, conf_bdrc, distance, index_version, collection, fetch_iiif=True)

            if INDEX_JSON and document_instance.document is not None and document_instance.index_name is not 'invalid':

                # at some point update the class to split GENERATE and UPDATE document
                # so in here after generating the document you would call UpdateDocument

                es_instance.direct_index(document_instance.document, document_instance.index_name)
                # printing on same line, replacing as it goes, \r goes at beginning
                print("\r Indexing document: {0}, with id: {1}".format(i, document_instance.id), flush=True, end="")

