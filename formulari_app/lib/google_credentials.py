import os
from dotenv import load_dotenv
from formulari_app.lib.logger import logger

load_dotenv()

# Define required Google credential keys
REQUIRED_CREDENTIALS = [
    "GOOGLE_TYPE",
    "GOOGLE_PROJECT_ID",
    "GOOGLE_PRIVATE_KEY_ID",
    "GOOGLE_PRIVATE_KEY",
    "GOOGLE_CLIENT_EMAIL",
    "GOOGLE_CLIENT_ID",
    "GOOGLE_AUTH_URI",
    "GOOGLE_TOKEN_URI",
    "GOOGLE_AUTH_PROVIDER_X509_CERT_URL",
    "GOOGLE_CLIENT_X509_CERT_URL",
    "GOOGLE_UNIVERSE_DOMAIN",
]

# Validate all credentials are set on startup
logger.info("Validating Google credentials...")
missing_creds = [key for key in REQUIRED_CREDENTIALS if not os.getenv(key)]
if missing_creds:
    error_msg = f"Missing Google credentials: {', '.join(missing_creds)}"
    logger.error("%s", error_msg)
    raise ValueError(f"❌ {error_msg}")

logger.info("✅ All %d Google credentials validated successfully", len(REQUIRED_CREDENTIALS))

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
