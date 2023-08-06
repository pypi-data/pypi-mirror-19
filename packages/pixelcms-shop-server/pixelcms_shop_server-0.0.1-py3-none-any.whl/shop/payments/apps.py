from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ShopPaymentsConfig(AppConfig):
    name = 'shop.payments'
    verbose_name = _('Shop payments')
