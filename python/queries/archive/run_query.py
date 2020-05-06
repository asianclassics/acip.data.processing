from neo4j import ServiceUnavailable
import logging

def run_query(tx, query, **kwargs):
    print(query, tx)
    try:
        res = tx.run(query, **{k: v for k, v in kwargs.items() if v is not None})
        # res.consume()  # do i need to call this explicitly?
        print(res.summary().counters)
        return [print(f"BATCH: {r['batch']}\nOPERATIONS:{r['operations']}") for r in res]

        #return print(res.summary().counters)

    
    # You should capture any errors along with the query and data for traceability
    except ServiceUnavailable as exception:
        logging.error(f"{kwargs['query']} raised an error: \n {exception}")
        raise

def run_transaction_function(tx, query, rel):
    return tx.run(query, rel=rel)