from neo4j import unit_of_work


@unit_of_work(timeout=25)
def run_transaction_function(tx, query, **kwargs):
    result = tx.run(query, **{k: v for k, v in kwargs.items() if v is not None})
    # print(results.summary().statement)
    print(result.summary().counters)
    [print(f"BATCH: {r['batch']}\nOPERATIONS:{r['operations']}") for r in result]
    return result.consume()
