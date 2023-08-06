from django.conf.urls import url, include

from shop.catalog import urls_api as catalog_urls_api
from shop.sale import urls_api as sale_urls_api
from shop.payments import urls_api as payments_urls_api


urlpatterns = [
    url(
        r'^catalog/',
        include(catalog_urls_api, namespace='catalog')
    ),
    url(
        r'^sale/',
        include(sale_urls_api, namespace='sale')
    ),
    url(
        r'^payments/',
        include(payments_urls_api, namespace='payments')
    )
]
