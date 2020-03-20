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
	'lowestFolioNo', 'highestFolioNo', 'nFolios', 'nPages',
	'tibEntry', 't3.engEntry', 'sktEntry'
UNION ALL
SELECT
	t1.catRef, CONVERT(uncompress(t2.Data) USING 'utf8') as tibText, newCatNo, collection, chkLevel, 
    catalogingStatus, titleEng, titleTib, titleTibBrief, titleSkt,
	langMain, authorEng, authorTib, authorSkt, authorDates,
	primaryAuthorTib, primaryAuthorEng, primaryAuthorSkt,
	subjectEng, subjectTib, subjectSkt,
	sectionVolume, volNdx,
	foliosPages, edition,
	description, notes, drawingsAndIllustrations,
	datespublished, textFormat, cover, readability,
	pageNumbers, pageSize, printedAreaSize, linesPerPage,
	verificationResults,
	lowestFolioNo, highestFolioNo, nFolios, nPages,
	t3.tibEntry, t3.engEntry, t3.sktEntry
FROM acipmaintenance.aciptbl t1
	join acipmaintenance.aciptbldata t2
		on (t1.catRef = t2.CatRef)
	left join acipmaintenance.subjitems t3
		on (t1.subjectTib = t3.tibEntry)
WHERE chkLevel in ('E', 'M', 'N', 'O')
INTO 
	outfile '/var/lib/mysql-files/etext_data_with_headers.csv' 
    fields terminated by ',' enclosed by '"' lines terminated by '\n';