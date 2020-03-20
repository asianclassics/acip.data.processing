USING PERIODIC COMMIT 
LOAD CSV WITH HEADERS FROM "file:///acip/etext_with_headers.csv" as row FIELDTERMINATOR ","
MATCH (w:Work {cat_ref: row.catRef})
MATCH (a:Author)
WHERE length(a.author_tib) > 0 and a.author_tib = row.primaryAuthorTib 
MERGE (a)-[:IS_CREATOR]->(w)
WITH w, row
MATCH (s:Subject)
WHERE length(s.subject_tib) > 0 and s.subject_tib = row.subjectTib
MERGE (w)-[:HAS_SUBJECT]->(s);


MATCH (w:Work)
MATCH (t:Transliteration)
WHERE w.cat_ref = t.cat_ref
MERGE (w)-[:HAS_TRANSLITERATION]->(t);