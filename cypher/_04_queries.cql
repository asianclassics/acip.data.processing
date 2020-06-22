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
match (a:Author)-[:IS_CREATOR]->(w:Work)
where size((a)-[:IS_CREATOR]->()) > 10
RETURN a.author_tib, a.author_eng, count(w) as number_of_works
ORDER BY number_of_works desc

// find works that are assigned more than 1 author
match (a:Author)-[:IS_CREATOR]->(w:Work)
where size((w)-[:IS_CREATOR]-()) > 1
return w, a


// find nodes with duplicate properties
// here we're looking for works with dupe titles (using tib and eng)
match (w:Work)
with w.title_tib as tibetan, w.title_eng as english, collect(w) as nodelist, count(*) as count
where count > 1
return count, tibetan, english
order by count desc;


MATCH (n:Person)
MERGE (c:Company {name: TOLOWER(SPLIT(n.slug, '@')[1])})
CREATE (n)-[:AT]->(c);

MATCH (n:Work)
MERGE (s:Sub {subject_tib: SPLIT(n.subject_tib, ';')})
WITH s, n
UNWIND s.subject_tib as subj
MATCH(t:Topic {topic_tib: replace(subj[0],"/","")})
MERGE (n)-[:HAS_SUBJECT]->(t);

MATCH (n:Work)
with SPLIT(n.subject_tib, ';') as s, n
UNWIND s as subj
WITH distinct subj
MERGE(t:Subject {subject_tib: subj})
MERGE (n)-[:HAS_SUBJECT]->(t);


match(p:Person)-[:IS_CREATOR]->(w:Work)-[:HAS_SUBJECT]->(t:Topic)
match(w)-[:HAS_INSTANCE]->(i:Item)-[:HAS_DIGITAL_ASSET]->(d:Digital_Asset)
return p, w, t, i, d;

// ----------------------------------------------
//This relates to creating nodes from subject paths
//converting properties representing file paths to tree structure
//https://community.neo4j.com/t/convert-properties-representing-file-paths-to-tree-structure/10509/5
//We use an APOC function to get the indexes of all slashes in the string
//(this gets us a list of indexes), then we use an extract on that list to get us
//the substring from the start of the path to the given index, and we make sure we
//add the full path at the end:
//
//WITH "path/to/the/thing.txt" as path
//WITH path, apoc.text.indexesOf(path, "/") as delimiters
//WITH path, [del in delimiters | substring(path, 0, del)] + path as paths
//RETURN paths
//This results in: ["path", "path/to", "path/to/the", "path/to/the/thing.txt"]
//Now that you have the absolute path to each node, you can MERGE the
//nodes (with a FOREACH), and then MERGE the relationships between each node.
//
//To avoid creating duplicates, you can use apoc.coll.pairsMin() on the nodes to
//get you a list of list pairs of adjacent nodes in the list, then UNWIND that and
//MERGE the relationships between.
// ----------------------------------------------
match(t:Topic)
unwind t.topic_eng as path
with path, apoc.text.indexesOf(path, "/") as delims
with path, [d in delims | substring(path, 0, d)] + path as paths
return paths