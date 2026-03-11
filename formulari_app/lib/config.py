import os
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from formulari_app.lib.error_handling import PermissionDenied

load_dotenv()

credentials = {
    "type": os.getenv("GOOGLE_TYPE"),
    "project_id": os.getenv("GOOGLE_PROJECT_ID"),
    "private_key_id": os.getenv("GOOGLE_PRIVATE_KEY_ID"),
    "private_key": os.getenv("GOOGLE_PRIVATE_KEY"),
    "client_email": os.getenv("GOOGLE_CLIENT_EMAIL"),
    "client_id": os.getenv("GOOGLE_CLIENT_ID"),
    "auth_uri": os.getenv("GOOGLE_AUTH_URI"),
    "token_uri": os.getenv("GOOGLE_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("GOOGLE_AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("GOOGLE_CLIENT_X509_CERT_URL"),
    "universe_domain": os.getenv("GOOGLE_UNIVERSE_DOMAIN"),
}

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_credentials() -> Credentials:
    missing = [k for k, v in credentials.items() if v is None]
    if missing:
        raise PermissionDenied(f"Faltan cedenciales: {missing}")

    creds = Credentials.from_service_account_info(credentials, scopes=SCOPES)
    print(creds)
    return creds
