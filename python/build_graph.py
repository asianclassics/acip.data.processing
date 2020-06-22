import os
from dotenv import load_dotenv
from python.functions.graph import load_data
from python.functions.graph import create_indexes
from python.functions.graph.create_relationships import create_relationships
from python.classes import GraphConnector

# CONNECT ----------------------------------------------------------
# load env
load_dotenv()

# connect to graph --------------------------------
graph = GraphConnector({
    "uri": os.environ.get("do_uri"),
    "password": os.environ.get("password"),
    "user": os.environ.get("do_user"),
    "encrypted": False
})


def build_graph():

    # --------------------------------------------------
    # build translations csv from texts and csv metadata
    # once built, you don't need to run it anymore
    # collect_translations()

    # build graph ------------------------------------
    load_data(graph, batch_size=100)
    create_indexes(graph)
    create_relationships(graph)
    graph.close()
    # --------------------------------------------------


if __name__ == "__main__":
    build_graph()

