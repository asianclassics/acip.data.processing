# from generate_acip_schema import ElasticSearch
from elasticsearch import Elasticsearch, RequestError, TransportError, ConflictError
from tests.config.elasticsearch import conf_es
import os
import logging
import tqdm
import base64
from operator import itemgetter


# ES --------------------------------------------------------
environment = "cloud"

# Current Directory
translations_dir = '/Users/joel/PROJECTS/WORK/CURRENT/ACIP/translations/'
aci_parsed_dir = 'aci_parsed/c6'
aci_dir = 'aci'
mixed_nuts = 'mixedNuts'

protocol, user, secret, host, port = itemgetter(
            'protocol', 'user', 'secret', 'host', 'port')(conf_es['cloud'])

config = {
    "url": f"{protocol}://{user}:{secret}@{host}:{port}",
    "dir": os.path.join(translations_dir, aci_parsed_dir),
    "index": "v1_acip_aci",
    "doc_type": "_doc",
    "file_type": "txt",
    "requires_encoding": True
}


def get_data():
    docs = [f for f in os.listdir(config["dir"]) if f.endswith(f".{config['file_type']}")]
    print(f"{len(docs)} translations to index, {docs}")
    number_of_docs = len(docs)
    return docs, number_of_docs


def generate_actions(doc):
    with open(os.path.join(config["dir"], doc), 'rb') as f:
        stream = f.read()

    if config["requires_encoding"]:
        stream = base64.b64encode(stream)

    print(f"\n {doc} is {(len(stream) * 3) / 4} bytes")
    # yield an encoded doc
    return {"data": stream}


def main():

    docs, number_of_docs = get_data()
    # client = ElasticSearch(conf_es, environment)
    client = Elasticsearch([config['url']])

    # progress = tqdm.tqdm(unit="docs", total=number_of_docs)
    # successes = 0
    #
    # for d in docs:
    #     body = generate_actions(d)
    #     try:
    #         response = client.index(
    #             index=config["index"],
    #             doc_type=config["doc_type"],
    #             body=body,
    #             id=d,
    #             params={"pipeline": config["file_type"]}
    #         )
    #
    #         progress.update(1)
    #
    #         if response['result'] != "created":
    #             print(f"\n{response['result']} for id: {d}")
    #
    #     except RequestError as e:
    #         logging.error(f"Request Error during index {e}")
    #         pass
    #     except TransportError as e:
    #         logging.error(f"Transport Error during index {e}")
    #         pass
    #     except ConflictError as e:
    #         logging.error(f"Document already exists {d}, {e}")
    #         pass
    #     except KeyError as e:
    #         logging.error(f"Key Error, @id not present on node, {e}")
    #         pass


if __name__ == "__main__":
    main()

# for ok, result in helpers.streaming_bulk(
#         es_instance,
#         documents(),
#         index="v1_acip_translations",
#         doc_type="_doc",
#         chunk_size=4,
#         params={"pipeline": "docx"}
#         ):
#     action, result = result.popitem()
#     if not ok:
#         print("Failed to index document")
#     else:
#         print("Success!")

