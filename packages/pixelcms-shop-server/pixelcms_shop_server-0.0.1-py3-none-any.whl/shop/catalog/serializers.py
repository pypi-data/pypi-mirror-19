from django.core.paginator import Paginator, InvalidPage
from django.shortcuts import Http404
from django.utils.functional import cached_property

from rest_framework import serializers
from cms.common import mixins

from shop import settings as shop_settings
from .models import (
    Category, Product, ProductImage, ProductAttributeValue,
    ProductOptionsGroup, ProductOption, ProductsModule
)


class CategorySubcategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = (
            'pk', 'name', 'route', 'image'
        )

    def get_image(self, obj):
        return obj.get_thumbnail_or_image(
            request=self.context['request'],
            version=shop_settings.SHOP_IMAGES_VERSIONS['category']
            ['subcategory']
        )


class CategoryProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'pk', 'name', 'route', 'image', 'price'
        )

    def get_image(self, obj):
        try:
            return obj.main_image.get_image(
                request=self.context['request'],
                version=shop_settings.SHOP_IMAGES_VERSIONS['product']
                ['category_view']
            )
        except AttributeError:
            return None

    def get_price(self, obj):
        return str(obj.price_gross)


class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    subcategories = CategorySubcategorySerializer(many=True)
    products = serializers.SerializerMethodField()
    pagination = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = (
            'pk', 'breadcrumbs', 'name', 'image', 'description',
            'subcategories', 'products', 'pagination'
        )

    def get_image(self, obj):
        return obj.get_image(
            request=self.context['request'],
            version=shop_settings.SHOP_IMAGES_VERSIONS['category']
            ['category_view']
        )

    @cached_property
    def _pagination(self):
        if shop_settings.SHOP_PRODUCTS_PAGINATION_ON_PAGE:
            query_page = self.context['request'].GET.get('page') or 1
            try:
                paginator = Paginator(
                    self.instance.products.order_by(self._order_by),
                    shop_settings.SHOP_PRODUCTS_PAGINATION_ON_PAGE
                )
                return paginator.page(query_page)
            except InvalidPage:
                raise Http404
        else:
            return None

    @cached_property
    def _order_by(self):
        query_order_by = self.context['request'].GET.get('order_by')
        if query_order_by == 'price_asc':
            return 'price_gross'
        elif query_order_by == 'price_desc':
            return '-price_gross'
        else:
            return 'order'

    def get_products(self, obj):
        order_by = self._order_by
        if self._pagination:
            products = self._pagination.object_list
        else:
            products = obj.products.order_by(order_by)

        return CategoryProductSerializer(
            products,
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


class ProductImageSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()
    full_size = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = (
            'thumbnail', 'full_size'
        )

    def get_thumbnail(self, obj):
        return obj.get_image(
            request=self.context['request'],
            version=shop_settings.SHOP_IMAGES_VERSIONS['product']
            ['product_view_thumbnail']
        )

    def get_full_size(self, obj):
        return obj.get_image(
            request=self.context['request'],
            version=shop_settings.SHOP_IMAGES_VERSIONS['product']
            ['product_view_full_size']
        )


class ProductAttributeSerializers(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = ProductAttributeValue
        fields = ('name', 'value')

    def get_name(self, obj):
        return obj.attribute.name


class ProductOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOption
        fields = ('pk', 'name', 'price_mod', 'price_mod_percentage')


class ProductOptionsGroupSerializer(serializers.ModelSerializer):
    options = ProductOptionSerializer(many=True)

    class Meta:
        model = ProductOptionsGroup
        fields = ('pk', 'name', 'options')


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)
    attributes = ProductAttributeSerializers(many=True)
    price = serializers.SerializerMethodField()
    options = ProductOptionsGroupSerializer(many=True)
    required_options = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True
    )

    class Meta:
        model = Product
        fields = (
            'pk', 'breadcrumbs', 'name', 'description', 'images', 'attributes',
            'price', 'available', 'options', 'required_options'
        )

    def get_price(self, obj):
        return str(obj.price_gross)


class CategoriesModuleSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = (
            'pk', 'name', 'route', 'image', 'description', 'subcategories'
        )

    def get_image(self, obj):
        return obj.get_thumbnail_or_image(
            request=self.context['request'],
            version=shop_settings.SHOP_IMAGES_VERSIONS['category']['module']
        )

    def get_subcategories(self, obj):
        try:
            max_level = int(self.context['request'].GET.get('max_level'))
        except (TypeError, ValueError):
            max_level = None
        if (
            obj.subcategories and
            (max_level is None or obj.level < max_level)
        ):
            return self.__class__(
                obj.subcategories,
                many=True,
                context={'request': self.context['request']}
            ).data
        else:
            return None


class ProductsModuleProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'pk', 'name', 'route', 'image', 'price'
        )

    def get_image(self, obj):
        try:
            return obj.main_image.get_image(
                request=self.context['request'],
                version=shop_settings.SHOP_IMAGES_VERSIONS['product']['module']
            )
        except AttributeError:
            return None

    def get_price(self, obj):
        return str(obj.price_gross)

    def to_representation(self, obj):
        data = super(ProductsModuleProductSerializer, self) \
            .to_representation(obj)
        module = self.root.instance
        if not module.show_names:
            data.pop('name')
        if not module.show_images:
            data.pop('image')
        if not module.show_prices:
            data.pop('price')
        return data


class ProductsModuleSerializer(mixins.ModuleSerializer):
    products = ProductsModuleProductSerializer(many=True)

    class Meta:
        model = ProductsModule
        fields = (
            'pk', 'name', 'module_name_header_level', 'html_class', 'products',
            'names_headers_level'
        )

    def to_representation(self, obj):
        data = super(ProductsModuleSerializer, self).to_representation(obj)
        if not obj.show_names:
            data.pop('names_headers_level')
        return data
