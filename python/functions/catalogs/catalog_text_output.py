# text utilities
def text_output_to_single_file(data, file):
    success = False
    try:
        with open(file, 'w', encoding='utf-8') as outfile:
            for row_idx, row in enumerate(data.itertuples(index=False, name='CatalogItem')):

                if not any(row) or not row:
                    continue
                else:
                    outfile.write('\n=======================================================\n')

                for idx, x in enumerate(row):
                    if x is None or len(x) == 0:
                        continue
                    if data.columns[idx] == 'nlm_catalog':
                        outfile.write(f"{x}\n")
                    else:
                        outfile.write(f"{data.columns[idx]}: {x}\n")

                # print("Progress {:2.1%}".format(row_idx / 10), end="\r")
        success = True
    except IOError as error:
        print('IOError', error)

    return success
