from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from polymorphic.admin import (
    PolymorphicInlineSupportMixin
)

from shop.payments.models import Payment
from .models import (
    Customer, Cart, CartProduct, Order, OrderProduct, OrderBillingData,
    OrderShippingData
)


class CustomerOrderInline(admin.TabularInline):
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def order_link(self, obj):
        return '<a href="{}">{}</a>'.format(
            reverse('admin:shop_order_change', args=[obj.pk]),
            obj.order_id
        )
    order_link.short_description = _('Order ID')
    order_link.allow_tags = True

    model = Order
    extra = 0
    fields = (
        'order_link', 'created', 'total', 'shipping_method', 'payment_method',
        'status'
    )
    readonly_fields = (
        'order_link', 'created', 'total', 'shipping_method', 'payment_method',
        'status'
    )


class CustomerCartInline(admin.TabularInline):
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def cart_link(self, obj):
        return '<a href="{}">{}</a>'.format(
            reverse('admin:shop_cart_change', args=[obj.pk]),
            str(obj.total)
        )
    cart_link.short_description = _('Total')
    cart_link.allow_tags = True

    model = Cart
    extra = 0
    fields = ('cart_link', 'products_count', 'created')
    readonly_fields = ('cart_link', 'products_count', 'created')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def email(self, obj):
        return obj.user.email
    email.short_description = _('Email')
    email.admin_order_field = 'user__email'

    def user_link(self, obj):
        return '<a href="{}">{}</a>'.format(
            reverse('admin:auth_user_change', args=[obj.user.pk]),
            obj.user
        )
    user_link.short_description = _('User')
    user_link.allow_tags = True

    def get_actions(self, request):
        actions = super(CustomerAdmin, self).get_actions(request)
        del actions['duplicate']
        return actions

    list_display = (
        'user', 'email'
    )
    search_fields = (
        'user__username', 'user__email'
    )
    readonly_fields = ('user_link', 'email')

    fieldsets = (
        (None, {
            'fields': (
                'user_link', 'email'
            )
        }),
    )

    inlines = (CustomerOrderInline, CustomerCartInline,)

    change_list_template = 'admin/change_list_filter_sidebar.html'
    change_list_filter_template = 'admin/filter_listing.html'


class CartProductInline(admin.TabularInline):
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def product_link(self, obj):
        return '<a href="{}">{}</a>'.format(
            reverse('admin:shop_product_change', args=[obj.product.pk]),
            obj.product
        )
    product_link.short_description = _('Product')
    product_link.allow_tags = True

    def product_image(self, obj):
        try:
            return '<img src="{}" alt="" />'.format(
                obj.product.main_image.image.original
                   .version_generate('admin_thumbnail').url
            )
        except (AttributeError, OSError):
            return ''
    product_image.short_description = _('Image')
    product_image.allow_tags = True

    def options(self, obj):
        options_list = []
        for o in obj.options.all():
            output = '{}: {}'.format(o.options_group.name, o.option.name)
            if o.option.price_mod:
                if o.option.price_mod > 0:
                    prefix = '+'
                else:
                    prefix = ''
                if o.option.price_mod_percentage:
                    suffix = '%'
                else:
                    suffix = ''
                output += ' ({}{}{})'.format(
                    prefix, o.option.price_mod, suffix
                )
            options_list.append(output)
        return '<br />'.join(options_list)
    options.short_description = _('Options')
    options.allow_tags = True

    model = CartProduct
    extra = 0
    fields = (
        'product_link', 'product_image', 'options', 'unit_price', 'quantity',
        'subtotal'
    )
    readonly_fields = (
        'product_link', 'product_image', 'options', 'unit_price', 'quantity',
        'subtotal'
    )


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def save_formset(self, request, form, formset, change):
        formset.save()  # save children
        form.instance.save()  # save parent

    def customer_link(self, obj):
        if obj.customer:
            return '<a href="{}">{}</a>'.format(
                reverse('admin:shop_customer_change', args=[obj.customer.pk]),
                obj.customer
            )
        else:
            return ''
    customer_link.short_description = _('Customer')
    customer_link.allow_tags = True

    def get_actions(self, request):
        actions = super(CartAdmin, self).get_actions(request)
        del actions['duplicate']
        return actions

    list_display = ('total', 'products_count', 'created', 'customer')
    search_fields = (
        'customer__user__username', 'customer__user__email',
        'customer__user__first_name', 'customer__user__last_name'
    )
    readonly_fields = (
        'id', 'created', 'customer_link', 'products_count', 'total'
    )

    fieldsets = (
        (None, {
            'fields': (
                'id', 'created', 'customer_link'
            )
        }),
        (None, {
            'classes': ('placeholder products-group',),
            'fields': ()
        }),
        (_('Total'), {
            'fields': ('products_count', 'total')
        })
    )

    inlines = (CartProductInline,)

    change_list_template = 'admin/change_list_filter_sidebar.html'
    change_list_filter_template = 'admin/filter_listing.html'


class OrderProductInline(admin.TabularInline):
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def product_or_product_name(self, obj):
        if obj.product:
            return '<a href="{}">{}</a>'.format(
                reverse('admin:shop_product_change', args=[obj.product.pk]),
                obj.product
            )
        else:
            return obj.product_name
    product_or_product_name.short_description = _('Product')
    product_or_product_name.allow_tags = True

    def product_image(self, obj):
        try:
            return '<img src="{}" alt="" />'.format(
                obj.product.main_image.image.original
                   .version_generate('admin_thumbnail').url
            )
        except (AttributeError, OSError):
            return ''
    product_image.short_description = _('Image')
    product_image.allow_tags = True

    def options(self, obj):
        options_list = []
        for o in obj.options.all():
            output = '{}: {}'.format(o.options_group, o.option)
            if o.price_mod:
                if o.price_mod > 0:
                    prefix = '+'
                else:
                    prefix = ''
                if o.price_mod_percentage:
                    suffix = '%'
                else:
                    suffix = ''
                output += ' ({}{}{})'.format(
                    prefix, o.price_mod, suffix
                )
            options_list.append(output)
        return '<br />'.join(options_list)
    options.short_description = _('Options')
    options.allow_tags = True

    model = OrderProduct
    extra = 0
    fields = (
        'product_or_product_name', 'product_image', 'options', 'unit_price',
        'quantity', 'subtotal'
    )
    readonly_fields = (
        'product_or_product_name', 'product_image', 'options', 'unit_price',
        'quantity', 'subtotal'
    )


class OrderBillingDataInline(admin.StackedInline):
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    model = OrderBillingData
    extra = 0


class OrderShippingDataInline(admin.StackedInline):
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    model = OrderShippingData
    extra = 0


class PaymentInlineAdmin(admin.TabularInline):
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def details_link(self, obj):
        return '<a href="{}">{}</a>'.format(
            reverse('admin:shop_payment_change', args=[obj.pk]),
            _('Details')
        )
    details_link.short_description = ''
    details_link.allow_tags = True

    def gateway_name(self, obj):
        return obj.gateway_name
    gateway_name.short_description = _('Gateway name')

    def internal_id(self, obj):
        return obj.get_internal_id()
    internal_id.short_description = _('Internal ID')

    def internal_status(self, obj):
        return obj.get_internal_status()
    internal_status.short_description = _('Internal status')

    model = Payment
    extra = 0
    fields = (
        'created', 'total', 'success', 'gateway_name', 'internal_id',
        'internal_status', 'details_link'
    )
    readonly_fields = (
        'created', 'total', 'success', 'gateway_name', 'internal_id',
        'internal_status', 'details_link'
    )


@admin.register(Order)
class OrderAdmin(PolymorphicInlineSupportMixin, admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def customer_link(self, obj):
        return '<a href="{}">{}</a>'.format(
            reverse('admin:shop_customer_change', args=[obj.customer.pk]),
            obj.customer
        )
    customer_link.short_description = _('Customer')
    customer_link.allow_tags = True

    def products_total(self, obj):
        return obj.products_total
    products_total.short_description = _('Products total')

    def get_actions(self, request):
        actions = super(OrderAdmin, self).get_actions(request)
        del actions['duplicate']
        return actions

    list_display = (
        'order_id', 'customer_link', 'created', 'total',
        'shipping_method', 'payment_method', 'status'
    )
    list_filter = ('shipping_method', 'payment_method')
    readonly_fields = (
        'order_id', 'customer_link', 'created', 'products_total',
        'customer_link', 'total'
    )
    search_fields = (
        'order_id', 'customer__user__username', 'customer__user__email',
        'customer__user__first_name', 'customer__user__last_name'
    )

    fieldsets = (
        (None, {
            'fields': (
                'order_id', 'customer_link', 'created', 'products_total',
                'shipping_method', 'payment_method', 'total', 'status'
            )
        }),
        (None, {
            'classes': ('placeholder products-group',),
            'fields': ()
        }),
        (None, {
            'classes': ('placeholder billing_data-group',),
            'fields': ()
        }),
        (None, {
            'classes': ('placeholder shipping_data-group',),
            'fields': ()
        }),
        (_('Additional'), {
            'fields': (
                'additional_comment',
            )
        }),
        (None, {
            'classes': ('placeholder payments-group',),
            'fields': ()
        })
    )

    inlines = (
        OrderProductInline, OrderBillingDataInline, OrderShippingDataInline,
        PaymentInlineAdmin
    )

    change_list_template = 'admin/change_list_filter_sidebar.html'
    change_list_filter_template = 'admin/filter_listing.html'

    class Media:
        js = ['admin/shop/sale/orderBillingShippingData.js']
