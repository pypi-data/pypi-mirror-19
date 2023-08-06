from django.conf import settings


TEST_POS_ID = 145227
TEST_MD5_KEY = '12f071174cb7eb79d4aac5bc2f07563f'
TEST_SECOND_MD5_KEY = '13a980d4f851f3d9a1cfc792fb1f5e50'
ENDPOINT_URL = 'https://secure.payu.com/api/v2_1/orders'
OAUTH_URL = 'https://secure.payu.com/pl/standard/user/oauth/authorize'

PAYU_POS_ID = getattr(settings, 'PAYU_POS_ID', TEST_POS_ID)
PAYU_MD5_KEY = getattr(settings, 'PAYU_MD5_KEY', TEST_MD5_KEY)
PAYU_SECOND_MD5_KEY = getattr(settings, 'PAYU_SECOND_MD5_KEY',
                              TEST_SECOND_MD5_KEY)
PAYU_ENDPOINT_URL = getattr(settings, 'ENDPOINT_URL', ENDPOINT_URL)
PAYU_OAUTH_URL = getattr(settings, 'OAUTH_URL', OAUTH_URL)
PAYU_VALIDITY_TIME = getattr(settings, 'PAYU_VALIDITY_TIME', 600)
