import json
import logging
from itertools import chain
from operator import itemgetter
from elasticsearch import Elasticsearch,  RequestError, TransportError  # ConflictError, NotFoundError, helpers
from elasticsearch_dsl import Search


# -------------------------------------------------------------------------------------------------
# CLASS: ELASTICSEARCH
# from the generate_acip_schema package
# git+https://github.com/joelcrawford/generate_acip_schema@master
# -------------------------------------------------------------------------------------------------
class ElasticSearch:
    def __init__(self, config, env='cloud'):
        self.config = config
        self.doc_type = "_doc"
        self.environment = env
        self.client = self.create_client()

    # -------------------------------------------------------------------------------------------------
    # create ElasticSearch client from config
    # -------------------------------------------------------------------------------------------------
    # def create_client(self):
    #
    #     protocol, user, secret, host, port = itemgetter(
    #         'protocol', 'user', 'secret', 'host', 'port')(self.config['cloud'])
    #
    #     url = f"{protocol}://{user}:{secret}@{host}:{port}"
    #     # [self.config[self.environment]],
    #     return Elasticsearch(
    #         [url],
    #         sniff_on_start=True,
    #         # refresh nodes after a node fails to respond
    #         sniff_on_connection_fail=True,
    #         # and also every 60 seconds
    #         sniffer_timeout=60,
    #         retry_on_timeout=True
    #     )

    def create_client(self):
        protocol, user, secret, host, port = itemgetter(
            'protocol', 'user', 'secret', 'host', 'port')(self.config['cloud'])

        url = f"{protocol}://{user}:{secret}@{host}:{port}"
        return Elasticsearch([url])

    # -------------------------------------------------------------------------------------------------
    # Create index if it does not already exist
    # -------------------------------------------------------------------------------------------------
    def check_index(self, idx):
        if not self.client.indices.exists(idx):
            print(f"Creating index {idx}")
            self.client.indices.create(idx)

    # -------------------------------------------------------------------------------------------------
    # Delete and re-create all indices in a given collection
    # -------------------------------------------------------------------------------------------------
    def recreate_indices(self, es_index_version=""):
        if isinstance(es_index_version, int):
            es_index_version = f"v{es_index_version}"

        wild_card_indices = f"{es_index_version}{self.config['index_prefix']}*"
        target_indices = self.client.indices.get_alias(wild_card_indices)
        for idx in target_indices:
            print(f"Deleting index {idx}")
            self.client.indices.delete(idx)

    # -------------------------------------------------------------------------------------------------
    # Direct index of main works to a FrontEnd index specifically for the UI
    # need to work on how to create this, but for now there's a _resources leaf
    # with all bdr: ID's that that document is related to
    # -------------------------------------------------------------------------------------------------
    def direct_index(self, document, index_name):

        try:
            # print(document)
            if '@id' not in document:
                raise KeyError

            response = self.client.create(
                index=index_name,
                doc_type=self.config["type"],
                body=json.dumps(document),
                id=document['@id']
            )

            if response['result'] != "created":
                print(f"\n{response['result']} for id: {document['@id']}")

        except RequestError as e:
            logging.error(f"Request Error during index {e}")
            pass
        except TransportError as e:
            logging.error(f"Transport Error during index {e}")
            pass
        except KeyError as e:
            logging.error(f"Key Error, @id not present on node, {e}")
            pass

    # -------------------------------------------------------------------------------------------------
    # GET COLLECTION
    # get current list of indexed id's across multiple indices (as defined in config)
    # can either can _id listing or listing from node in JSON
    # for our purposes node '_resources' under '_source' has all ids associated with any given document
    # ** can use collection or distance to filter search
    # -------------------------------------------------------------------------------------------------
    def get_listing(self, index_version, with_prefix=False, node=None, filter_by_collection=None,
                    filter_by_distance=None):
        if isinstance(index_version, int):
            index_version = f"v{index_version}"

        listing = list()

        idx_list = [f"{index_version}_{idx['name']}" for idx in self.config["indices"]]

        for idx in idx_list:
            self.check_index(idx)
            if self.client.indices.exists(idx):
                s = Search(using=self.client, index=idx, doc_type=self.doc_type)

                if filter_by_collection is not None:
                    s = s.filter('term', **{'_collection': filter_by_collection})

                if filter_by_distance is not None:
                    s = s.filter('term', **{'_distance': filter_by_distance})

                if node is None:
                    s = s.source([])  # only get ids, otherwise `fields` takes a list of field names
                    ids = [h.meta.id for h in s.scan()]
                else:
                    try:
                        s = s.source([node])  # only get ids, otherwise `fields` takes a list of field names
                        ids = [list(h[node]) for h in s.scan()]  # possibly don't need to wrap in list here
                        # ids = sum(ids, [])
                        ids = list(chain.from_iterable(ids))

                    except KeyError:
                        print(f"{node} does not exist in _source of index {idx}")
                        continue

                listing = list(set(listing + ids))

        if with_prefix:
            listing = ['bdr:{0}'.format(c) if c[:4] != 'bdr:' else c for c in listing]
        else:
            listing = [c[4:] if c[:4] == 'bdr:' else c for c in listing]

        return sorted(listing)
