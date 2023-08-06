import requests

from . import settings as payu_settings


def get_oauth_token():
    oauth_request_data = {
        'grant_type': 'client_credentials',
        'client_id': payu_settings.PAYU_POS_ID,
        'client_secret': payu_settings.PAYU_MD5_KEY
    }
    try:
        oauth_request = requests.post(
            payu_settings.OAUTH_URL,
            data=oauth_request_data
        )
        response = oauth_request.json()
        return response['access_token']
    except:
        return False
