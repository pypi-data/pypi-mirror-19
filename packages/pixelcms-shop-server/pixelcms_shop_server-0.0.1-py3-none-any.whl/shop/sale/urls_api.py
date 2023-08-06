from django.conf.urls import url

from . import views_api


urlpatterns = [
    url(
        r'^get-cart/$',
        views_api.GetCartView.as_view(),
        name='get_cart'
    ),
    url(
        r'^get-cart/(?P<pk>[0-9a-f\-]{36})/$',
        views_api.GetCartView.as_view(),
        name='get_cart_by_pk'
    ),
    url(
        r'^add-to-cart/$',
        views_api.add_to_cart_view,
        name='add_to_cart'
    ),
    url(
        r'^add-to-cart/(?P<cart_pk>[0-9a-f\-]{36})/$',
        views_api.add_to_cart_view,
        name='add_to_cart_by_pk'
    ),
    url(
        r'^bind-cart/(?P<pk>[0-9a-f\-]{36})/$',
        views_api.bind_cart_view,
        name='bind_cart'
    ),
    url(
        r'^cart-change-quantity/(?P<cart_pk>[0-9a-f\-]{36})/$',
        views_api.cart_change_quantity_view,
        name='cart_change_quantity'
    ),
    url(
        r'^remove-from-cart/(?P<cart_pk>[0-9a-f\-]{36})/$',
        views_api.remove_from_cart_view,
        name='remove_from_cart'
    ),
    url(
        r'^place-order/(?P<cart_pk>[0-9a-f\-]{36})/$',
        views_api.place_order_view,
        name='place_order'
    )
]
