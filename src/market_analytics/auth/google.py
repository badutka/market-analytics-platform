import json
from google.auth import default
from google.oauth2 import service_account


def get_google_credentials(settings):
    if settings.google_credentials_json:
        return service_account.Credentials.from_service_account_info(
            json.loads(settings.google_credentials_json)
        )

    if settings.google_credentials:
        return service_account.Credentials.from_service_account_file(
            settings.google_credentials
        )

    # Fall back to ADC (works on GCP)
    credentials, _ = default()
    return credentials
