class ErrorHandlerBase(Exception):
    def __init__(self, msg:str):
        self.message = msg
        super().__init__(self.message)

class PermissionDenied(ErrorHandlerBase):
    def __init__(self, msg:str):
        super().__init__(f"Permis denegat: {msg}")

class WorksheetNotFound(ErrorHandlerBase):
    def __init__(self, work_sheet:str):
        super().__init__(f"Worksheet no trobada: '{work_sheet}'" if work_sheet else "Worksheet no especificada")

class SpreadsheetNotFound(ErrorHandlerBase):
    def __init__(self, spreadsheet_id:str):
        super().__init__(f"Spreadsheet no trobada: '{spreadsheet_id}'" if spreadsheet_id else "Spreadsheet no especificada")

class APIError(ErrorHandlerBase):
    def __init__(self, msg:str):
        super().__init__(f"Error de l'API: {msg}")

class DataAppendError(ErrorHandlerBase):
    def __init__(self, msg:str):
        super().__init__(f"Error al afegir dades: {msg}")
