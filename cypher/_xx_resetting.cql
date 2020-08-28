// queries to reset ----------------------------------------

// APOC
// 3rd param (true) drops all (since 1st 2 maps are empty) indexes and constraints
CALL apoc.schema.assert({},{},true) 
YIELD label, key
RETURN *;

MATCH (n) DETACH DELETE n;
