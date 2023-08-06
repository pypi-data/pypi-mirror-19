import uuid
from decimal import Decimal
import logging

from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from django.utils import timezone
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.template import Context, Template
from django.utils.html import mark_safe
from django.core.urlresolvers import reverse

from hashids import Hashids
from cms.emails.models import Message

from shop import settings as shop_settings
from shop.catalog.models import Product, ProductOptionsGroup, ProductOption
from shop.config.models import ShippingMethod, PaymentMethod, EmailTemplate


class Customer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, verbose_name=_('user'),
        on_delete=models.CASCADE
    )

    class Meta:
        app_label = 'shop'
        ordering = ('user',)
        verbose_name = _('customer')
        verbose_name_plural = _('customers')

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_hook(sender, instance, created, **kwargs):
    if created:
        Customer.objects.get_or_create(user=instance)


@receiver(post_delete, sender=Customer)
def delete_user_hook(sender, instance, **kwargs):
    try:
        instance.user.delete()
    except ObjectDoesNotExist:
        pass


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(
        Customer, verbose_name=_('customer'), null=True, blank=True,
        related_name='carts'
    )
    created = models.DateTimeField(_('created'), default=timezone.now)
    products_count = models.PositiveSmallIntegerField(
        _('products count'), default=0
    )
    total = models.DecimalField(
        _('total'), max_digits=18, decimal_places=2, default=0
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'shop'
        ordering = ('-created',)
        verbose_name = _('cart')
        verbose_name_plural = _('carts')

    def __str__(self):
        return str(self.total)

    def save(self, *args, **kwargs):
        self.products_count = self.products.aggregate(
            Sum(
                'quantity',
                output_field=models.PositiveSmallIntegerField()
            )
        )['quantity__sum'] or 0
        self.total = self.products.aggregate(
            Sum(
                'subtotal',
                output_field=models.DecimalField()
            )
        )['subtotal__sum'] or Decimal(0)
        super(Cart, self).save(*args, **kwargs)


class CartProduct(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, related_name='products')
    product = models.ForeignKey(Product, related_name='cart_products')
    unit_price = models.DecimalField(
        _('unit price'), max_digits=18, decimal_places=2
    )
    quantity = models.PositiveSmallIntegerField(_('quantity'))
    subtotal = models.DecimalField(
        _('subtotal'), max_digits=18, decimal_places=2
    )

    class Meta:
        app_label = 'shop'
        ordering = ('pk',)
        verbose_name = _('cart product')
        verbose_name_plural = _('cart products')

    def __str__(self):
        return self.product.name

    def save(self, *args, **kwargs):
        # save() automatically recalculates product and cart
        price = self.product.price_gross
        mod = Decimal(0)
        mod_percentage = Decimal(0)
        for o in self.options \
                .filter(option__price_mod__isnull=False) \
                .exclude(option__price_mod=0):
            if not o.option.price_mod_percentage:
                mod += o.option.price_mod
            else:
                mod_percentage += o.option.price_mod
        price += mod
        price += self.product.price_gross * mod_percentage / 100
        self.unit_price = round(price, 2)
        self.subtotal = self.unit_price * self.quantity
        super(CartProduct, self).save(*args, **kwargs)
        self.cart.save()

    def validate_required_options(self):
        required_options_pks = self.product.required_options \
            .values_list('pk', flat=True)
        present_options_pks = self.options.all() \
            .values_list('options_group__pk', flat=True)
        if set(required_options_pks) == set(present_options_pks):
            return True
        else:
            return False


@receiver(post_delete, sender=CartProduct)
def delete_cart_product_hook(sender, instance, **kwargs):
    instance.cart.save()


class CartProductOptionValue(models.Model):
    cart_product = models.ForeignKey(CartProduct, related_name='options')
    options_group = models.ForeignKey(ProductOptionsGroup)
    option = models.ForeignKey(ProductOption)

    class Meta:
        app_label = 'shop'
        ordering = ('pk',)
        unique_together = (('cart_product', 'options_group'),)
        verbose_name = _('option')
        verbose_name_plural = _('options')


@receiver(post_delete, sender=CartProductOptionValue)
def delete_cart_product_option_value_hook(sender, instance, **kwargs):
    try:
        cart_product = instance.cart_product
        valid = cart_product.validate_required_options()
        if valid:
            cart_product.save()
        else:
            cart_product.delete()
    except CartProduct.DoesNotExist:
        # this happens when deleting product from cart
        pass


class Order(models.Model):
    order_id = models.CharField(
        _('order ID'), max_length=255, null=True, blank=True
        # null=True because order_id is generated in response for post_save
        # signal, based on actual object pk
    )
    customer = models.ForeignKey(
        Customer, verbose_name=_('customer'), related_name='orders'
    )
    created = models.DateTimeField(_('created'), default=timezone.now)
    shipping_method = models.ForeignKey(
        ShippingMethod, verbose_name=_('shipping method'),
        related_name='orders'
    )
    payment_method = models.ForeignKey(
        PaymentMethod, verbose_name=_('payment method'), related_name='orders'
    )
    total = models.DecimalField(
        _('total'), max_digits=18, decimal_places=2,
        validators=[validators.MinValueValidator(0)],
        help_text=_('includes the cost of shipping and payment')
    )
    status = models.CharField(
        _('status'), max_length=255,
        choices=shop_settings.SHOP_ORDER_STATUS_CHOICES
    )
    additional_comment = models.TextField(
        _('additional comment'), null=True, blank=True
    )

    class Meta:
        app_label = 'shop'
        ordering = ('-created',)
        verbose_name = _('shop order')
        verbose_name_plural = _('shop orders')

    def __str__(self):
        return str(self.order_id)

    def save(self, *args, **kwargs):
        self.total = (
            self.products_total +
            self.shipping_method.price +
            self.payment_method.price
        )
        if self.pk:
            orig = Order.objects.get(pk=self.pk)
            if orig.status != self.status:
                self.send_order_status_changed_email()
        super(Order, self).save(*args, **kwargs)

    def send_order_placed_emails(self):
        try:
            template = EmailTemplate.objects.get(event='customer@order_placed')
            context = Context({
                'order_id': self.order_id,
                'order_status': self.get_status_display(),
                'order_link': mark_safe('<a href="{0}">{0}</a>'.format(
                    '{}/s/orders/{}'.format(
                        settings.FRONTEND_ADDRESS, self.order_id
                    )
                ))
            })
            Message.objects.create(
                subject=Template(template.subject).render(context),
                recipients=self.customer.user.email,
                content=Template(template.content).render(context),
                reply_to='no-reply'
            )
        except EmailTemplate.DoesNotExist:
            logger = logging.getLogger(__name__)
            logger.error(
                'Error while sending email. Template customer@order_placed '
                'does not exists.'
            )
        try:
            template = EmailTemplate.objects.get(event='admin@order_placed')
            context = Context({
                'order_link': mark_safe('<a href="{0}">{0}</a>'.format(
                    '{}{}'.format(
                        settings.BACKEND_ADDRESS,
                        reverse('admin:shop_order_change', args=(self.pk,))
                    )
                ))
            })
            Message.objects.create(
                subject=Template(template.subject).render(context),
                recipients=shop_settings.ADMIN_EMAILS_RECIPIENTS,
                content=Template(template.content).render(context),
                reply_to='no-reply'
            )
        except EmailTemplate.DoesNotExist:
            logger = logging.getLogger(__name__)
            logger.error(
                'Error while sending email. Template admin@order_placed '
                'does not exists.'
            )

    def send_order_status_changed_email(self):
        try:
            template = EmailTemplate.objects \
                .get(event='customer@order_status_changed')
            context = Context({
                'order_id': self.order_id,
                'order_status': self.get_status_display(),
                'order_link': mark_safe('<a href="{0}">{0}</a>'.format(
                    '{}/s/orders/{}'.format(
                        settings.FRONTEND_ADDRESS, self.order_id
                    )
                ))
            })
            Message.objects.create(
                subject=Template(template.subject).render(context),
                recipients=self.customer.user.email,
                content=Template(template.content).render(context),
                reply_to='no-reply'
            )
        except EmailTemplate.DoesNotExist:
            logger = logging.getLogger(__name__)
            logger.error(
                'Error while sending email. Template '
                'customer@order_status_changed does not exists.'
            )

    @property
    def products_total(self):
        return self.products.aggregate(
            Sum(
                'subtotal',
                output_field=models.DecimalField()
            )
        )['subtotal__sum'] or 0

    @property
    def create_payment_eligible(self):
        return (
            self.payment_method.has_gateway and
            self.status == 'WAITING_FOR_PAYMENT' and
            not self.payments.filter(success=True).exists()
        )


@receiver(post_save, sender=Order)
def generate_order_id(sender, instance, created, **kwargs):
    if created:
        hashids = Hashids(
            salt=settings.SECRET_KEY,
            alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ',
            min_length=6
        )
        now = timezone.now()
        instance.order_id = '{}-{}-{}'.format(
            now.year,
            now.month,
            hashids.encode(instance.pk)
        )
        instance.save()


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, related_name='products')
    product = models.ForeignKey(
        Product, verbose_name=_('product'), null=True,
        on_delete=models.SET_NULL
    )
    product_name = models.CharField(_('name'), max_length=255)
    unit_price = models.DecimalField(
        _('unit price'), max_digits=18, decimal_places=2
    )
    quantity = models.PositiveSmallIntegerField(_('quantity'))
    subtotal = models.DecimalField(
        _('subtotal'), max_digits=18, decimal_places=2
    )

    class Meta:
        app_label = 'shop'
        ordering = ('pk',)
        verbose_name = _('order product')
        verbose_name_plural = _('order products')


class OrderProductOption(models.Model):
    order_product = models.ForeignKey(OrderProduct, related_name='options')
    options_group = models.CharField(_('options group'), max_length=255)
    option = models.CharField(_('option'), max_length=255)
    price_mod = models.DecimalField(
        _('price modification'), max_digits=18, decimal_places=2,
        null=True, blank=True
    )
    price_mod_percentage = models.BooleanField(_('percentage'), default=False)

    class Meta:
        app_label = 'shop'
        ordering = ('pk',)
        verbose_name = _('option')
        verbose_name_plural = _('options')


class OrderBillingData(models.Model):
    order = models.OneToOneField(Order, related_name='billing_data')
    name = models.CharField(
        _('first and last name / company name'), max_length=255
    )
    vat_id = models.CharField(
        _('VAT ID'), max_length=255, null=True, blank=True
    )
    address = models.CharField(_('address'), max_length=255)
    postal_code = models.CharField(_('postal code'), max_length=255)
    place = models.CharField(_('place'), max_length=255)
    phone = models.CharField(
        _('phone'), max_length=255, null=True, blank=True
    )

    class Meta:
        app_label = 'shop'
        verbose_name = _('billing data')
        verbose_name_plural = _('billing data')

    def __str__(self):
        return ''


class OrderShippingData(models.Model):
    order = models.OneToOneField(Order, related_name='shipping_data')
    name = models.CharField(
        _('first and last name / company name'), max_length=255
    )
    address = models.CharField(_('address'), max_length=255)
    postal_code = models.CharField(_('postal code'), max_length=255)
    place = models.CharField(_('place'), max_length=255)
    phone = models.CharField(
        _('phone'), max_length=255, null=True, blank=True
    )

    class Meta:
        app_label = 'shop'
        verbose_name = _('shipping data')
        verbose_name_plural = _('shipping data')

    def __str__(self):
        return ''
