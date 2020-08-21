from tqdm import tqdm


def filter_keys(document):
    print('filter_keys', document)
    # return a row with only the keys you want


def dataframe_doc_generator(df, index_name="v1_acip_catalogs"):

    for idx, document in tqdm(df.iterrows(), total=df.shape[0]):

        doc_id = document['catno'] if len(document['catno']) > 3 else f"unknown_id_{idx}"

        yield {
            "_index": index_name,
            "_id": doc_id,
            "_source": document.to_dict()  # filterKeys(document),
        }
