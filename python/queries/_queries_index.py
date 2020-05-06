# CREATE INDEX ON :Transliteration(cat_ref);

# currently cannot name indexes? as opposed to docs:
# https://neo4j.com/docs/cypher-manual/current/administration/indexes-for-search-performance/#administration-indexes-create-a-single-property-index

delete = """
    CALL apoc.schema.assert({},{},true) YIELD label, key RETURN *;
"""

work = """
    CREATE INDEX ON :Work(cat_ref);
"""

item = """
    CREATE INDEX ON :Item(cat_ref);
"""

subject_constraint = """
    CREATE CONSTRAINT ON (t:Topic) ASSERT t.subject_tib IS UNIQUE;
"""

person_constraint = """
    CREATE CONSTRAINT ON (p:Person) ASSERT p.author_tib IS UNIQUE;
"""