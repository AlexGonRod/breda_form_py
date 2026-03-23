from dotenv import load_dotenv
from formulari_app.lib.error_handling import DataAppendError
from formulari_app.models.models import FORMDATA

load_dotenv()
max_persons = 40

class SheetsService:
    @classmethod
    def get_total_personas(cls, sheet):
        return sheet.acell("F2").value

    @classmethod
    def append_row(cls, data: list[FORMDATA], sheet, sheet_name:str) -> tuple[bool, str]:
        if not data:
            raise DataAppendError("No hay datos para añadir")
        
        name = sheet_name.capitalize()
        if "Tast" in name:
            total_persones = int(cls.get_total_personas(sheet))
            if total_persones >= max_persons:
                raise DataAppendError(f"El número total de personas excede el límite de {max_persons}. Total actual: {total_persones}")

        row_formula = "=ROW()-1"
        full_row = [row_formula] + data

        sheet.append_row(full_row,value_input_option="USER_ENTERED", insert_data_option="INSERT_ROWS")

        return (True, "Datos añadidos correctamente")
