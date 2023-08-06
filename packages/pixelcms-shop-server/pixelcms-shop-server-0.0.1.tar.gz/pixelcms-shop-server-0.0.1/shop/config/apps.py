from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ShopConfigConfig(AppConfig):
    name = 'shop.config'
    verbose_name = _('Shop config')
