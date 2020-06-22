import os 
from neo4j import CypherError, ServiceUnavailable, unit_of_work
from transaction_function import run_transaction_function


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
