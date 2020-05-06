from neo4j import GraphDatabase

class GraphDataLoader:
    def __init__(self, query):
        self.query = query

    