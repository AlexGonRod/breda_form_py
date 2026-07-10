import os
from dotenv import load_dotenv
from formulari_app.lib.constants import MAX_PERSONS
from formulari_app.lib.error_handling import DataAppendError
from formulari_app.lib.logger import logger

load_dotenv()

class SheetsService:
    @classmethod
    def get_max_personas(cls, sheet_name: str) -> int:
        sheet_name_lower = sheet_name.lower()
        for event_key, max_val in MAX_PERSONS.items():
            if sheet_name_lower.startswith(event_key.lower()):
                logger.debug("Max persons for %s: %d", sheet_name, max_val)
                return max_val
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
    def append_row(cls, data: list, sheet, sheet_name: str) -> tuple[bool, str]:
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
                persones_to_add = int(data[2])
                if total_persones + persones_to_add > event_max:
                    spots_left = event_max - total_persones
                    logger.warning(
                        "Event full for %s. Current: %d, Requested: %d, Max: %d, Spots left: %d",
                        name, total_persones, persones_to_add, event_max, spots_left
                    )
                    raise DataAppendError(
                        f"No hi ha prou places. Només queden {spots_left} places i n'has demanat {persones_to_add}."
                    )
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
