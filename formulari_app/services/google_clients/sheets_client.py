import gspread
from formulari_app.lib.error_handling import WorksheetNotFound, SpreadsheetNotFound, APIError, DataAppendError, PermissionDenied
from formulari_app.lib.logger import logger


def sheets_client(creds, spreadsheet_name: str, sheet_name: str):
    spreadsheet = None
    worksheet = None

    try:
        logger.debug("Connecting to spreadsheet: %s, sheet: %s", spreadsheet_name, sheet_name)
        client = gspread.authorize(creds)
        # get the instance of the Spreadsheet
        spreadsheet = client.open_by_key(spreadsheet_name)
        worksheet = spreadsheet.worksheet(sheet_name)

        if not spreadsheet:
            raise SpreadsheetNotFound(f"{spreadsheet_name}")
        if not worksheet:
            raise WorksheetNotFound(f"{sheet_name}")

        logger.info("✅ Connected to sheet: %s", sheet_name)
        return worksheet

    except gspread.exceptions.WorksheetNotFound as e:
        logger.error("Worksheet not found: %s", sheet_name)
        raise WorksheetNotFound(f"Worksheet not found: {sheet_name}") from e

    except gspread.exceptions.APIError as e:
        logger.error("Google Sheets API error %d: %s", e.response.status_code, e)
        if e.response.status_code == 404:
            raise SpreadsheetNotFound(f"{spreadsheet_name}") from e
        if e.response.status_code == 429:
            logger.warning("Google Sheets API quota exceeded")
            raise DataAppendError("Límit de quota excedida") from e
        elif e.response.status_code == 403:
            logger.warning("Permission denied to Google Sheets")
            raise PermissionDenied("Acces denegat a la fulla de càlcul") from e
        else:
            raise APIError(f"Codi d'error {e.response.status_code}") from e

    except gspread.exceptions.GSpreadException as e:
        logger.error("Google Sheets error: %s", e)
        raise DataAppendError(f"Error al afegir dades: {str(e)}") from e

    except Exception as e:
        logger.error("Error initializing SheetsClient: %s", e, exc_info=True)
        raise ValueError(f'Error initializing SheetsClient: {str(e)}') from e
