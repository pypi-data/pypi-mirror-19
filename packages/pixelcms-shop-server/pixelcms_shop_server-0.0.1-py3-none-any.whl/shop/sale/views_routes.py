from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.decorators import permission_classes

from cms.common import utils

from shop.config.models import ShippingMethod
from .models import Order
from .serializers import (
    ShippingMethodSerializer, OrdersSerializer, OrderSerializer
)


@api_view()
def cart_view(request):
    return Response({
        'component_name': 'ShopCart',
        'component_data': {
            'methods': ShippingMethodSerializer(
                ShippingMethod.objects.filter(published=True),
                many=True,
                context={'request': request}
            ).data
        },
        'meta': utils.generate_meta(
            title=_('Cart')
        )
    })


@api_view()
@permission_classes((permissions.IsAuthenticated,))
def orders_view(request):
    return Response({
        'component_name': 'ShopOrders',
        'component_data': OrdersSerializer(
            request.user.customer,
            context={'request': request}
        ).data,
        'meta': utils.generate_meta(
            title=_('Shop orders')
        )
    })


@api_view()
@permission_classes((permissions.IsAuthenticated,))
def order_view(request, order_id):
    order = get_object_or_404(
        Order,
        customer=request.user.customer,
        order_id=order_id
    )
    return Response({
        'component_name': 'ShopOrder',
        'component_data': OrderSerializer(
            order,
            context={'request': request}
        ).data,
        'meta': utils.generate_meta(
            title=_('Shop order')
        )
    })
