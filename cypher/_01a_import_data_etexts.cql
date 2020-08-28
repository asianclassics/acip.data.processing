// IMPORT DATA
// import location for Neo4j:
// -- /Users/joel/Library/Application Support/Neo4j Desktop/Application/neo4jDatabases
// -- so when importing into Neo4j specify:
// ---- file:///directory_in_database_folder_above/file

// reset database
MATCH (n) DETACH DELETE n;

// LOAD DATA ---------------------------

//"catRef","tibText","newCatNo","collection","chkLevel","catalogingStatus","titleEng","titleTib","titleTibBrief","titleSkt","langMain","authorEng","authorTib","authorSkt","authorDates","primaryAuthorTib","primaryAuthorEng","primaryAuthorSkt","subjectEng","subjectTib","subjectSkt","sectionVolume","volNdx","foliosPages","edition","description","notes","drawingsAndIllustrations","datespublished","textFormat","cover","readability","pageNumbers","pageSize","printedAreaSize","linesPerPage","verificationResults","lowestFolioNo","highestFolioNo","nFolios","nPages","tibEntry","t3.engEntry","sktEntry"
USING PERIODIC COMMIT 
LOAD CSV WITH HEADERS FROM $fileAuthors as row FIELDTERMINATOR ","
CREATE (:Author {
    id: row.recID,
    author_eng: row.primaryNameEng,
    author_tib:	row.primaryNameTib,
    author_skt: row.primaryNameSkt,
    author_dates: row.Dates
});

// "tibEntry","engEntry","sktEntry","newTibEntry","newEngEntry","newSktEntry","recID"
USING PERIODIC COMMIT 
LOAD CSV WITH HEADERS FROM $fileSubjects as row FIELDTERMINATOR ","
CREATE (:Subject {
    id: row.recID,
    subject_eng: row.engEntry,
    subject_tib:	row.tibEntry,
    subject_skt: row.sktEntry
});
// load metadata
//[0] catRef[0]	tibText[1] newCatNo[2]	collection	chkLevel	catalogingStatus	
//[6] titleEng[6] titleTib[7]	titleTibBrief[8]	titleSkt[9]	langMain	
//[11] authorEng	authorTib authorSkt	authorDates	
//[15] primaryAuthorTib	primaryAuthorEng		
//[17] primaryAuthorSkt subjectEng	subjectTib	subjectSkt	sectionVolume	volNdx[22]
//[23] foliosPages[23]	edition[24]	description[25]	notes[26]	drawingsAndIllustrations	datespublished[27]	
//[28] textFormat	cover	readability	pageNumbers	pageSize	
//[33] printedAreaSize	linesPerPage	verificationResults	lowestFolioNo	
//[37] highestFolioNo	nFolios	nPages	tibEntry	engEntry	sktEntry
USING PERIODIC COMMIT 
LOAD CSV WITH HEADERS FROM $fileTexts as row FIELDTERMINATOR ","
CREATE (:Work {
	cat_ref:row.catRef,
    cat_number:row.newCatNo,
    title_eng: row.titleEng,
    title_tib: row.titleTib,
    title_tib_brief: row.titleTibBrief,
    title_skt: row.titleSkt
    });

USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM $fileTexts as row FIELDTERMINATOR ","
CREATE (:Item {
    cat_ref: row.catRef,
    language: row.langMain,
    foliosPages: row.foliosPages,
    edition: row.edition,
    description: row.description,
    notes: row.notes,
    textFormat: row.textFormat,
    cover: row.cover,
    readability: row.readability,
    pageNumbers: row.pageNumbers,
    pageSize: row.pageSize,
    printedAreaSize: row.printedAreaSize,
    linesPerPage: row.linesPerPage
});

USING PERIODIC COMMIT 
LOAD CSV WITH HEADERS FROM $fileTextData as row FIELDTERMINATOR ","
CREATE (:Transliteration {
    cat_ref: row.catRef,
    text: row.tibText
});


