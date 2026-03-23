import pytest
from formulari_app.lib.validators import FormDataValidator


class TestFormDataValidation:
    """Test form data validation and conversion."""
    
    def test_valid_form_data(self):
        """Test validation with valid data."""
        valid_data = {
            "nom": "Joan Martínez",
            "telefon": "612345678",
            "persones": "4"
        }
        result = FormDataValidator.validate_and_convert(valid_data)
        assert result.nom == "Joan Martínez"
        assert result.telefon == "612345678"
        assert result.persones == "4"
    
    def test_valid_name_variations(self):
        """Test valid names with accents and hyphens."""
        valid_names = [
            {"nom": "María José", "telefon": "612345678", "persones": "1"},
            {"nom": "Jean-Pierre", "telefon": "612345678", "persones": "2"},
            {"nom": "José María de los Ángeles", "telefon": "612345678", "persones": "3"},
        ]
        for data in valid_names:
            result = FormDataValidator.validate_and_convert(data)
            assert result.nom == data["nom"]
    
    def test_missing_nom(self):
        """Test missing name field."""
        with pytest.raises(ValueError, match="El nom és obligatori"):
            FormDataValidator.validate_and_convert({
                "telefon": "612345678",
                "persones": "1"
            })
    
    def test_nom_too_short(self):
        """Test name too short."""
        with pytest.raises(ValueError, match="almenys 2 caràcters"):
            FormDataValidator.validate_and_convert({
                "nom": "A",
                "telefon": "612345678",
                "persones": "1"
            })
    
    def test_nom_invalid_characters(self):
        """Test name with invalid characters."""
        with pytest.raises(ValueError, match="caràcters no vàlids"):
            FormDataValidator.validate_and_convert({
                "nom": "Joan@123",
                "telefon": "612345678",
                "persones": "1"
            })
    
    def test_missing_telefon(self):
        """Test missing phone."""
        with pytest.raises(ValueError, match="El telèfon és obligatori"):
            FormDataValidator.validate_and_convert({
                "nom": "Joan Martínez",
                "persones": "1"
            })
    
    def test_telefon_invalid_digits(self):
        """Test phone with non-digit characters."""
        with pytest.raises(ValueError, match="únicament dígits"):
            FormDataValidator.validate_and_convert({
                "nom": "Joan Martínez",
                "telefon": "612-345-678",
                "persones": "1"
            })
    
    def test_telefon_wrong_length(self):
        """Test phone with wrong number of digits."""
        with pytest.raises(ValueError, match="exactament 9 dígits"):
            FormDataValidator.validate_and_convert({
                "nom": "Joan Martínez",
                "telefon": "61234567",
                "persones": "1"
            })
    
    def test_telefon_invalid_start(self):
        """Test phone starting with invalid digit."""
        with pytest.raises(ValueError, match="no és vàlid per a España"):
            FormDataValidator.validate_and_convert({
                "nom": "Joan Martínez",
                "telefon": "512345678",
                "persones": "1"
            })
    
    def test_missing_persones(self):
        """Test missing participants count."""
        with pytest.raises(ValueError, match="obligatori"):
            FormDataValidator.validate_and_convert({
                "nom": "Joan Martínez",
                "telefon": "612345678"
            })
    
    def test_persones_not_number(self):
        """Test participants count not a number."""
        with pytest.raises(ValueError, match="número enter"):
            FormDataValidator.validate_and_convert({
                "nom": "Joan Martínez",
                "telefon": "612345678",
                "persones": "abc"
            })
    
    def test_persones_zero(self):
        """Test zero participants."""
        with pytest.raises(ValueError, match="almenys 1"):
            FormDataValidator.validate_and_convert({
                "nom": "Joan Martínez",
                "telefon": "612345678",
                "persones": "0"
            })
    
    def test_persones_over_max(self):
        """Test participants over max."""
        with pytest.raises(ValueError, match="màxim"):
            FormDataValidator.validate_and_convert({
                "nom": "Joan Martínez",
                "telefon": "612345678",
                "persones": "41"
            })
    
    def test_valid_persones_edge_cases(self):
        """Test valid edge cases for participants."""
        valid_cases = ["1", "2", "20", "39", "40"]
        for persones in valid_cases:
            result = FormDataValidator.validate_and_convert({
                "nom": "Joan Martínez",
                "telefon": "612345678",
                "persones": persones
            })
            assert result.persones == persones
    
    def test_form_data_with_whitespace(self):
        """Test form data is properly trimmed."""
        result = FormDataValidator.validate_and_convert({
            "nom": "  Joan Martínez  ",
            "telefon": "  612345678  ",
            "persones": "  5  "
        })
        assert result.nom == "Joan Martínez"
        assert result.telefon == "612345678"
        assert result.persones == "5"
