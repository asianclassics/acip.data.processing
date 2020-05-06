import os 
from neo4j import unit_of_work

@unit_of_work(timeout=25, metadata={'name': 'load data'})
def run_transaction_function(tx, query, **kwargs):
    results = tx.run(query, **{k: v for k, v in kwargs.items() if v is not None})
    print(results.summary().counters)
    [print(f"BATCH: {r['batch']}\nOPERATIONS:{r['operations']}") for r in results]
    return results.consume()