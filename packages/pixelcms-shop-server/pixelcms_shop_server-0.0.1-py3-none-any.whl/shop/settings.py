from django.conf import settings
from django.utils.translation import ugettext_lazy as _


SHOP_CURRENCY = getattr(settings, 'SHOP_CURRENCY', '')
SHOP_PRODUCTS_PAGINATION_ON_PAGE = getattr(
    settings, 'SHOP_PRODUCTS_PAGINATION_ON_PAGE', 10
)
SHOP_QUANTITY_LIMIT = getattr(
    settings, 'SHOP_QUANTITY_LIMIT', 1000
)
SHOP_IMAGES_VERSIONS = getattr(
    settings, 'SHOP_IMAGES_VERSIONS', {
        'product': {
            'category_view': 'shop_product_small',
            'product_view_thumbnail': 'shop_product_small',
            'product_view_full_size': 'shop_product_big',
            'module': 'shop_product_small',
            'cart': 'shop_product_small'
        },
        'category': {
            'category_view': 'shop_category_big',
            'subcategory': 'shop_category_small',
            'module': 'shop_category_small'
        }
    }
)
SHOP_ORDER_STATUS_CHOICES = getattr(
    settings, 'SHOP_ORDER_STATUS_CHOICES', (
        ('WAITING_FOR_PAYMENT', _('Waiting for payment')),
        ('WAITING_FOR_SHIPPING', _('Waiting for shipping')),
        ('COMPLETED', _('Completed')),
    )
)
SHOP_ORDERS_PAGINATION_ON_PAGE = getattr(
    settings, 'SHOP_ORDERS_PAGINATION_ON_PAGE', 10
)
SHOP_PAYMENTS_GATES = getattr(
    settings, 'SHOP_PAYMENTS_GATES', ()
)
ADMIN_EMAILS_RECIPIENTS = getattr(
    settings, 'ADMIN_EMAILS_RECIPIENTS', 'admin@localhost'
)
