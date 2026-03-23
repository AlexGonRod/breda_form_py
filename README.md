# 🥘 Formulari de la Breda - Form Application

A Reflex-based form application for managing event registrations with Google Sheets integration.

## Features

- ✅ Form submission to Google Sheets
- 📊 Real-time occupancy tracking
- 🔐 Google API authentication
- 📱 Responsive Catalan interface
- ⚡ Built with Reflex

## Prerequisites

- Python 3.13+
- Google Service Account with Sheets API access
- Environment variables configured

## Installation

### 1. Clone Repository
```bash
git clone <repository-url>
cd breda_formulari_reflex
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory with your Google credentials:

```env
# Google Service Account Credentials
GOOGLE_TYPE=service_account
GOOGLE_PROJECT_ID=your-project-id
GOOGLE_PRIVATE_KEY_ID=your-private-key-id
GOOGLE_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n
GOOGLE_CLIENT_EMAIL=your-service-account@your-project.iam.gserviceaccount.com
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_AUTH_URI=https://accounts.google.com/o/oauth2/auth
GOOGLE_TOKEN_URI=https://oauth2.googleapis.com/token
GOOGLE_AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
GOOGLE_CLIENT_X509_CERT_URL=your-cert-url
GOOGLE_UNIVERSE_DOMAIN=googleapis.com

# Google Sheets Configuration
GOOGLE_ACTES_SPREADSHEET_ID=your-spreadsheet-id

# Application Configuration
MAX_PERSONS=40  # Maximum participants per event (default: 40)
```

**How to get Google credentials:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the Google Sheets API
4. Create a Service Account
5. Generate a private key (JSON)
6. Copy the credentials into your `.env` file

## Running Locally

### Development Mode
```bash
reflex run
```
The application will be available at `http://localhost:3000`

### Production Mode
```bash
reflex export
reflex deploy
```

## Testing

Run the test suite:
```bash
pytest formulari_app/lib/tests/ -v
```

## Deployment

### Using Railway.app (Recommended)

1. Connect your GitHub repository
2. Add environment variables in Railway dashboard
3. Railway will automatically detect and deploy the Reflex app

See [railway.json](railway.json) for platform configuration.

### Manual Deployment

1. Build the production bundle:
   ```bash
   reflex export
   ```

2. Deploy using your hosting service (Railway, Vercel, etc.)

3. Set all environment variables in your hosting platform

## Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_TYPE` | ✅ | Service account type (always "service_account") |
| `GOOGLE_PROJECT_ID` | ✅ | Google Cloud project ID |
| `GOOGLE_PRIVATE_KEY_ID` | ✅ | Private key ID from service account |
| `GOOGLE_PRIVATE_KEY` | ✅ | Private key (with escaped newlines) |
| `GOOGLE_CLIENT_EMAIL` | ✅ | Service account email |
| `GOOGLE_CLIENT_ID` | ✅ | Client ID from service account |
| `GOOGLE_AUTH_URI` | ✅ | OAuth auth URI |
| `GOOGLE_TOKEN_URI` | ✅ | OAuth token URI |
| `GOOGLE_AUTH_PROVIDER_X509_CERT_URL` | ✅ | Certificate URL |
| `GOOGLE_CLIENT_X509_CERT_URL` | ✅ | Client certificate URL |
| `GOOGLE_UNIVERSE_DOMAIN` | ✅ | Universe domain (usually googleapis.com) |
| `GOOGLE_ACTES_SPREADSHEET_ID` | ✅ | Google Sheets ID to store responses |
| `MAX_PERSONS` | ❌ | Max participants per event (default: 40) |

## Project Structure

```
breda_formulari_reflex/
├── formulari_app/
│   ├── __init__.py
│   ├── formulari_app.py          # Main app entry point
│   ├── lib/                      # Utilities
│   │   ├── error_handling.py     # Custom exceptions
│   │   ├── google_credentials.py # Credential loading/validation
│   │   └── tests/                # Unit tests
│   ├── models/                   # Data models
│   │   └── models.py
│   ├── pages/                    # Page components
│   │   └── formulari/
│   ├── services/                 # Business logic
│   │   ├── sheets_service.py
│   │   └── google_clients/
│   └── assets/                   # Images, favicon
├── pyproject.toml                # Project metadata
├── README.md                      # This file
└── rxconfig.py                   # Reflex configuration
```

## Troubleshooting

### "Missing Google credentials" error
- Check that all environment variables in `.env` are set
- Verify the `.env` file is in the root directory
- Restart the application after updating `.env`

### "Spreadsheet not found" error
- Verify `GOOGLE_ACTES_SPREADSHEET_ID` is correct
- Ensure the service account has access to the spreadsheet
- Check that the spreadsheet has the required worksheets

### API Rate Limiting (429 error)
- Reduce the frequency of form submissions
- Contact Google Cloud support to increase quota

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add/update tests
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues or questions, contact: `bredainfocat@gmail.com`
