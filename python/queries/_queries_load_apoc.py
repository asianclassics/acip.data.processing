# loading data --------------------------------------------
# http://104.248.221.150/csv/

# PERSON -----------------------------------------------
persons = """
    CALL apoc.periodic.iterate('
    CALL apoc.load.csv($csv) yield map as row return row
    ','
    MERGE (p:Person {id: row.recID})
    ON CREATE SET
        p.name_eng = row.primaryNameEng,
        p.name_tib = row.primaryNameTib,
        p.name_skt = row.primaryNameSkt,
        p.person_dates = row.dates
    ', {batchSize:$bsize, iterateList:true, parallel:true, params:{csv:$csv, bsize:$bsize}}
    );
"""

# TOPIC -----------------------------------------------
topics = """
    CALL apoc.periodic.iterate('
    CALL apoc.load.csv($csv) yield map as row return row
    ','
    MERGE (t:Topic {id:row.recID}) 
    ON CREATE SET
        t.topic_eng = row.engEntry,
        t.topic_tib = row.tibEntry,
        t.topic_skt = row.sktEntry
    ', {batchSize:$bsize, iterateList:true, parallel:true, params:{csv:$csv, bsize:$bsize}}
    );
"""

# must call this after WORK is created
topics_temporary = """
    MATCH (w:Work)
    WITH SPLIT(n.subject_tib, ';') as list_tib
    UNWIND t.list_tib as subject_tib
    MERGE(t:Topic {topic_tib: subject_tib})
"""

# WORK -----------------------------------------------
works = """
    CALL apoc.periodic.iterate('
    CALL apoc.load.csv($csv) yield map as row return row
    ','
    MERGE (w:Work {id: row.titletibbrief})
    ON CREATE SET
        w.author_eng = row.authorengprimary,
        w.author_tib = row.authortibprimary,
        w.title_tib_brief = row.titletibbrief,
        w.subject_eng = row.subjecteng,
        w.subject_tib = row.subjecttib,
        w.subject_skt = row.subjectskt
    ', {batchSize:$bsize, iterateList:true, parallel:true, params:{csv:$csv, bsize:$bsize}}
    );
"""

# ACI COURSE ITEM ------------------------------------
aci_item = """
CALL apoc.periodic.iterate('
CALL apoc.load.csv($csv, {sep:$sep}) yield map as row return row
','
MERGE (i:Item {cat_ref: row.assetID})
ON CREATE SET
    i.cat_ref = row.assetID,
    i.type = "Translation",
    i.title_tib_brief = row.workID,
    i.title_eng = row.title_eng,
    i.author_eng = row.author_eng,
    i.folio = row.folio
', {batchSize:$bsize, iterateList:true, parallel:true, params:{csv:$csv, bsize:$bsize, sep:$sep}}
    );
"""

aci_digital_asset = """
CALL apoc.periodic.iterate('
    CALL apoc.load.csv($csv, {sep:$sep}) yield map as row return row
    ','
    MERGE (d:Digital_Asset:Translation {cat_ref: row.assetID})
    ON CREATE SET
        d.text = row.text
    ', {batchSize:$bsize, iterateList:true, parallel:true, params:{csv:$csv, bsize:$bsize, sep:$sep}}
    );
"""


# ITEM -----------------------------------------------
items = """
    CALL apoc.periodic.iterate('
    CALL apoc.load.csv($csv) yield map as row return row
    ','
    MERGE (i:Item {cat_ref: row.catref})
    ON CREATE SET
        i.cat_ref = row.catref,
        i.type = "Transliteration",
        i.title_tib_brief = row.titletibbrief,
        i.title_eng = row.titleeng,
        i.title_tib = row.titletib,
        i.title_skt = row.titleskt,
        i.cat_number = row.newcatref,
        i.language = row.language,
        i.chklevel = row.chklevel,
        i.collection = row.collection,
        i.foliosPages = row.folios,
        i.edition = row.edition,
        i.description = row.description,
        i.notes = row.notes,
        i.textFormat = row.textformat,
        i.cover = row.cover,
        i.readability = row.readability,
        i.pageNumbers = row.pagenumbers,
        i.pageSize = row.pagesize,
        i.printedAreaSize = row.printedareasize,
        i.linesPerPage = row.linesperpage
    ', {batchSize:$bsize, iterateList:true, parallel:true, params:{csv:$csv, bsize:$bsize}}
    );
"""

digital_asset = """
    CALL apoc.periodic.iterate('
    CALL apoc.load.csv($csv) yield map as row return row
    ','
    MERGE (d:Digital_Asset:Transliteration {cat_ref: row.catref})
    ON CREATE SET
        d.text = row.tibtext
    ', {batchSize:$bsize, iterateList:true, parallel:true, params:{csv:$csv, bsize:$bsize}}
    );
"""

#  d.type = \'Transliteration\',
