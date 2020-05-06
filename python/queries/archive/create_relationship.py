from neo4j import ServiceUnavailable
import logging

def create_relationship_between_people(tx, person1_name, person2_name):

    query = """
        MERGE (p1:Person { name: $person1_name })
        MERGE (p2:Person { name: $person2_name })
        MERGE (p1)-[:KNOWS]->(p2)
        RETURN p1, p2
    """

    try:
        return tx.run(query, person1_name=person1_name, person2_name=person2_name)
    
    # You should capture any errors along with the query and data for traceability
    except ServiceUnavailable as exception:
        logging.error(f"{query} raised an error: \n {exception}")
        raise
