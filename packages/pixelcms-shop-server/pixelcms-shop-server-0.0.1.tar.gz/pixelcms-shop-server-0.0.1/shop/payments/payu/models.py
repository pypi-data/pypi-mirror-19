import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils import timezone

import requests
from ipware.ip import get_real_ip, get_ip

from shop.payments.models import Payment
from shop.sale.models import OrderProduct
from shop.payments.exceptions import PaymentCreationError
from shop import settings as shop_settings
from .utils import get_oauth_token
from . import settings as payu_settings


STATUS_CHOICES = (
    ('NEW', _('New')),
    ('PENDING', _('Pending')),
    ('WAITING_FOR_CONFIRMATION', _('Waiting for confirmation')),
    ('COMPLETED', _('Completed')),
    ('CANCELED', _('Canceled')),
    ('REJECTED', _('Rejected')),
)


class PayuPayment(Payment):
    GATEWAY_NAME = 'PayU'
    internal_id = models.CharField(_('PayU order ID'), max_length=255)
    internal_status = models.CharField(
        _('status'), max_length=255, choices=STATUS_CHOICES, default='NEW'
    )

    class Meta:
        app_label = 'shop'

    def save(self, *args, **kwargs):
        if self.internal_status == 'COMPLETED':
            self.success = True
        elif self.internal_status in ('CANCELED', 'REJECTED'):
            self.success = False
        super(PayuPayment, self).save(*args, **kwargs)

    @classmethod
    def create(cls, order, request):
        products = [
            {
                'name': p.product.name,
                'unitPrice': int(p.product.price_gross * 100),
                'quantity': p.quantity
            }
            for p in OrderProduct.objects.filter(order=order)
        ]
        products.append({
            'name': '{} ({})'.format(
                _('Shipping'),
                order.shipping_method.name
            ),
            'unitPrice': int(order.shipping_method.price * 100),
            'quantity': 1
        })
        payment_request_data = {
            'extOrderId': '{}/{}'.format(
                order.order_id,
                len(order.payments.all()) + 1
            ),
            'notifyUrl': request.build_absolute_uri(
                reverse('shop_api:payments:payu:notify')
            ),
            'orderUrl': '{}/s/orders/{}'.format(
                settings.FRONTEND_ADDRESS, order.order_id
            ),
            'customerIp': get_real_ip(request) or get_ip(request),
            'merchantPosId': payu_settings.PAYU_POS_ID,
            'validityTime': payu_settings.PAYU_VALIDITY_TIME,
            'description': order.order_id,
            'currencyCode': shop_settings.SHOP_CURRENCY,
            'totalAmount': int(order.total * 100),
            'continueUrl': '{}/s/payment-return'
                           .format(settings.FRONTEND_ADDRESS),
            'settings': {'invoiceDisabled': True},
            'buyer': {
                'email': order.customer.user.email
            },
            'products': products
        }
        payment_request_headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(get_oauth_token())
        }
        try:
            r = requests.post(
                payu_settings.PAYU_ENDPOINT_URL,
                json=payment_request_data,
                headers=payment_request_headers,
                allow_redirects=False
            )
            r.raise_for_status()
            response = r.json()
            payment = cls.objects.create(
                order=order,
                total=order.total,
                internal_id=response['orderId'],
                payment_uri=response['redirectUri'],
                valid_until=(
                    timezone.now() +
                    datetime.timedelta(
                        seconds=payu_settings.PAYU_VALIDITY_TIME - 5
                    )
                )
            )
            return payment
        except:
            raise PaymentCreationError
