from dotenv import load_dotenv
from formulari_app.lib.error_handling import DataAppendError
from formulari_app.models.models import FORMDATA

load_dotenv()

class SheetsService:
    @classmethod
    def append_row(cls, data: list[FORMDATA], sheet) -> tuple[bool, str]:
        if not data:
            raise DataAppendError("No hay datos para añadir")

        row_formula = "=ROW()-1"
        full_row = [row_formula] + data

        sheet.append_row(full_row,value_input_option="USER_ENTERED", insert_data_option="INSERT_ROWS")

        return (True, "Datos añadidos correctamente")
