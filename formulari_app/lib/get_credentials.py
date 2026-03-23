from google.oauth2.service_account import Credentials
from formulari_app.lib.error_handling import PermissionDenied


def get_credentials(credentials: dict[str, str | None], scopes: list[str]) -> Credentials:
    missing = [k for k, v in credentials.items() if not v]
    if missing:
        raise PermissionDenied(f"Faltan cedenciales: {missing}")

    creds = Credentials.from_service_account_info(credentials, scopes=scopes)
    return creds
