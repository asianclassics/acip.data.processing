import os 
from neo4j import CypherError, ServiceUnavailable
from python.queries import delete, load
from python.functions import run_transaction_function

base_uri = 'http://104.248.221.150/csv'

topic_path = os.path.join(base_uri, 'subjects_acip.csv')
person_path = os.path.join(base_uri, 'authors_acip.csv')
work_path = os.path.join(base_uri, 'choney_etexts.csv')
stpete_path = os.path.join(base_uri, 'choney_stpete.csv')
aci_path = os.path.join(base_uri, 'aci_translations_with_headers.csv')
acip_path = os.path.join(base_uri, 'acip_translations_with_headers.csv')


# @unit_of_work(timeout=25, metadata={'name': 'load data'})
# def run_transaction_function(tx, query, **kwargs):
#     result = tx.run(query, **{k: v for k, v in kwargs.items() if v is not None})
#     # print(results.summary().statement)
#     print(result.summary().counters)
#     [print(f"BATCH: {r['batch']}\nOPERATIONS:{r['operations']}") for r in result]
#     return result.consume()


def load_data(graph, batch_size=100):
    with graph.driver.session() as tx:
        try:
            tx.write_transaction(run_transaction_function, delete.all)
            tx.write_transaction(run_transaction_function, load.topics, csv=topic_path, bsize=batch_size)
            tx.write_transaction(run_transaction_function, load.persons, csv=person_path, bsize=batch_size)
            tx.write_transaction(run_transaction_function, load.works, csv=work_path, bsize=batch_size)
            tx.write_transaction(run_transaction_function, load.items, csv=work_path, bsize=batch_size)
            tx.write_transaction(run_transaction_function, load.aci_item, csv=aci_path, bsize=batch_size, sep="TAB")
            tx.write_transaction(run_transaction_function, load.aci_item, csv=acip_path, bsize=batch_size, sep="TAB")
            tx.write_transaction(run_transaction_function, load.digital_asset, csv=work_path, bsize=batch_size)
            tx.write_transaction(run_transaction_function, load.aci_digital_asset,
                                 csv=aci_path, bsize=batch_size, sep="TAB")
            tx.write_transaction(run_transaction_function, load.aci_digital_asset,
                                 csv=acip_path, bsize=batch_size, sep="TAB")
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
