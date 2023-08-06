from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils.module_loading import import_string

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import permission_classes

from shop.sale.models import Order
from .exceptions import PaymentCreationError


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def create_payment_view(request, order_id):
    try:
        order = Order.objects.get(
            order_id=order_id,
            customer=request.user.customer
        )
        if order.create_payment_eligible:
            existing_payment = order.payments.filter(
                success=None,
                valid_until__gt=timezone.now()
            ).first()
            if existing_payment:
                payment = existing_payment
            else:
                gateway_model = import_string(order.payment_method.gateway)
                try:
                    payment = gateway_model.create(
                        order=order,
                        request=request
                    )
                except PaymentCreationError:
                    return Response(
                        data={
                            '_error': _('Error occurred during payment '
                                        'creation. Service may be temporary '
                                        'unavailable. Please try again in a '
                                        'moment.')
                        },
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
            return Response({
                'payment_uri': payment.payment_uri
            })
        else:
            if order.payments.filter(success=True).exists():
                return Response(
                    data={
                        '_error': _('Payment for this order has been already '
                                    'made.')
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                return Response(
                    data={
                        '_error': _('Payment is not available for this order.')
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
    except Order.DoesNotExist:
        return Response(
            data={'_error': _('Order not found.')},
            status=status.HTTP_400_BAD_REQUEST
        )
