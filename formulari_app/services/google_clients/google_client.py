from formulari_app.lib.get_credentials import get_credentials

class GoogleClient:
    def __init__(self, creds):

        if not creds:
            raise ValueError("Authentication client is required to initialize GoogleClient.")

        self.creds = creds
    # authorize the clientsheet
    @classmethod
    def create_with_credentials(cls, credentials_args, scopes):
        creds = get_credentials(credentials_args, scopes)
        return creds
