USE acipmaintenance;
SELECT 'catRef', 'tibText', 'newCatNo', 'collection', 'chkLevel', 
    'catalogingStatus', 'titleEng', 'titleTib', 'titleTibBrief', 'titleSkt',
	'langMain', 'authorEng', 'authorTib', 'authorSkt', 'authorDates',
	'primaryAuthorTib', 'primaryAuthorEng', 'primaryAuthorSkt',
	'subjectEng', 'subjectTib', 'subjectSkt',
	'sectionVolume', 'volNdx',
	'foliosPages', 'edition',
	'description', 'notes', 'drawingsAndIllustrations',
	'datespublished', 'textFormat', 'cover', 'readability',
	'pageNumbers', 'pageSize', 'printedAreaSize', 'linesPerPage',
	'verificationResults',
	'lowestFolioNo', 'highestFolioNo', 'nFolios', 'nPages'
UNION ALL
SELECT
	t1.catRef, CONVERT(uncompress(t2.Data) USING 'utf8'), newCatNo, collection, chkLevel, 
    catalogingStatus, titleEng, titleTib, titleTibBrief, titleSkt,
	langMain, authorEng, authorTib, authorSkt, authorDates,
	convert((t1.primaryAuthorTib) USING 'utf8'), primaryAuthorEng, primaryAuthorSkt,
	subjectEng, subjectTib, subjectSkt,
	sectionVolume, volNdx,
	foliosPages, edition,
	description, t1.notes, drawingsAndIllustrations,
	datespublished, textFormat, cover, readability,
	pageNumbers, pageSize, printedAreaSize, linesPerPage,
	verificationResults,
	lowestFolioNo, highestFolioNo, nFolios, nPages
FROM acipmaintenance.aciptbl t1
	join acipmaintenance.aciptbldata t2
		on (t1.catRef = t2.CatRef)
WHERE chkLevel in ('E', 'M', 'N', 'O')
INTO 
	outfile '/var/lib/mysql-files/etext_text_data_with_headers.csv' 
    fields terminated by ',' enclosed by '"' lines terminated by '\n';