from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from polymorphic.admin import PolymorphicChildModelAdmin

from .models import PayuPayment


@admin.register(PayuPayment)
class PayuPaymentAdmin(PolymorphicChildModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def order_link(self, obj):
        return '<a href="{}">{}</a>'.format(
            reverse('admin:shop_order_change', args=[obj.order.pk]),
            obj.order
        )
    order_link.short_description = _('Shop order')
    order_link.allow_tags = True

    def get_actions(self, request):
        actions = super(PayuPaymentAdmin, self).get_actions(request)
        del actions['duplicate']
        return actions

    base_model = PayuPayment
    readonly_fields = (
        # 'order' it has to be there
        # (weired bug making it unable to save otherwise)
        'order', 'gateway_name', 'order_link', 'created', 'total', 'success',
        'payment_uri', 'valid_until', 'internal_id', 'internal_status'
    )
    fieldsets = (
        (None, {
            'fields': (
                'gateway_name', 'order_link', 'created', 'total',
                'success', 'payment_uri', 'valid_until', 'internal_id',
                'internal_status'
            )
        }),
    )
