person_work_apoc = """
    MATCH (w:Work)
    MATCH (p:Person)
    WHERE size(p.name_tib) > 0 and p.name_tib = w.author_tib
    CALL apoc.create.relationship(p, 'IS_CREATOR',{}, w) YIELD rel
    REMOVE rel.noOp;
"""

person_work = """
    MATCH (w:Work)
    MATCH (p:Person)
    WHERE size(p.name_tib) > 0 and p.name_tib = w.author_tib
    MERGE(p)-[:IS_CREATOR]->(w);
"""

work_item_apoc = """
    MATCH (w:Work)
    MATCH (i:Item)
    WHERE w.title_tib_brief = i.title_tib_brief
    CALL apoc.create.relationship(w, 'HAS_INSTANCE',{}, i) YIELD rel
    REMOVE rel.noOp;
"""

work_item = """
    MATCH (w:Work)
    MATCH (i:Item)
    WHERE w.title_tib_brief = i.title_tib_brief
    MERGE(w)-[:HAS_INSTANCE]->(i);
"""

item_digital_asset = """
    MATCH (i:Item)
    MATCH (d:Digital_Asset)
    WHERE i.cat_ref = d.cat_ref
    MERGE(i)-[:HAS_DIGITAL_ASSET]->(d);
"""

topic_work_temporary = """
    MATCH (w:Work)
    WITH w,
        SPLIT(w.subject_tib, ';') as list_tib,
        SPLIT(w.subject_eng, ';') as list_eng,
        SPLIT(w.subject_skt, ';') as list_skt
    UNWIND list_tib as subject_tib
    UNWIND list_eng as subject_eng
    UNWIND list_skt as subject_skt
    WITH distinct subject_tib as tib, w, subject_eng, subject_skt
    WITH distinct subject_eng as eng, tib, w, subject_skt
    WITH distinct subject_skt as skt, tib, eng, w
    MERGE(t:Topic {
        topic_tib: tib,
        topic_eng: eng,
        topic_skt: skt
        })
    MERGE(w)-[:HAS_SUBJECT]->(t)
"""

topic_work_temp_by_english = """
    MATCH (w:Work)
    WITH w, SPLIT(w.subject_eng, ';') as list_eng
    UNWIND list_eng as subject_eng
    WITH distinct subject_eng as eng, w
    MERGE(t:Topic {topic_eng: eng})
    MERGE(w)-[:HAS_SUBJECT]->(t)
"""
