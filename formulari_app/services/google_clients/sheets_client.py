import gspread
from formulari_app.lib.error_handling import WorksheetNotFound, SpreadsheetNotFound
from formulari_app.services.google_clients.google_client import GoogleClient
from formulari_app.lib.google_credentials import credentials, SCOPES

def sheets_client(spreadhseet_name: str, sheet_name: str):
    try:
        creds = GoogleClient.create_with_credentials(credentials, SCOPES)
        client = gspread.Client(auth=creds)
        # get the instance of the Spreadsheet
        ws = client.open_by_key(spreadhseet_name)
        sheet = ws.worksheet(sheet_name)

        if not ws:
            raise WorksheetNotFound(f"{spreadhseet_name}")
        if not sheet:
            raise SpreadsheetNotFound(f"{sheet_name}")

        last_row = sheet.row_count
        return ws, sheet, last_row

    except Exception as e:
        raise Exception(f'Error initializing SheetsClient: {str(e)}') from e
