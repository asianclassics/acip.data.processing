MERGE (a:TestPerson {id: row.recID})
    ON CREATE SET
        a.author_eng = row.primaryNameEng,
        a.author_tib = row.primaryNameTib,
        a.author_skt = row.primaryNameSkt,
        a.author_dates = row.Dates;