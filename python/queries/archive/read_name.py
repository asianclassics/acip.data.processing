def read_person_by_name(tx, name):
    query = """
        MATCH (p:Person)
        WHERE p.name = $person_name
        RETURN p.name AS name
    """
    return tx.run(query, person_name=name)
