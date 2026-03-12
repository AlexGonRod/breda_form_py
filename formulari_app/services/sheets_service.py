from dotenv import load_dotenv
from formulari_app.lib.error_handling import DataAppendError
from formulari_app.models.models import FORMDATA

load_dotenv()

def mock_formdata(last_row, data):
    return (last_row - 1), data[0], data[1], data[2]

class SheetsService:
    def __init__(self) -> None:
        pass

    @classmethod
    def append_row(self, data: list[FORMDATA], sheet) -> tuple[bool, str]:
        if not data:
            raise DataAppendError("No hay datos para añadir")
        last_row = sheet.row_count
        data_mock = mock_formdata(last_row, data)
        sheet.append_row(data_mock, table_range=f"A{last_row+1}")

        return (True, "Datos añadidos correctamente")
