import os
from dotenv import load_dotenv
from python.load_data import load_data
from python.create_indexes import create_indexes
from python.create_relationships import create_relationships
from python.classes import GraphConnector
from neo4j import GraphDatabase
from python.build_translations import collect_translations

# CONNECT ----------------------------------------------------------
# load env variables for AURA connection --------------------------
load_dotenv()

uri = "bolt+routing://206.189.78.105:7687"
graph = GraphDatabase.driver(uri, auth=("neo4j", "4thebenefitof@LL"), encrypted=False)
print(graph)

# connect to graph --------------------------------
graph = GraphConnector({
    "uri": os.environ.get("do_uri"),
    "password": os.environ.get("password"),
    "user": os.environ.get("do_user"),
    "encrypted": False
})


def main():
    # collect_translations()
    # # build graph ------------------------------------
    #
    # # ------------------------------------------------
    load_data(graph, batch_size=100)
    create_indexes(graph)
    create_relationships(graph)

    graph.close()


if __name__ == "__main__":
    main()

