from neo4j import ServiceUnavailable
import logging

def load_etexts(tx, csv):
    print(csv)
    query = """
        MATCH (n:TestWork)
        DETACH DELETE n;

        LOAD CSV WITH HEADERS FROM $csv as row FIELDTERMINATOR ","
        CREATE (:TestWork {
            cat_ref:row.catRef,
            cat_number:row.newCatNo,
            title_eng: row.titleEng,
            title_tib: row.titleTib,
            title_tib_brief: row.titleTibBrief,
            title_skt: row.titleSkt
            });
    """
    try:
        res = tx.run(query, csv=csv)
        res.consume()
        return print(res.summary().counters)
    
    # You should capture any errors along with the query and data for traceability
    except ServiceUnavailable as exception:
        logging.error(f"{query} raised an error: \n {exception}")
        raise