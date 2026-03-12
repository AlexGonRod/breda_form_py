import gspread
from formulari_app.lib.error_handling import WorksheetNotFound, SpreadsheetNotFound, APIError, DataAppendError, PermissionDenied


def sheets_client(creds, spreadhseet_name: str, sheet_name: str):
    ws, sheet= None, None

    try:
        client = gspread.Client(auth=creds)
        # get the instance of the Spreadsheet
        ws = client.open_by_key(spreadhseet_name)
        sheet = ws.worksheet(sheet_name)

        if not ws:
            raise WorksheetNotFound(f"{spreadhseet_name}")
        if not sheet:
            raise SpreadsheetNotFound(f"{sheet_name}")

        return sheet

    except gspread.exceptions.WorksheetNotFound as e:
        raise WorksheetNotFound(f"{ws}") from e

    except gspread.exceptions.APIError as e:
        if e.response.status_code == 404:
            raise SpreadsheetNotFound(f"{sheet}") from e
        if e.response.status_code == 429:
            raise DataAppendError("Límite de cuota excedido") from e
        elif e.response.status_code == 403:
            raise PermissionDenied("Acceso denegado a la hoja de cálculo") from e
        else:
            raise APIError(f"Código de estado {e.response.status_code}") from e

    except gspread.exceptions.GSpreadException as e:
        raise DataAppendError(f"Error al añadir datos: {str(e)}") from e

    except Exception as e:
        raise ValueError(f'Error initializing SheetsClient: {str(e)}') from e
