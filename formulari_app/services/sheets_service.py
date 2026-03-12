from dotenv import load_dotenv
from formulari_app.lib.error_handling import DataAppendError
from formulari_app.services.google_clients.sheets_client import sheets_client
from formulari_app.services.google_clients.google_client import GoogleClient
from formulari_app.lib.google_credentials import credentials, SCOPES
from formulari_app.models.models import FORMDATA

load_dotenv()

def get_first_empty_row(sheet, start, end, col=2):
    cell_range = f"{chr(64+col)}{start}:{chr(64+col)}{end}"
    values = sheet.get(cell_range)

    for i, row in enumerate(values):
        if not row or row == ['']:
            return start + i
    if len(values) < (end - start + 1):
        print(f"First empty row in block {start}-{end} is {start + len(values)}")
        return start + len(values)
    return None

class SheetsService:
    def __init__(self, spreadsheet_name: str, sheet_name: str) -> None:
        self.spreadsheet_name = spreadsheet_name
        self.sheet_name = sheet_name
        self.data_mock = []

    def get_sheets_client(self):
        creds = GoogleClient.create_with_credentials(credentials_args = credentials, scopes = SCOPES)
        return sheets_client(creds, self.spreadsheet_name, self.sheet_name)

    def mock_formdata(self, data):
        return self.sheets_client[2]+1,data[0], data[1], data[2]

    def append_row(self, data: list[FORMDATA]) -> tuple[bool, str]:
        if not data:
            raise DataAppendError("No hay datos para añadir")

        sheet = self.get_sheets_client()
        last_row = sheet.row_count

        self.data_mock = self.mock_formdata(data)
        sheet.append_row(self.data_mock, table_range=f"A{last_row+1}")

        return (True, "Datos añadidos correctamente")
