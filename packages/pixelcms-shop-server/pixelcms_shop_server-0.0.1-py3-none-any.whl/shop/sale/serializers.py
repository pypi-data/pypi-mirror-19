from django.core.paginator import Paginator, InvalidPage
from django.shortcuts import Http404
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from shop import settings as shop_settings
from shop.catalog.models import Product
from .models import (
    Cart, CartProduct, CartProductOptionValue, PaymentMethod, ShippingMethod,
    OrderProductOption, OrderProduct, Order, Customer
)


class CartDataProductOptionSerializer(serializers.ModelSerializer):
    options_group = serializers.SerializerMethodField()
    option = serializers.SerializerMethodField()

    class Meta:
        model = CartProductOptionValue
        fields = ('options_group', 'option')

    def get_options_group(self, obj):
        return obj.options_group.name

    def get_option(self, obj):
        return obj.option.name


class CartDataProductSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    route = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    options = CartDataProductOptionSerializer(many=True)
    unit_price = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartProduct
        fields = (
            'pk', 'name', 'route', 'image', 'options', 'unit_price',
            'quantity', 'subtotal'
        )

    def get_name(self, obj):
        return obj.product.name

    def get_route(self, obj):
        return obj.product.route

    def get_image(self, obj):
        try:
            return obj.product.main_image.get_image(
                request=self.context['request'],
                version=shop_settings.SHOP_IMAGES_VERSIONS['product']['cart']
            )
        except AttributeError:
            return None

    def get_unit_price(self, obj):
        return str(obj.unit_price)

    def get_subtotal(self, obj):
        return str(obj.subtotal)


class CartDataSerializer(serializers.ModelSerializer):
    products = CartDataProductSerializer(many=True)
    timestamp = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = (
            'pk', 'products', 'products_count', 'total', 'timestamp'
        )

    def get_timestamp(self, obj):
        return obj.timestamp.timestamp()


class CartProductOptionValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProductOptionValue
        fields = (
            'options_group', 'option'
        )


class AddToCartSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter(
            published=True,
            category__published_with_parents=True,
            available=True
        )
    )
    options = CartProductOptionValueSerializer(many=True)
    quantity = serializers.IntegerField(
        min_value=1, max_value=shop_settings.SHOP_QUANTITY_LIMIT
    )

    def validate(self, data):
        product_options_groups = data['product'].options.all()
        for o in data['options']:
            if (
                o['options_group'] not in product_options_groups or
                o['option'] not in o['options_group'].options.all()
            ):
                raise serializers.ValidationError(_('Wrong option.'))
        return data


class CartChangeQuantitySerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=[])
    quantity = serializers.IntegerField(
        min_value=1, max_value=shop_settings.SHOP_QUANTITY_LIMIT
    )

    def __init__(self, *args, **kwargs):
        self.fields['product'].queryset = CartProduct.objects.filter(
            cart__customer=kwargs['context']['customer'],
            cart__pk=kwargs['context']['cart_pk']
        )
        super(CartChangeQuantitySerializer, self).__init__(*args, **kwargs)


class RemoveFromCartSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=[])

    def __init__(self, *args, **kwargs):
        self.fields['product'].queryset = CartProduct.objects.filter(
            cart__customer=kwargs['context']['customer'],
            cart__pk=kwargs['context']['cart_pk']
        )
        super(RemoveFromCartSerializer, self).__init__(*args, **kwargs)


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = (
            'pk', 'name', 'price', 'has_gateway'
        )


class ShippingMethodSerializer(serializers.ModelSerializer):
    payment_methods = PaymentMethodSerializer(many=True)

    class Meta:
        model = ShippingMethod
        fields = (
            'pk', 'name', 'price', 'payment_methods'
        )


class OrderBillingDataSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    vat_id = serializers.CharField(required=False, max_length=255)
    address = serializers.CharField(max_length=255)
    postal_code = serializers.CharField(max_length=255)
    place = serializers.CharField(max_length=255)
    phone = serializers.CharField(required=False, max_length=255)


class OrderShippingDataSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    address = serializers.CharField(max_length=255)
    postal_code = serializers.CharField(max_length=255)
    place = serializers.CharField(max_length=255)
    phone = serializers.CharField(required=False, max_length=255)


class PlaceOrderSerializer(serializers.ModelSerializer):
    bd = OrderBillingDataSerializer()
    shipping_data_form = serializers.BooleanField()
    sd = OrderShippingDataSerializer(required=False)

    class Meta:
        model = Order
        fields = (
            'shipping_method', 'payment_method', 'bd',
            'shipping_data_form', 'sd', 'additional_comment'
        )


class OrdersOrderSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'order_id', 'created', 'total', 'status'
        )

    def get_status(self, obj):
        return obj.get_status_display()


class OrdersSerializer(serializers.Serializer):
    orders = serializers.SerializerMethodField()
    pagination = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = (
            'orders', 'pagination'
        )

    @cached_property
    def _pagination(self):
        if shop_settings.SHOP_ORDERS_PAGINATION_ON_PAGE:
            query_page = self.context['request'].GET.get('page') or 1
            try:
                paginator = Paginator(
                    Order.objects.filter(customer=self.instance),
                    shop_settings.SHOP_ORDERS_PAGINATION_ON_PAGE
                )
                return paginator.page(query_page)
            except InvalidPage:
                raise Http404
        else:
            return None

    def get_orders(self, obj):
        if self._pagination:
            orders = self._pagination.object_list
        else:
            orders = Order.objects.filter(customer=obj)
        return OrdersOrderSerializer(
            orders,
            many=True,
            context={'request': self.context['request']}
        ).data

    def get_pagination(self, obj):
        if self._pagination and self._pagination.paginator.num_pages > 1:
            return {
                'count': self._pagination.paginator.count,
                'num_pages': self._pagination.paginator.num_pages,
                'current_page': self._pagination.number
            }
        else:
            return None


class OrderShippingMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingMethod
        fields = (
            'name', 'price'
        )


class OrderPaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = (
            'name', 'price', 'additional_info'
        )


class OrderProductOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProductOption
        fields = ('options_group', 'option')


class OrderProductSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    route = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    options = OrderProductOptionSerializer(many=True)
    unit_price = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrderProduct
        fields = (
            'pk', 'name', 'route', 'image', 'options', 'unit_price',
            'quantity', 'subtotal'
        )

    def get_name(self, obj):
        if obj.product:
            return obj.product.name
        else:
            return obj.product_name

    def get_route(self, obj):
        if obj:
            return obj.product.route
        else:
            return None

    def get_image(self, obj):
        try:
            return obj.product.main_image.get_image(
                request=self.context['request'],
                version=shop_settings.SHOP_IMAGES_VERSIONS['product']['cart']
            )
        except AttributeError:
            return None

    def get_unit_price(self, obj):
        return str(obj.unit_price)

    def get_subtotal(self, obj):
        return str(obj.subtotal)


class OrderSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    shipping_method = OrderShippingMethodSerializer()
    payment_method = OrderPaymentMethodSerializer()
    billing_data = OrderBillingDataSerializer()
    shipping_data = OrderShippingDataSerializer()
    products = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'order_id', 'created', 'status', 'create_payment_eligible',
            'shipping_method', 'payment_method', 'total', 'billing_data',
            'shipping_data', 'additional_comment', 'products'
        )

    def get_status(self, obj):
        return obj.get_status_display()

    def get_products(self, obj):
        return OrderProductSerializer(
            obj.products,
            many=True,
            context={'request': self.context['request']}
        ).data
