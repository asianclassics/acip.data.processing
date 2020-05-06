from neo4j import GraphDatabase
import socket

class GraphConnector:
    def __init__(self, config):
        self.config = config
        self._driver = GraphDatabase.driver(config['uri'], auth=(config['user'], config['password']))
        
    # def connect(self):
    #     return self._driver

    def close(self):
        self._driver.close()
        return print('Connection closed.')


    def read_data(self, query, limit):
        with self._driver.session() as session:
            results = session.read_transaction(query, limit)
            for r in results:
                print(r)

    # def write_data(self, query):
    #     with self._driver.session() as session:
    #         # Using write transactions allow the driver to handle retries and transient errors for you
    #         write_results = session.write_transaction(query, "Alice", "David")
    #         for result in write_results:
    #             print("Create successful: ", result.get("p1"), result.get("p2"))