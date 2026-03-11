import gspread
from formulari_app.lib.config import get_credentials

class GoogleClient:
    def __init__(self):
        self.credentials = get_credentials()

        # authorize the clientsheet
        try:
            self.client = gspread.Client(auth=self.credentials)

        except Exception as e:
            raise Exception(f'Error initializing GoogleClient: {str(e)}')
