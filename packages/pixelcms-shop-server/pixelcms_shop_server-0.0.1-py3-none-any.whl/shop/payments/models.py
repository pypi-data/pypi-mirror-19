from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from polymorphic.models import PolymorphicModel

from shop.sale.models import Order


class Payment(PolymorphicModel):
    order = models.ForeignKey(
        Order, verbose_name=_('shop order'), related_name='payments'
    )
    created = models.DateTimeField(
        _('created'), auto_now_add=True
    )
    total = models.DecimalField(
        _('total'), max_digits=18, decimal_places=2, default=0
    )
    success = models.NullBooleanField(_('success'), default=None)
    payment_uri = models.CharField(_('payment URI'), max_length=255)
    valid_until = models.DateTimeField(_('valid until'))

    class Meta:
        app_label = 'shop'
        ordering = ('-created',)
        verbose_name = _('payment')
        verbose_name_plural = _('payments')

    def save(self, *args, **kwargs):
        super(Payment, self).save(*args, **kwargs)
        if self.success:
            order = self.order
            if order.shipping_method.set_waiting_for_shipping_status:
                order.status = 'WAITING_FOR_SHIPPING'
            else:
                order.status = 'COMPLETED'
            order.save()

    @property
    def gateway_name(self):
        return self.get_real_instance().GATEWAY_NAME

    @property
    def is_valid(self):
        return timezone.now() < self.valid_until

    def get_internal_id(self):
        return self.get_real_instance().internal_id

    def get_internal_status(self):
        return self.get_real_instance().get_internal_status_display()
