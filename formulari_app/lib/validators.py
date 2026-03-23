from pydantic import ValidationError, BaseModel
from formulari_app.models.models import FORMDATA
from formulari_app.lib.logger import logger


class FormDataValidator:
    @staticmethod
    def validate_and_convert(form_data: dict) -> FORMDATA:
        try:
            logger.debug("Validating form data: %s", form_data)

            # Extract individual fields
            nom = form_data.get("nom", "").strip()
            telefon = form_data.get("telefon", "").strip()
            persones = form_data.get("persones", "").strip()

            # Validate each field
            FormDataValidator._validate_nom(nom)
            FormDataValidator._validate_telefon(telefon)
            persones_int = FormDataValidator._validate_persones(persones)

            # Create validated model
            validated_data = FORMDATA(
                nom=nom,
                telefon=telefon,
                persones=str(persones_int)
            )

            logger.info("✅ Form data validated successfully: nom=%s, telefon=%s, persones=%d", nom, telefon, persones_int)
            return validated_data

        except ValueError as e:
            logger.error("Validation error: %s", e)
            raise
        except ValidationError as e:
            error_msg = f"Invalid form data: {e}"
            logger.error("%s", error_msg)
            raise ValueError(error_msg) from e
        except Exception as e:
            error_msg = f"Unexpected validation error: {e}"
            logger.error("%s", error_msg, exc_info=True)
            raise ValueError(error_msg) from e

    @staticmethod
    def _validate_nom(nom: str) -> None:
        if not nom:
            raise ValueError("El nom és obligatori")

        if len(nom) < 2:
            raise ValueError("El nom ha de tenir almenys 2 caràcters")

        if len(nom) > 100:
            raise ValueError("El nom no pot tenir més de 100 caràcters")

        # Check for valid characters (letters, spaces, hyphens, accents)
        valid_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ áéíóúàèìòùäëïöüÁÉÍÓÚÀÈÌÒÙÄËÏÖÜ '-")
        if not all(c in valid_chars for c in nom):
            raise ValueError("El nom conté caràcters no vàlids. Únicament lletres, espais i guions permettits")

    @staticmethod
    def _validate_telefon(telefon: str) -> None:

        if not telefon:
            raise ValueError("El telèfon és obligatori")

        if not telefon.isdigit():
            raise ValueError("El telèfon ha de contenir únicament dígits")

        if len(telefon) != 9:
            raise ValueError("El telèfon ha de tenir exactament 9 dígits")

        if not telefon.startswith(("6", "7", "8", "9")):
            raise ValueError("El telèfon no és vàlid per a España")

    @staticmethod
    def _validate_persones(persones: str) -> int:
        if not persones:
            raise ValueError("El nombre de participants és obligatori")

        try:
            persones_int = int(persones.strip())
        except ValueError:
            raise ValueError("El nombre de participants ha de ser un número enter")

        if persones_int < 1:
            raise ValueError("Ha de haver almenys 1 participant")

        if persones_int > 40:
            raise ValueError("Número màxim de participants: 40")

        return persones_int
