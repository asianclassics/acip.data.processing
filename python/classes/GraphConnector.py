from neo4j import GraphDatabase


class GraphConnector:
    def __init__(self, config):
        self.config = config
        self.driver = GraphDatabase.driver(
            config['uri'], auth=(config['user'], config['password']), encrypted=config['encrypted'])

    def close(self):
        self.driver.close()
        return print('Connection closed.')
