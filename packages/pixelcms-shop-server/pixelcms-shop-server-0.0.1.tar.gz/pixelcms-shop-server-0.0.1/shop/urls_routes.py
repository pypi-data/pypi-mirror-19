from django.conf.urls import url, include

from shop.catalog import urls_routes as catalog_urls_routes
from shop.sale import urls_routes as sale_urls_routes

urlpatterns = [
    url(
        r'^',
        include(catalog_urls_routes, namespace='catalog')
    ),
    url(
        r'^',
        include(sale_urls_routes, namespace='sale')
    )
]
