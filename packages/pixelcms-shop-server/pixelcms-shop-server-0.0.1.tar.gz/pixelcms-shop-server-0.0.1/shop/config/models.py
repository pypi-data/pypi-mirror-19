from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core import validators

from shop.payments import PAYMENT_GATEWAY_CHOICES


class TaxRule(models.Model):
    name = models.CharField(_('name'), max_length=255)
    rate = models.DecimalField(_('rate [%]'), max_digits=6, decimal_places=2)

    class Meta:
        app_label = 'shop'
        ordering = ('name',)
        verbose_name = _('tax rule')
        verbose_name_plural = _('tax rules')

    def __str__(self):
        return self.name


class PaymentMethod(models.Model):
    name = models.CharField(_('name'), max_length=255)
    published = models.BooleanField(_('published'), default=True)
    order = models.PositiveSmallIntegerField(_('order'), default=0)
    price = models.DecimalField(
        _('price'), max_digits=18, decimal_places=2,
        validators=[validators.MinValueValidator(0)]
    )
    set_waiting_for_payment_status = models.BooleanField(
        _('set "Waiting for payment" status'), default=True
    )
    gateway = models.CharField(
        _('gateway'), max_length=255, choices=PAYMENT_GATEWAY_CHOICES,
        null=True, blank=True
    )
    additional_info = models.TextField(
        _('additional information'),
        help_text=_('This text will be presented to customer after placing an '
                    'order.'),
        null=True, blank=True
    )

    class Meta:
        app_label = 'shop'
        ordering = ('order',)
        verbose_name = _('payment method')
        verbose_name_plural = _('payment methods')

    def __str__(self):
        return '{} ({})'.format(self.name, self.price)

    @property
    def has_gateway(self):
        return bool(self.gateway)


class ShippingMethod(models.Model):
    name = models.CharField(_('name'), max_length=255)
    published = models.BooleanField(_('published'), default=True)
    order = models.PositiveSmallIntegerField(_('order'), default=0)
    price = models.DecimalField(
        _('price'), max_digits=18, decimal_places=2,
        validators=[validators.MinValueValidator(0)]
    )
    set_waiting_for_shipping_status = models.BooleanField(
        _('set "Waiting for shipping" status'), default=True
    )
    payment_methods = models.ManyToManyField(
        PaymentMethod, verbose_name=_('payment methods')
    )

    class Meta:
        app_label = 'shop'
        ordering = ('order',)
        verbose_name = _('shipping method')
        verbose_name_plural = _('shipping methods')

    def __str__(self):
        return '{} ({})'.format(self.name, self.price)


class EmailTemplate(models.Model):
    EMAIL_EVENT_CHOICES = (
        (
            'customer@order_placed',
            _('Order placement - (to customer)')
        ),
        (
            'customer@order_status_changed',
            _('Order status change (to customer)')
        ),
        (
            'admin@order_placed',
            _('Order placement - (to admin)')
        )
    )
    event = models.CharField(
        _('event'), max_length=255, choices=EMAIL_EVENT_CHOICES, unique=True
    )
    published = models.BooleanField(_('published'), default=True)
    subject = models.CharField(_('subject'), max_length=255)
    content = models.TextField(_('content'))

    class Meta:
        app_label = 'shop'
        ordering = ('event',)
        verbose_name = _('email template')
        verbose_name_plural = _('email templates')

    def __str__(self):
        return self.get_event_display()
