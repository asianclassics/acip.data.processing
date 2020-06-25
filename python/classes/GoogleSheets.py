import gspread
from oauth2client.service_account import ServiceAccountCredentials


class GoogleSheets:
    def __init__(self, config, key=None):
        self.config = config
        self.credentials = self.authorize()
        self.workbook_key = key

        if key is None and 'workbook_key' in config:
            self.workbook_key = config['workbook_key']

        self.data = self.get_listing()

    def authorize(self):
        gc = None
        try:
            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                self.config["json_creds"], self.config["scope"]
            )

            gc = gspread.authorize(credentials)
            print(f"Authorizing script for Google Sheets...", gc)
        except IOError as e:
            print(e)

        return gc

    def get_listing(self, ws=None, col=1, with_prefix=False):
        if ws is None:
            ws = self.config["starting_worksheet_name"]

        if self.workbook_key is not None and ws is not None:
            wkb = self.credentials.open_by_key(self.workbook_key)
            wks = wkb.worksheet(ws)
            works = wks.col_values(col)

            if with_prefix:
                works = ['bdr:{0}'.format(c) if c[:4] != 'bdr:' else c for c in works]
            else:
                works = [c[4:] if c[:4] == 'bdr:' else c for c in works]

            return sorted(works)

        return

    def get_worksheet_data(self, ws=None):
        if ws is None:
            ws = self.config["starting_worksheet_name"]

        if self.workbook_key is not None and ws is not None:
            wkb = self.credentials.open_by_key(self.workbook_key)
            wks = wkb.worksheet(ws)
            return wks
            # works = wks.col_values(col)

    def get_worksheets(self):
        worksheets = {}
        workbook = None
        if self.workbook_key is not None:
            workbook = self.credentials.open_by_key(self.workbook_key)

            for item in workbook.worksheets():
                worksheets.update({item.title: item.id})

        return [workbook, worksheets]

    def write_listing(self, data=None, ws=None, header=None):
        if ws is None:
            ws = self.config["worksheet_name"]

        if data is None:
            data = self.data

        [workbook, worksheets] = self.get_worksheets()

        if workbook is None:
            print("No workbook!")
            return
        elif ws in worksheets:
            print("Deleting worksheet", ws)
            sh = workbook.worksheet(ws)
            workbook.del_worksheet(sh)

        # recreate the worksheet
        print("Recreating worksheet. Data has length: ", len(data))
        workbook.add_worksheet(title=ws, rows=len(data), cols=26)

        if header is not None:
            # add header as list of list
            workbook.values_append(
                ws,
                params={'valueInputOption': 'USER_ENTERED'},
                body={'values': [list(header)]}
            )
            # .values to numpy array, tolist...list of lists!
            workbook.values_append(
                ws,
                params={'valueInputOption': 'USER_ENTERED'},
                body={'values': data.values.tolist()}
            )
        else:
            workbook.values_append(
                ws,
                params={'valueInputOption': 'RAW'},
                body={'values': [data], 'majorDimension': 'COLUMNS'}
            )

