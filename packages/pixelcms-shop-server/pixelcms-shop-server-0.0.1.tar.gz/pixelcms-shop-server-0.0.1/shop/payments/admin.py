from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from polymorphic.admin import PolymorphicParentModelAdmin

from .models import Payment
from .payu.models import PayuPayment


@admin.register(Payment)
class PaymentAdmin(PolymorphicParentModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def gateway_name(self, obj):
        return obj.gateway_name
    gateway_name.short_description = _('Gateway name')

    def internal_id(self, obj):
        return obj.get_internal_id()
    internal_id.short_description = _('Internal ID')

    def internal_status(self, obj):
        return obj.get_internal_status()
    internal_status.short_description = _('Internal status')

    def get_actions(self, request):
        actions = super(PaymentAdmin, self).get_actions(request)
        del actions['duplicate']
        return actions

    base_model = Payment
    child_models = (PayuPayment,)

    list_display = (
        'created', 'total', 'success', 'gateway_name', 'internal_id',
        'internal_status'
    )
