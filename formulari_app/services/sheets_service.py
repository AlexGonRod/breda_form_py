import os
from dotenv import load_dotenv
from formulari_app.lib.error_handling import DataAppendError
from formulari_app.models.models import FORMDATA
from formulari_app.lib.logger import logger

load_dotenv()

class SheetsService:
    # Event-specific maximum persons
    EVENT_MAX_PERSONS = {
        "Tast": 40,
        "Paelles": 999,  # No real limit
    }

    @classmethod
    def get_max_personas(cls, sheet_name: str) -> int:
        for event_key, max_val in cls.EVENT_MAX_PERSONS.items():
            if event_key.lower() in sheet_name.lower():
                logger.debug("Max persons for %s: %d", sheet_name, max_val)
                return max_val
        # Default to no limit
        logger.debug("No max limit configured for %s, using default 999", sheet_name)
        return 999

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

        # Check occupancy limit only for events with defined limits
        event_max = cls.get_max_personas(sheet_name)
        if event_max < 999:  # Only if it has a real limit (not the default 999)
            try:
                total_persones = int(cls.get_total_personas(sheet))
                if total_persones >= event_max:
                    logger.warning("Event full for %s. Current: %d, Max: %d", name, total_persones, event_max)
                    raise DataAppendError(f"El número total de persones excedeix el límit de {event_max}. Total actual: {total_persones}")
            except DataAppendError:
                raise
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
