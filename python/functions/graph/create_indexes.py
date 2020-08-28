from neo4j import unit_of_work
from neo4j.exceptions import ServiceUnavailable, CypherSyntaxError
from python.queries import index


@unit_of_work(timeout=25, metadata={'name': 'load data'})
def run_transaction_function(tx, query, **kwargs):
    results = tx.run(query, **{k: v for k, v in kwargs.items() if v is not None})
    print(results.summary().counters)
    return results.consume()


def create_indexes(graph):
    with graph.driver.session() as tx:
        try:
            tx.write_transaction(run_transaction_function, index.delete)
            tx.write_transaction(run_transaction_function, index.work)
            tx.write_transaction(run_transaction_function, index.item)
            tx.write_transaction(run_transaction_function, index.person_constraint)
            tx.write_transaction(run_transaction_function, index.subject_constraint)
            tx.success = True
        except CypherSyntaxError as e:
            tx.success = False
            print(f'CypherSyntaxError {e}')
            raise
        # You should capture any errors along with the query and data for traceability
        except ServiceUnavailable as e:
            tx.success = False
            # logging.error(f"{kwargs['query']} raised an error: \n {e}")
            print(f'ServiceUnavailable {e}')
            raise
