# to properly delete nodes you must delete constraints and indexes
all = """
    MATCH(n) DETACH DELETE n;
"""

node = """
    MATCH(n) WHERE {node} IN labels(n) DETACH DELETE n;
"""

pattern = """
    match (n) where ANY(l in labels(n) WHERE l =~ {pattern})
    detach delete n;
"""

# this is a method to delete all indexes and constraints
# 3rd param (true) drops all (since 1st 2 maps are empty) indexes and constraints
reset_indexes = """
    CALL apoc.schema.assert({},{},true) 
    YIELD label, key
    RETURN *;
"""

relationships = """
    match()-[r]-() DETACH DELETE r;
"""