// SUBJECTS -------------------------------------------------
// what subjects have larger number of works transliterated?
// 01. visualize it
MATCH (s:Subject)<-[:HAS_SUBJECT]-(w:Work)
where size(()-[:HAS_SUBJECT]->(s)) > 10
RETURN s, w;

// 02. see a table of results
MATCH (s:Subject)<-[:HAS_SUBJECT]-(w:Work)
where size(()-[:HAS_SUBJECT]->(s)) > 10
RETURN s.subject_eng, count(w) as number_of_works
ORDER BY number_of_works desc

// AUTHORS -------------------------------------------------
// what authors have larger number of works transliterated?
// 01. visualize it
MATCH (a:Author)-[:IS_CREATOR]->(w:Work)
where size((a)-[:IS_CREATOR]->()) > 10
RETURN a, w;

// 02. see a table of results
match (a:Author)-[r:IS_CREATOR]->(w:Work)
where size((a)-[:IS_CREATOR]->()) > 10
RETURN a.author_eng, count(w) as number_of_works
ORDER BY number_of_works desc

// find works that are assigned more than 1 author
match (a:Author)-[r:IS_CREATOR]->(w:Work)
where size((w)-[:IS_CREATOR]-()) > 1
return w, a



