CREATE INDEX ON :Work(cat_ref);
CREATE INDEX ON :Transliteration(cat_ref);
CREATE INDEX ON :Item(cat_ref);
CREATE CONSTRAINT ON (s:Subject) ASSERT s.subject_tib IS UNIQUE;


// we don't have a subject or author database
// not unique yet.
CREATE CONSTRAINT ON (a:Author) ASSERT a.author_tib IS UNIQUE;

// still not unique
CREATE CONSTRAINT ON (a:Author) ASSERT (a.author_tib, a.author_eng) IS NODE KEY;

