from dotenv import load_dotenv
import gspread
from formulari_app.lib.error_handling import WorksheetNotFound, SpreadsheetNotFound, APIError, dataAppendError, PermissionDenied
from formulari_app.services.google_clients.sheets_client import sheets_client
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
        # authorize the clientsheet
        self.sheets_client = sheets_client(spreadsheet_name, sheet_name)
        self.data_mock = []

    def mock_formdata(self, data):
        return self.sheets_client[2]+1,data[0], data[1], data[2]

    def append_row(self, data: list[FORMDATA]) -> tuple[bool, str]:
        if not data:
            raise dataAppendError("No hay datos para añadir")

        ws, sheet, last_row = self.sheets_client
        try:
            self.data_mock = self.mock_formdata(data)
            sheet.append_row(self.data_mock, table_range=f"A{last_row+1}")

            return (True, "Datos añadidos correctamente")

        except gspread.exceptions.WorksheetNotFound as e:
            raise WorksheetNotFound(f"{ws}") from e

        except gspread.exceptions.APIError as e:
            if e.response.status_code == 404:
                raise SpreadsheetNotFound(f"{sheet}") from e
            if e.response.status_code == 429:
                raise dataAppendError("Límite de cuota excedido") from e
            elif e.response.status_code == 403:
                raise PermissionDenied("Acceso denegado a la hoja de cálculo") from e
            else:
                raise APIError(f"Código de estado {e.response.status_code}") from e

        except gspread.exceptions.GSpreadException as e:
            return (False, f"Error al añadir datos: {str(e)}")

        except Exception as e:
            raise  PermissionDenied(f"Error: {str(e)}") from e
