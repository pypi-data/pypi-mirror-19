from django.conf.urls import url

from . import views_api


urlpatterns = [
    url(
        r'^notify/$',
        views_api.notify_view,
        name='notify'
    )
]
