from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ShopCatalogConfig(AppConfig):
    name = 'shop.catalog'
    verbose_name = _('Shop catalog')
