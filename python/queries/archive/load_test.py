from neo4j import ServiceUnavailable
import logging

def load_test(tx, csv):
    print(csv)
    query = """
        LOAD CSV WITH HEADERS FROM $csv as row FIELDTERMINATOR ","
        CREATE (:TestAuthor {
            id: row.recID,
            author_eng: row.primaryNameEng,
            author_tib:	row.primaryNameTib,
            author_skt: row.primaryNameSkt,
            author_dates: row.Dates
        });
    """

    try:
        return tx.run(query, csv=csv)
    
    # You should capture any errors along with the query and data for traceability
    except ServiceUnavailable as exception:
        logging.error(f"{query} raised an error: \n {exception}")
        raise
