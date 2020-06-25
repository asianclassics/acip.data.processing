import os
from dotenv import load_dotenv
load_dotenv()

# ELASTICSEARCH
conf_es = {
    "type": "_doc",
    "indices": [
        {"type": "work", "name": "bdrc_work", "code": "W"},
        {"type": "item", "name": "bdrc_item", "code": "I"},
        {"type": "topic", "name": "bdrc_topic", "code": "T"},
        {"type": "person", "name": "bdrc_person", "code": "P"},
        {"type": "place", "name": "bdrc_geography", "code": "G"}
    ],
    "development": {
        'host': 'localhost',
        'port': 9200
    },
    "index_prefix": "_bdrc_",
    "cloud": {
        'protocol': 'https',
        'host': os.environ['ELASTIC_HOST'],
        'port': os.environ['ELASTIC_PORT'],
        'user': os.environ['ELASTIC_USER'],
        'secret': os.environ['ELASTIC_SECRET']
    }
}
