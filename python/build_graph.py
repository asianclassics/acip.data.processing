from python.functions import load_data, create_indexes, create_relationships
from python.classes import GraphConnector
from python.config import conf_neo4j

# CONNECT ----------------------------------------------------------
# connect to graph --------------------------------
graph = GraphConnector({
    "uri": conf_neo4j["uri"],
    "password": conf_neo4j["password"],
    "user": conf_neo4j["user"],
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
    print(graph)
    quit()
    build_graph()

