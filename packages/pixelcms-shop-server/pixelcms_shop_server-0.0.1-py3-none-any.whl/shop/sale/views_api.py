from django.shortcuts import get_object_or_404, Http404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.decorators import permission_classes

from shop import settings as shop_settings
from .models import (
    Cart, CartProduct, CartProductOptionValue, Order, OrderProduct,
    OrderProductOption, OrderBillingData, OrderShippingData
)
from .serializers import (
    CartDataSerializer, AddToCartSerializer,
    CartChangeQuantitySerializer, RemoveFromCartSerializer,
    PlaceOrderSerializer
)
from .utils import get_cart


class GetCartView(generics.RetrieveAPIView):
    serializer_class = CartDataSerializer

    def get_object(self):
        cart = get_cart(self.request, self.kwargs.get('pk'))
        if not cart:
            raise Http404
        return cart


@api_view(['POST'])
def add_to_cart_view(request, cart_pk=None):
    serializer = AddToCartSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        cart = get_cart(request, cart_pk)
        if not cart:
            if request.user.is_authenticated:
                customer = request.user.customer
            else:
                customer = None
            cart = Cart.objects.create(customer=customer)

        # check if product with exact options is already in cart
        # if so use it, otherwise create new
        product = serializer.validated_data['product']
        options = serializer.validated_data['options']
        possible_objects = CartProduct.objects.filter(
            cart=cart,
            product=product
        )
        obj = None
        for possible_obj in possible_objects:
            # check if options match
            if len(possible_obj.options.all()) == len(options):
                obj = possible_obj
                for o in options:
                    if not possible_obj.options.filter(
                        options_group=o['options_group'],
                        option=o['option']
                    ).exists():
                        obj = None
                        break
                if obj:
                    break

        if obj:
            # product found so only quantity changes
            obj.quantity += serializer.validated_data['quantity']
            if obj.quantity > shop_settings.SHOP_QUANTITY_LIMIT:
                obj.quantity = shop_settings.SHOP_QUANTITY_LIMIT
            obj.save()
        else:
            # product not found so create new with options
            obj = CartProduct.objects.create(
                cart=cart,
                product=product,
                quantity=serializer.validated_data['quantity']
            )
            for o in options:
                CartProductOptionValue.objects.create(
                    cart_product=obj,
                    options_group=o['options_group'],
                    option=o['option']
                )
            obj.save()

        cart.refresh_from_db()
        return Response(
            CartDataSerializer(cart, context={'request': request}).data
        )


@permission_classes(permissions.IsAuthenticated)
@api_view(['POST'])
def bind_cart_view(request, pk):
    cart = get_object_or_404(Cart, customer=None, pk=pk)
    cart.customer = request.user.customer
    cart.save()
    return Response(
        CartDataSerializer(cart, context={'request': request}).data
    )


@api_view(['POST'])
def cart_change_quantity_view(request, cart_pk):
    if request.user.is_authenticated:
        customer = request.user.customer
    else:
        customer = None
    serializer = CartChangeQuantitySerializer(
        data=request.data,
        context={
            'customer': customer,
            'cart_pk': cart_pk
        }
    )
    if serializer.is_valid(raise_exception=True):
        cart_product = serializer.validated_data['product']
        cart_product.quantity = serializer.validated_data['quantity']
        cart_product.save()
        return Response(
            CartDataSerializer(
                cart_product.cart, context={'request': request}
            ).data
        )


@api_view(['POST'])
def remove_from_cart_view(request, cart_pk):
    if request.user.is_authenticated:
        customer = request.user.customer
    else:
        customer = None
    serializer = RemoveFromCartSerializer(
        data=request.data,
        context={
            'customer': customer,
            'cart_pk': cart_pk
        }
    )
    if serializer.is_valid(raise_exception=True):
        cart_product = serializer.validated_data['product']
        cart = cart_product.cart
        cart_product.delete()
        cart.save()
        return Response(
            CartDataSerializer(cart, context={'request': request}).data
        )


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def place_order_view(request, cart_pk):
    cart = get_object_or_404(
        Cart,
        customer=request.user.customer,
        pk=cart_pk
    )
    serializer = PlaceOrderSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        payment_method = serializer.validated_data['payment_method']
        shipping_method = serializer.validated_data['shipping_method']
        if payment_method.set_waiting_for_payment_status:
            order_status = 'WAITING_FOR_PAYMENT'
        elif shipping_method.set_waiting_for_shipping_status:
            order_status = 'WAITING_FOR_SHIPPING'
        else:
            order_status = 'COMPLETED'
        bd = serializer.validated_data['bd']
        if serializer.validated_data['shipping_data_form']:
            sd = serializer.validated_data['sd']
        else:
            sd = {
                'name': bd['name'],
                'address': bd['address'],
                'postal_code': bd['postal_code'],
                'place': bd['place'],
                'phone': bd.get('phone')
            }
        order = Order.objects.create(
            customer=cart.customer,
            shipping_method=shipping_method,
            payment_method=payment_method,
            status=order_status,
            additional_comment=serializer.validated_data
            .get('additional_comment')
        )
        for p in cart.products.all():
            order_product = OrderProduct.objects.create(
                order=order,
                product=p.product,
                product_name=p.product.name,
                unit_price=p.unit_price,
                quantity=p.quantity,
                subtotal=p.subtotal
            )
            for o in p.options.all():
                OrderProductOption.objects.create(
                    order_product=order_product,
                    options_group=o.options_group.name,
                    option=o.option.name,
                    price_mod=o.option.price_mod,
                    price_mod_percentage=o.option.price_mod_percentage
                )
        order.save()
        OrderBillingData.objects.create(
            order=order,
            **bd
        )
        OrderShippingData.objects.create(
            order=order,
            **sd
        )
        cart.delete()
        order.send_order_placed_emails()

        response_data = {
            'order_id': order.order_id,
            'order_status': order.get_status_display(),
            'payment_additional_info': order.payment_method
                                            .additional_info,
            'has_payment_gateway': payment_method.has_gateway
        }
        return Response(response_data)
