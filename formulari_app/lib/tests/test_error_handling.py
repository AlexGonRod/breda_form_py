import pytest
from formulari_app.lib.error_handling import PermissionDenied, WorksheetNotFound, SpreadsheetNotFound, APIError, DataAppendError

class TestErrors():
    def test_permission_denied(self):
        with pytest.raises(PermissionDenied) as exc_info:
            raise PermissionDenied("Accés no autoritzat")
        assert str(exc_info.value) == "Permis denegat: Accés no autoritzat"

    def test_worksheetNotFound(self):
        with pytest.raises(WorksheetNotFound) as exc_info:
            raise WorksheetNotFound("Formulari")
        assert str(exc_info.value) == "Worksheet no trobada: 'Formulari'"

    def test_SpreadsheetNotFound(self):
        with pytest.raises(SpreadsheetNotFound) as exec_info:
            raise SpreadsheetNotFound('1234')
        assert str(exec_info.value) == "Spreadsheet no trobada: '1234'"

    def test_APIError(self):
        with pytest.raises(APIError) as exec_info:
            raise APIError("Error en connectar amb l'API")
        assert str(exec_info.value) == "Error de l'API: Error en connectar amb l'API"

    def test_DataAppendError(self):
        with pytest.raises(DataAppendError) as exec_info:
            raise DataAppendError("Error en afegir dades al full")
        assert str(exec_info.value) == "Error al afegir dades: Error en afegir dades al full"
