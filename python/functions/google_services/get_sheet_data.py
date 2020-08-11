def get_sheet_data(service, **kwargs):
    sheet_range = f'{kwargs["workbooks"]["mappings"]["sheet_name"]}!A1:Z'
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=kwargs["workbooks"]["mappings"]["key_test"],
                                range=sheet_range, majorDimension="ROWS").execute()
    data = result.get('values', [])

    if not data:
        print('No data found.')
    else:
        return data

        # for row in values:
        #     # Print columns A and E, which correspond to indices 0 and 4.
        #     print('%s, %s' % (row[0], row[4]))

