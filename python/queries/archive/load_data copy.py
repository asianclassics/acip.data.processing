import os 
from neo4j import CypherError
from queries.run_query import run_query
from queries._queries_delete import q_delete_pattern
from queries._queries_load_apoc import q_load_authors, q_load_works, q_load_items

base_uri = 'http://104.248.221.150/csv'

csv_etexts = 'etext_with_headers.csv'
csv_authors = 'etext_authors_with_headers.csv'


def load_data(graph, batchsize=1000):
    with graph._driver.session() as session:
        try:
            tx = session.begin_transaction()
            # run_query(tx, q_delete_pattern, pattern="Test.*")
            run_query(tx, q_load_authors, csv=os.path.join(base_uri, csv_authors), bsize=200)
            run_query(tx, q_load_works, csv=os.path.join(base_uri, csv_etexts), bsize=batchsize)
            run_query(tx, q_load_items, csv=os.path.join(base_uri, csv_etexts), bsize=batchsize)
            #tx.commit()
            tx.success = True
        except CypherError as e:
            tx.success = False
            print(f'CypherError {e}')