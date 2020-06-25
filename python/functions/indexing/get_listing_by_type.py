from python.classes import BXml


# -------------------------------------------------------------------------------------------------
# take an array, sort and unique-fy
# -------------------------------------------------------------------------------------------------
def make_unique(listing):
    full_listing = sorted(listing)
    unique_listing = []
    for n, item in enumerate(full_listing):
        if item not in full_listing[n + 1:]:
            unique_listing.append(item)

    return unique_listing


# -------------------------------------------------------------------------------------------------
#
# -------------------------------------------------------------------------------------------------
def get_listing_by_type(get_type, elastic_instance, instance=None, file=None, gs_key=None, es_index_version="v4",
                        filter_by_collection=None, filter_by_distance=None):

    listing = []

    if instance is None:
        instance = elastic_instance
    if get_type == 'xml':
        listing = BXml(file).get_listing()
    elif get_type == 'gs':
        listing = instance.get_listing(ws=gs_key)
    elif get_type == 'resources':
        listing = instance.get_listing(es_index_version, node="_resources", filter_by_collection=filter_by_collection,
                                       filter_by_distance=filter_by_distance)

    print(f"New listings: {len(listing)}, {listing}")
    # get rid of I's (we don't actually use this type)
    listing = [x for x in listing if x[0] != 'I']
    print(f"Excluding the I (items) BDRC type >> {len(listing)}")

    existing_listing = elastic_instance.get_listing(es_index_version)
    print(f"Current ElasticSearch index of {len(existing_listing)} items, {existing_listing}")

    # find new listings not already indexed in ES
    new_listing = [x for x in listing if x not in existing_listing]

    if len(new_listing) > 0:
        print(f"To be indexed: {len(new_listing)} items, {new_listing}")

    return [new_listing, existing_listing]
