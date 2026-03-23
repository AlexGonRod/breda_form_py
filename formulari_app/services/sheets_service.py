import os
from dotenv import load_dotenv
from formulari_app.lib.error_handling import DataAppendError
from formulari_app.models.models import FORMDATA
from formulari_app.lib.logger import logger

load_dotenv()

# Read max_persons from env with default fallback
try:
    max_persons = int(os.getenv("MAX_PERSONS", "40"))
    if max_persons < 1:
        raise ValueError("MAX_PERSONS must be >= 1")
    logger.info("Max persons configured: %d", max_persons)
except ValueError as e:
    error_msg = f"Invalid MAX_PERSONS environment variable: {e}"
    logger.error("%s", error_msg)
    raise ValueError(error_msg) from e

class SheetsService:
    @classmethod
    def get_total_personas(cls, sheet):
        try:
            total = sheet.acell("F2").value
            logger.debug("Retrieved occupancy from sheet: %s", total)
            return total
        except Exception as e:
            logger.error("Error retrieving occupancy: %s", e)
            raise

    @classmethod
    def append_row(cls, data: list[FORMDATA], sheet, sheet_name: str) -> tuple[bool, str]:
        if not data:
            logger.warning("Attempted to append empty data to %s", sheet_name)
            raise DataAppendError("No hay datos para añadir")

        name = sheet_name.capitalize()
        logger.info("Processing form submission for: %s", name)
        logger.debug("Form data: %s", data)
        
        if "Tast" in name:
            try:
                total_persones = int(cls.get_total_personas(sheet))
                if total_persones >= max_persons:
                    logger.warning("Event full for %s. Current: %d, Max: %d", name, total_persones, max_persons)
                    raise DataAppendError(f"El número total de persones excedeix el límit de {max_persons}. Total actual: {total_persones}")
            except Exception as e:
                logger.error("Error checking occupancy for %s: %s", name, e)
                raise

        try:
            row_formula = "=ROW()-1"
            full_row = [row_formula] + data
            
            sheet.append_row(full_row, value_input_option="USER_ENTERED", insert_data_option="INSERT_ROWS")
            logger.info("✅ Successfully appended row to %s: %s", name, data)
            return (True, "Dades afegides correctament")
        except Exception as e:
            logger.error("Error appending row to %s: %s", name, e)
            raise
