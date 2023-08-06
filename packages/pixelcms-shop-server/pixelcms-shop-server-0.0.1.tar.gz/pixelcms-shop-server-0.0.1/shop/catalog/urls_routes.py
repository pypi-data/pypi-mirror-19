from django.conf.urls import url

from . import views_routes


urlpatterns = [
    url(
        r'^c/(?P<slug>[0-9a-z\-_]+),(?P<pk>[0-9]+)/$',
        views_routes.category_view,
        name='category'
    ),
    url(
        r'^p/(?P<slug>[0-9a-z\-_]+),(?P<pk>[0-9]+)/$',
        views_routes.product_view,
        name='product'
    )
]
