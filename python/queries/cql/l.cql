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