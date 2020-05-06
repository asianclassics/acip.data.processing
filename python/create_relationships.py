import os 
from neo4j import CypherError, ServiceUnavailable, unit_of_work
from python.queries import rels, delete


@unit_of_work(timeout=25, metadata={'name': 'create relationships'})
def run_transaction_function(tx, query, **kwargs):
    results = tx.run(query, **{k: v for k, v in kwargs.items() if v is not None})
    # print(results.summary().statement)
    print(results.summary().counters)
    return results.consume()


def create_relationships(graph):
    with graph.driver.session() as tx:
        try:
            tx.write_transaction(run_transaction_function, delete.relationships)
            tx.write_transaction(run_transaction_function, rels.person_work)
            tx.write_transaction(run_transaction_function, rels.work_item)
            tx.write_transaction(run_transaction_function, rels.item_digital_asset)
            tx.write_transaction(run_transaction_function, rels.topic_work_temp_by_english)
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
