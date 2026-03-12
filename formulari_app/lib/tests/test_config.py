import pytest
from google.oauth2.service_account import Credentials
from formulari_app.lib.config import get_credentials
from formulari_app.lib.google_credentials import credentials, SCOPES
from formulari_app.lib.error_handling import PermissionDenied

false_credentials = {
    "project_id": "fake_project",
    "private_key_id": "fake_key_id",
    "private_key": "fake_key",
    "client_email": "fake_email",
    "client_id": "fake_client_id",
    "auth_uri": "fake_auth_uri",
    "token_uri": "fake_token_uri",
    "auth_provider_x509_cert_url": "fake_auth_provider_x509_cert_url",
    "client_x509_cert_url": "fake_client_x509_cert_url",
    "universe_domain": None,
}

class TestGetConfig:
    def test_credentials(self):
        assert get_credentials(credentials, SCOPES) is not None

    def test_credentials_type(self):
        assert isinstance(get_credentials(credentials, SCOPES), Credentials)

    def test_credentials_missing(self):
        with pytest.raises(PermissionDenied):
            get_credentials(false_credentials, SCOPES)
