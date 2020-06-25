import json
import copy
from socket import timeout
from http.client import IncompleteRead
import logging
from urllib import error, request


# -------------------------------------------------------------------------------------------------
# CLASS: GENERATE DOCUMENT
# from the generate_acip_schema package
# git+https://github.com/joelcrawford/generate_acip_schema@master
# -------------------------------------------------------------------------------------------------
class GenerateDocument:
    def __init__(self, doc_number, config, distance, version, collection=2,  fetch_iiif=False):
        self.update_document_with_iiif = fetch_iiif
        self.doc_number = doc_number
        self.id = self.get_id()
        self.id_acip = doc_number if doc_number.split(":")[0] == "bdr" else f"bdr:{doc_number}"
        self.config = config
        self.metadata = {"distance": distance, "collection": collection, "index_version": version}
        self.index_name = self.assign_index()
        self.document = self.get_updated_document()

    # -------------------------------------------------------------------------------------------------
    # Get document ID, remove the BDR: prefix if it exists
    # -------------------------------------------------------------------------------------------------
    def get_id(self, doc_number=None):
        if doc_number is None:
            doc_number = self.doc_number
        return doc_number.split(":")[1] if doc_number.split(":")[0] == "bdr" else doc_number

    # -------------------------------------------------------------------------------------------------
    # Load JSON document, as it is
    # -------------------------------------------------------------------------------------------------
    def get_document(self):
        return self.load_document(_id=self.id)

    # -------------------------------------------------------------------------------------------------
    # Load JSON document
    # And alter schema to ACIP model
    # 1. update_document: deals with BDRC @graph node with sub-nodes
    # 2. walk_document: recursive walk through document to get listing of associated ID's
    # 3. add_nodes_to_document: add additional nodes (pre-process) to document to accommodate UI / Search
    # -------------------------------------------------------------------------------------------------
    def get_updated_document(self):

        temp_doc = self.load_document(_id=self.id)
        document = self.update_document(temp_doc)

        # there's probably a better way to do this...
        dupe_doc = copy.deepcopy(document)
        [updated_document, full_listing] = self.walk_document(document, dupe_doc)
        del temp_doc, dupe_doc

        return self.add_nodes_to_document(updated_document, full_listing)

    # -------------------------------------------------------------------------------------------------
    # Add nodes to document before indexing
    #   -- make set from listing // _resources //
    #   -- set distance // _distance // from original NLM document,
    #   ---- NLM work is 0 > related doc is 1 > found in related doc is 2, etc
    #   -- set collection // _collection // which NLM collection, 1: previous project years, 2: current
    #   -- manifest URL // _manifestURL // link to BDRC manifest for IIIF scans
    #   -- first image // _firstImageURL // link to the actual JPG image for first page of scans
    # -------------------------------------------------------------------------------------------------
    def add_nodes_to_document(self, document, listing):

        document['_resources'] = self.get_related_ids(listing)
        document["_distance"] = self.metadata["distance"]
        document["_collection"] = self.metadata["collection"]
        document["_bdrc_id"] = self.id

        if 'workHasItem' in document:
            if self.update_document_with_iiif:
                iiif = self.get_iiif(document)
                if iiif:
                    document['_manifestURL'] = iiif["manifestURL"]
                    document['_firstImageURL'] = iiif["imageURL"]

        if 'skos:prefLabel' in document:
            document['_label'] = self.inject_pref_label(document['skos:prefLabel'])

        return document

    # -------------------------------------------------------------------------------------------------
    # Get both the manifest and first image URL
    # -------------------------------------------------------------------------------------------------
    def get_iiif(self, document):
        iiif = {}
        manifest = self.load_manifest(document['workHasItem'])
        first_image = self.load_first_image_url(manifest)

        if manifest or first_image:
            iiif = {"manifestURL": manifest, "imageURL": first_image}

        return iiif

    # -------------------------------------------------------------------------------------------------
    # Create a unique listing of related IDs for a given document
    # -------------------------------------------------------------------------------------------------
    def get_related_ids(self, related_items_list=None):
        if related_items_list is None:
            full_listing = sorted(self.walk_document(self.document))
        else:
            full_listing = sorted(related_items_list)
        unique_listing = []
        for n, item in enumerate(full_listing):
            if item not in full_listing[n + 1:]:
                unique_listing.append(item)

        return unique_listing

    # -------------------------------------------------------------------------------------------------
    # Assign an index name based on type of document
    # W, work // I, Item // P, Person // G, Geography // T, Topic (Subject)
    # note: this is an example of switch case in python
    # -------------------------------------------------------------------------------------------------
    def assign_index(self):
        key = self.id[0]
        index_name = f"v{self.metadata['index_version']}{self.config['es_index_prefix']}"
        return {
            'W': index_name + "work",
            'I': index_name + "item",
            'P': index_name + "person",
            'G': index_name + "geography",
            'T': index_name + "topic"
        }.get(key, "invalid")

    # -------------------------------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------------------------------
    def load_document(self, _id=None, req_obj=None):
        document = None
        making_some_attempts = 0
        _id = self.id if _id is None else _id
        req = self.config["endpoint"] + _id + self.config["file_type"] if req_obj is None else req_obj

        while making_some_attempts < 10:
            try:
                document = json.load(request.urlopen(req))
                making_some_attempts = 10
            except IncompleteRead as Incomplete_error:
                logging.error(f"{_id} // error during chunk read {Incomplete_error}")
                making_some_attempts += 1
                continue
            except timeout as Timeout_error:
                logging.error(f"{_id} // socket timeout {Timeout_error}")
                making_some_attempts += 1
                continue
            except error.HTTPError as HTTP_error:
                logging.error(f"{_id} // error during url request {HTTP_error.code}")
                making_some_attempts += 1
                continue
            except error.URLError as URL_error:
                logging.error(f"{_id} // error during url request {URL_error}")
                making_some_attempts += 1
                continue
            except request.ConnectionResetError as Reset_error:
                logging.error(f"{_id} // error during request {Reset_error}")
                making_some_attempts += 1
                continue
            break

        return document

    # -------------------------------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------------------------------
    def get_root_on_graph(self, graph, doc_number=None):
        if doc_number is None:
            doc_number = self.id
        try:
            root_index = [x['@id'] for x in graph].index(f"bdr:{doc_number}")
            return graph[root_index]
        except ValueError:
            # root_index = -1
            return graph

    # -------------------------------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------------------------------
    def update_document(self, document):
        updated_document = {}
        if document is not None:
            if '@id' in document:
                if document['@id'] == f"bdr:{self.id}":
                    return document

            if '@graph' in document:
                graph = document['@graph']
                updated_document = self.get_root_on_graph(graph)

                try:
                    author_index = [x['type'] for x in graph].index("AgentAsCreator")
                except ValueError:
                    author_index = -1

                if author_index > -1:
                    if 'agent' in graph[author_index]:
                        updated_document['_creator'] = graph[author_index]['agent']['@id']

                try:
                    notes = [item['noteText'] for item in graph
                             if item.get('type') and item.get('noteText') and item['type'] == 'Note']

                except ValueError:
                    notes = []

                if len(notes) > 0:
                    updated_document['_notes'] = notes

        return updated_document

    # -------------------------------------------------------------------------------------------------
    # walking the document alters document itself
    # deepcopy (orig_doc) passed in to function...what's best practice for this?
    # -------------------------------------------------------------------------------------------------
    def walk_document(self, node, orig_doc, results_listing=None, current_key=None):
        if current_key != '@id':
            if results_listing is None:
                results_listing = []
            # if node is a dictionary
            if isinstance(node, dict):
                for key, item in node.items():
                    if key != '@id':
                        # if value is also a dict or list, recurse
                        if isinstance(item, (dict, list)):
                            self.walk_document(item, orig_doc, results_listing=results_listing, current_key=key)
                        else:
                            if item != self.id_acip:

                                if self.test_for_identifier(item):
                                    results_listing.append(item)

                                    if self.test_for_identifier(item, interest=self.config["indices_to_denormalize"]):
                                        orig_doc[key] = self.denormalize(item)
                                        # print(item, key, node)

            # if node is a list
            elif isinstance(node, list):
                current_list = []

                for i, n in enumerate(node):
                    # if value is a dict or list, recurse
                    if isinstance(n, (dict, list)):
                        self.walk_document(n, orig_doc, results_listing=results_listing)
                    else:
                        if n != self.id_acip:

                            if self.test_for_identifier(n):
                                results_listing.append(n)

                                if self.test_for_identifier(n, interest=self.config["indices_to_denormalize"]):
                                    current_list.append(self.denormalize(n))
                if len(current_list) > 0 and current_key in orig_doc:
                    orig_doc[current_key] = current_list
                    # print(current_key, current_list)

            else:
                logging.error(f"Not Iterable {node}")

        return [orig_doc, results_listing]

    # -------------------------------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------------------------------
    def denormalize(self, leaf):
        doc_number = self.get_id(leaf)
        # print(f"check this id: {doc_number}")
        label = None
        document = self.load_document(_id=doc_number)
        if document is not None:
            if '@graph' in document:
                document = self.get_root_on_graph(document['@graph'], doc_number)

            if 'skos:prefLabel' in document:
                # print(doc_number, document['skos:prefLabel'])
                label = self.inject_pref_label(document['skos:prefLabel'], doc_number=doc_number)
            elif 'rdfs:label' in document:
                label = self.inject_pref_label(document['rdfs:label'], doc_number=doc_number)

        return label

    # -------------------------------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------------------------------
    def load_manifest(self, node):

        manifest = None
        doc_number = node.split(":")[1] if node.split(":")[0] == "bdr" else node

        manifest_document = self.load_document(_id=doc_number)

        if 'itemVolumes' in manifest_document and manifest_document is not None:
            if manifest_document['itemVolumes'] == 1:
                if 'itemHasVolume' in manifest_document:
                    manifest = f"{self.config['presentation_endpoint']}/v:{manifest_document['itemHasVolume']}/manifest"
            elif manifest_document['itemVolumes'] > 1:
                manifest = f"{self.config['presentation_endpoint']}/collection/i:{manifest_document['@id']}"

        return manifest

    # -------------------------------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------------------------------
    def load_first_image_url(self, manifest):

        first_image = None
        data = self.load_document(_id=self.id, req_obj=manifest)

        if data is not None:
            # this logic taken directly from BDRC
            if 'sequences' not in data:
                if 'manifests' in data:
                    first_image = self.load_first_image_url(data['manifests'][0]['@id'])

            if 'sequences' in data and data['sequences'][0]['canvases']:
                for i in range(len(data['sequences'][0]['canvases'])):
                    s = data['sequences'][0]['canvases'][i]
                    if s['label'] == "tbrc-1":
                        # data['sequences'][0]['canvases'][2]
                        if s['images'][0]:
                            first_image = s['images'][0]['resource']['@id'].split("/full", 1)[0]

                if data['sequences'][0]['canvases'][0]:
                    s = data['sequences'][0]['canvases'][0]
                    if s['images'][0] and s['images'][0]['resource']['@id']:
                        first_image = s['images'][0]['resource']['@id'].split("/full", 1)[0]

        return first_image

    # -------------------------------------------------------------------------------------------------
    # Test for bdr prefix and schema type
    # -------------------------------------------------------------------------------------------------
    def test_for_identifier(self, s, interest=None):
        if interest is None:
            interest = self.config["indices_of_interest"]
        if type(s) == str:
            if s.split(":")[0] == "bdr":
                if s[4] in interest:
                    if s[5].isdigit():
                        return True

    # -------------------------------------------------------------------------------------------------
    # Add label to document using skos:prefLabel
    # -------------------------------------------------------------------------------------------------
    def inject_pref_label(self, node, doc_number=None):
        label = None
        # if node is a dictionary
        if isinstance(node, dict):
            for key, value in node.items():
                if key == '@value':
                    label = value
        elif isinstance(node, list):
            for item in node:
                if item["@language"] == self.config["language_main"]:
                    label = item["@value"]
                elif item["@language"] == self.config["language_secondary"]:
                    label = item["@value"]
                # if isinstance(item, dict):
                #     label = next((item["@value"] for k, v in item.items()
                #     if v in self.config["languages_main"]), None)

        if doc_number is None:
            # print(f"inject for {node} {label}")
            return label
        else:
            return {'_id': doc_number, '_value': label}
