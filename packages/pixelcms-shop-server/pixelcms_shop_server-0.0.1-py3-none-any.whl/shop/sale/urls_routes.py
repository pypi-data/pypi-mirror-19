from django.conf.urls import url

from . import views_routes


urlpatterns = [
    url(
        r'^cart/$',
        views_routes.cart_view,
        name='cart'
    ),
    url(
        r'^orders/$',
        views_routes.orders_view,
        name='orders'
    ),
    url(
        r'^orders/(?P<order_id>[0-9A-Z\-]+)/$',
        views_routes.order_view,
        name='order'
    )
]
