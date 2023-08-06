from django.conf.urls import url, include

from . import views_api
from .payu import urls_api as payu_urls_api


urlpatterns = [
    url(
        r'^create-payment/(?P<order_id>[0-9A-Z\-]+)/$',
        views_api.create_payment_view,
        name='create_payment'
    ),
    url(
        r'^payu/',
        include(payu_urls_api, namespace='payu')
    )
]
