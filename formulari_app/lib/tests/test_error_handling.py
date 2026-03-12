import pytest
from formulari_app.lib.error_handling import PermissionDenied, WorksheetNotFound, SpreadsheetNotFound, APIError, DataAppendError

class TestErrors():
    def test_permission_denied(self):
        with pytest.raises(PermissionDenied) as exc_info:
            raise PermissionDenied("Acceso no autorizado")
        assert str(exc_info.value) == "Permiso denegado: Acceso no autorizado"

    def test_worksheetNotFound(self):
        with pytest.raises(WorksheetNotFound) as exc_info:
            raise WorksheetNotFound("Formulario")
        assert str(exc_info.value) == "Worksheet no encontrada: 'Formulario'"

    def test_SpreadsheetNotFound(self):
        with pytest.raises(SpreadsheetNotFound) as exec_info:
            raise SpreadsheetNotFound('1234')
        assert str(exec_info.value) == "Spreadsheet no encontrada: '1234'"

    def test_APIError(self):
        with pytest.raises(APIError) as exec_info:
            raise APIError("Error al conectar con la API")
        assert str(exec_info.value) == "Error de API: Error al conectar con la API"

    def test_DataAppendError(self):
        with pytest.raises(DataAppendError) as exec_info:
            raise DataAppendError("Error al añadir datos a la hoja")
        assert str(exec_info.value) == "Error al añadir datos: Error al añadir datos a la hoja"
