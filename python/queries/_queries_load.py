# loading etext data --------------------------------------------
# http://104.248.221.150/csv/etext_with_headers.csv
base_uri = 'http://104.248.221.150/csv'

csv_etexts = 'etext_with_headers.csv'  # httpTexts
csv_authors = 'etext_authors_with_headers.csv'  #httpAuthors
# AUTHORS
q_load_authors = """
    LOAD CSV WITH HEADERS FROM {csv} as row FIELDTERMINATOR ","
    WITH row LIMIT {limit}
    MERGE (a:TestPerson {id: row.recID})
    ON CREATE SET
        a.author_eng = row.primaryNameEng,
        a.author_tib = row.primaryNameTib,
        a.author_skt = row.primaryNameSkt,
        a.author_dates = row.Dates;
"""

# WORKS
q_load_works = """
    LOAD CSV WITH HEADERS FROM {csv} as row FIELDTERMINATOR ","
    WITH row LIMIT {limit}
    MERGE (w:TestWork2 {cat_ref: row.catRef})
    ON CREATE SET
        w.cat_ref = row.catRef,
        w.cat_number = row.newCatNo,
        w.author_eng = row.primaryAuthorEng,
        w.author_tib = row.primaryAuthorTib,
        w.title_eng = row.titleEng,
        w.title_tib = row.titleTib,
        w.title_tib_brief = row.titleTibBrief,
        w.title_skt = row.titleSkt;
"""

# ITEMS
q_load_items = """
    LOAD CSV WITH HEADERS FROM {csv} as row FIELDTERMINATOR ","
    WITH row LIMIT {limit}
    MERGE (i:TestItem {cat_ref: row.catRef})
    ON CREATE SET
        i.cat_ref = row.catRef,
        i.language = row.langMain,
        i.foliosPages = row.foliosPages,
        i.edition = row.edition,
        i.description = row.description,
        i.notes = row.notes,
        i.textFormat = row.textFormat,
        i.cover = row.cover,
        i.readability = row.readability,
        i.pageNumbers = row.pageNumbers,
        i.pageSize = row.pageSize,
        i.printedAreaSize = row.printedAreaSize,
        i.linesPerPage = row.linesPerPage;
"""

# using apoc
q_apoc_load = """
    CALL apoc.periodic.iterate('
    CALL apoc.load.csv($httpTexts) yield map as row return row
    ','
    MERGE (i:TestItem {cat_ref: row.catRef})
    ON CREATE SET
        i.cat_ref = row.catRef,
        i.language = row.langMain,
        i.foliosPages = row.foliosPages,
        i.edition = row.edition,
        i.description = row.description,
        i.notes = row.notes,
        i.textFormat = row.textFormat,
        i.cover = row.cover,
        i.readability = row.readability,
        i.pageNumbers = row.pageNumbers,
        i.pageSize = row.pageSize,
        i.printedAreaSize = row.printedAreaSize,
        i.linesPerPage = row.linesPerPage
    ', {batchSize:$bsize, iterateList:true, parallel:true, params:{httpTexts:$httpTexts, bsize:$bsize}}
    );
"""