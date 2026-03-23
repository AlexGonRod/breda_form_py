import gspread
from formulari_app.lib.error_handling import WorksheetNotFound, SpreadsheetNotFound, APIError, DataAppendError, PermissionDenied
from formulari_app.lib.logger import logger


def sheets_client(creds, spreadhseet_name: str, sheet_name: str):
    ws, sheet= None, None

    try:
        logger.debug("Connecting to spreadsheet: %s, sheet: %s", spreadhseet_name, sheet_name)
        client = gspread.Client(auth=creds)
        # get the instance of the Spreadsheet
        ws = client.open_by_key(spreadhseet_name)
        sheet = ws.worksheet(sheet_name)

        if not ws:
            raise WorksheetNotFound(f"{spreadhseet_name}")
        if not sheet:
            raise SpreadsheetNotFound(f"{sheet_name}")

        logger.info("✅ Connected to sheet: %s", sheet_name)
        return sheet

    except gspread.exceptions.WorksheetNotFound as e:
        logger.error("Worksheet not found: %s", sheet_name)
        raise WorksheetNotFound(f"{ws}") from e

    except gspread.exceptions.APIError as e:
        logger.error("Google Sheets API error %d: %s", e.response.status_code, e)
        if e.response.status_code == 404:
            raise SpreadsheetNotFound(f"{sheet}") from e
        if e.response.status_code == 429:
            logger.warning("Google Sheets API quota exceeded")
            raise DataAppendError("Límit de quota excedida") from e
        elif e.response.status_code == 403:
            logger.warning("Permission denied to Google Sheets")
            raise PermissionDenied("Acces denegat a la fulla de càlcul") from e
        else:
            raise APIError(f"Códi d'error {e.response.status_code}") from e

    except gspread.exceptions.GSpreadException as e:
        logger.error("Google Sheets error: %s", e)
        raise DataAppendError(f"Error al afegir dades: {str(e)}") from e

    except Exception as e:
        logger.error("Error initializing SheetsClient: %s", e, exc_info=True)
        raise ValueError(f'Error initializing SheetsClient: {str(e)}') from e
