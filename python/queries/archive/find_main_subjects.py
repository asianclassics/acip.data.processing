def find_main_subjects(tx, limit):
    query = """
        MATCH (t:Topic)<-[:HAS_SUBJECT]-(w:Work)
        where size(()-[:HAS_SUBJECT]->(t)) > $limit
        RETURN distinct(t);
    """
    return tx.run(query, limit=limit)
