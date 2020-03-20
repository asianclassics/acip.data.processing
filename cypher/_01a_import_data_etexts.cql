// IMPORT DATA
// import location for Neo4j:
// -- /Users/joel/Library/Application Support/Neo4j Desktop/Application/neo4jDatabases
// -- so when importing into Neo4j specify:
// ---- file:///directory_in_database_folder_above/file
// reset database
MATCH (n) DETACH DELETE n;

// LOAD DATA ---------------------------
// place data in Neo4j data folder

//"catRef","tibText","newCatNo","collection","chkLevel","catalogingStatus","titleEng","titleTib","titleTibBrief","titleSkt","langMain","authorEng","authorTib","authorSkt","authorDates","primaryAuthorTib","primaryAuthorEng","primaryAuthorSkt","subjectEng","subjectTib","subjectSkt","sectionVolume","volNdx","foliosPages","edition","description","notes","drawingsAndIllustrations","datespublished","textFormat","cover","readability","pageNumbers","pageSize","printedAreaSize","linesPerPage","verificationResults","lowestFolioNo","highestFolioNo","nFolios","nPages","tibEntry","t3.engEntry","sktEntry"
USING PERIODIC COMMIT 
LOAD CSV WITH HEADERS FROM "file:///acip/etext_authors_with_headers.csv" as row FIELDTERMINATOR ","
CREATE (:Author {
    id: row.recID,
    author_eng: row.primaryNameEng,
    author_tib:	row.primaryNameTib,
    author_skt: row.primaryNameSkt,
    author_dates: row.Dates
});

// "tibEntry","engEntry","sktEntry","newTibEntry","newEngEntry","newSktEntry","recID"
USING PERIODIC COMMIT 
LOAD CSV WITH HEADERS FROM "file:///acip/etext_subjects_with_headers.csv" as row FIELDTERMINATOR ","
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
LOAD CSV WITH HEADERS FROM "file:///acip/etext_with_headers.csv" as row FIELDTERMINATOR ","
CREATE (w:Work {
	cat_ref:row.catRef,
    cat_number:row.newCatNo,
    title_eng: row.titleEng,
    title_tib: row.titleTib,
    title_tib_brief: row.titleTibBrief,
    title_skt: row.titleSkt
    });

USING PERIODIC COMMIT 
LOAD CSV WITH HEADERS FROM "file:///acip/etext_text_data_with_headers.csv" as row FIELDTERMINATOR ","
CREATE (t:Transliteration {
    cat_ref: row.catRef,
    text: row.tibText
});


