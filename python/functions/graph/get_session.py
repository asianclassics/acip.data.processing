import os 
from neo4j import CypherError, ServiceUnavailable
from python.functions.graph import run_transaction_function
from python.classes import GraphConnector


# create the graph object, then

def write_data(graph, query, **kwargs):
    with graph._driver.session as tx:
        try:
            # run transaction function
            tx.write_transaction(run_transaction_function, query, kwargs)
            tx.success = True
        except CypherError as e:
            tx.success = False
            print(f'CypherError {e}')
            raise
        # You should capture any errors along with the query and data for traceability
        except ServiceUnavailable as e:
            tx.success = False
            # logging.error(f"{kwargs['query']} raised an error: \n {e}")
            print(f'ServiceUnavailable {e}')
            raise
