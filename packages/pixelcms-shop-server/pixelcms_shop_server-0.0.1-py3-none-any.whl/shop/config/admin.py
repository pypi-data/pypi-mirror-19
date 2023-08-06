from django.contrib import admin

from cms.common import mixins

from .models import TaxRule, PaymentMethod, ShippingMethod, EmailTemplate


@admin.register(TaxRule)
class TaxRuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'rate')
    search_fields = ('name',)

    change_list_template = 'admin/change_list_filter_sidebar.html'
    change_list_filter_template = 'admin/filter_listing.html'


@admin.register(ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'published', 'order', 'price',
        'set_waiting_for_shipping_status'
    )
    list_filter = ('published',)
    list_editable = ('published', 'order')

    filter_horizontal = ('payment_methods',)

    change_list_template = 'admin/change_list_filter_sidebar.html'
    change_list_filter_template = 'admin/filter_listing.html'


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'published', 'order', 'price',
        'set_waiting_for_payment_status', 'gateway'
    )
    list_filter = ('published',)
    list_editable = ('published', 'order')

    change_list_template = 'admin/change_list_filter_sidebar.html'
    change_list_filter_template = 'admin/filter_listing.html'

    class Media:
        js = mixins.TinyMCE.js


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('event', 'published', 'subject')
    list_filter = ('published',)
    list_editable = ('published',)
    seatch_fields = ('event', 'subject')

    change_list_template = 'admin/change_list_filter_sidebar.html'
    change_list_filter_template = 'admin/filter_listing.html'

    class Media:
        js = mixins.TinyMCE.js
