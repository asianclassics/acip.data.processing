// CREATE RELATIONSHIPS
// note that when I combine these 3 queries into 1 there are orphaned nodes
// whereas running them separately all relationships are successfully created

USING PERIODIC COMMIT 
LOAD CSV WITH HEADERS FROM $fileTexts as row FIELDTERMINATOR ","
MATCH (w:Work {cat_ref: row.catRef})
MATCH (a:Author)
WHERE size(a.author_tib) > 0 and a.author_tib = row.primaryAuthorTib 
MERGE (a)-[:IS_CREATOR]->(w);

USING PERIODIC COMMIT 
LOAD CSV WITH HEADERS FROM $fileTexts as row FIELDTERMINATOR ","
MATCH (w:Work {cat_ref: row.catRef})
MATCH (i:Item {cat_ref: row.catRef})
MERGE (w)-[:HAS_INSTANCE]->(i)
WITH i, row
MATCH (t:Transliteration {cat_ref: row.catRef})
MERGE (i)-[:HAS_DIGITAL_ASSET]->(t);

USING PERIODIC COMMIT 
LOAD CSV WITH HEADERS FROM $fileTexts as row FIELDTERMINATOR ","
MATCH (w:Work {cat_ref: row.catRef})
MATCH (s:Subject)
WHERE size(s.subject_tib) > 0 and s.subject_tib = row.subjectTib
MERGE (w)-[:HAS_SUBJECT]->(s);
