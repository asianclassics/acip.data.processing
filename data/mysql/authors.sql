SELECT 
'primaryNameTib', 'primaryNameSkt', 'primaryNameEng', 'primaryNameLang', 'otherNameTib', 
'otherNameSkt', 'otherNameEng', 'Dates', 'Date-Begin', 'Date-End', 'TranslatedBy', 'TranslatorOf', 
'recID', 'bAuthor', 'bTranslator', 'Notes'
UNION ALL
SELECT `Primary Name-Tibetan`, `Primary Name-Sanskrit`, `Primary Name-English`, `Primary Name Language`, `Other Names-Tibetan`, 
`Other Names-Sanskrit`, `Other Names-English`, `Dates`, `Date-Begin`, `Date-End`, `Translated by`, `Translator of`, 
`recID`, `bAuthor`, `bTranslator`, `Notes`
FROM acipmaintenance.authors
WHERE length(`Primary Name-Tibetan`) > 0
INTO 
	outfile '/var/lib/mysql-files/etext_authors_with_headers.csv' 
    fields terminated by ',' enclosed by '"' lines terminated by '\n';