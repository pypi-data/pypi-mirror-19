from django.conf.urls import url

from . import views_api


urlpatterns = [
    url(
        r'^categories-module/$',
        views_api.CategoriesModuleView.as_view(),
        name='categories_module'
    ),
    url(
        r'^products-module/(?P<template_id>[0-9a-z\-_]+)/$',
        views_api.ProductsModuleView.as_view(),
        name='products_module'
    ),
]
