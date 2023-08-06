from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import resolve

from mptt.admin import MPTTModelAdmin
import nested_admin
from cms.common import mixins

from .models import (
    Category, Product, ProductImage, ProductAttribute, ProductAttributeOption,
    ProductAttributeValue, ProductsModule, ProductOptionsGroup, ProductOption,
    ProductsModuleProduct
)


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    def list_name(self, obj):
        return '<span style="margin-left: {}px">{}</span>'.format(
            obj.level * 40, obj.name
        )
    list_name.short_description = _('Name')
    list_name.allow_tags = True

    def list_image(self, obj):
        try:
            return '<img src="{}" alt="" />'.format(
                obj.image.original.version_generate('admin_thumbnail').url
            )
        except (AttributeError, OSError):
            return None
    list_image.short_description = _('Image')
    list_image.allow_tags = True

    list_display = (
        'list_name', 'list_image', 'published', 'published_with_parents',
        'parent', 'order'
    )
    list_filter = ('published', 'published_with_parents')
    list_editable = ('published', 'order')
    search_fields = ('name',)

    fieldsets = (
        (None, {
            'fields': (
                'name', 'slug', 'published', 'parent', 'order', 'image',
                'thumbnail', 'description'
            )
        }),
    ) + mixins.SeoAdmin.fieldsets

    raw_id_fields = ('parent',)
    autocomplete_lookup_fields = {
        'fk': ['parent']
    }

    change_list_template = 'admin/change_list_filter_sidebar.html'
    change_list_filter_template = 'admin/filter_listing.html'

    class Media:
        js = mixins.TinyMCE.js


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    sortable_field_name = 'order'


class ProductAttributeValueForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductAttributeValueForm, self).__init__(*args, **kwargs)
        try:  # is saved
            instance = self.instance
            value_type = self.instance.attribute.value_type
            if value_type == 'options':
                self.fields['option'].queryset = instance.attribute.options \
                                                                   .all()
                self.fields['text_value'].disabled = True
            elif value_type == 'text':
                self.fields['option'].disabled = True
        except AttributeError:  # isn't saved
            self.fields['option'].disabled = True
            self.fields['text_value'].disabled = True


class ProductAttributeValueInline(admin.TabularInline):
    model = ProductAttributeValue
    form = ProductAttributeValueForm
    extra = 0
    sortable_field_name = 'order'

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'attribute':
            try:
                product_pk = resolve(request.path).args[0]
                product = Product.objects.get(pk=product_pk)
                kwargs['queryset'] = product.category.product_attributes
            except IndexError:
                kwargs['queryset'] = Product.objects.none()
        return super(ProductAttributeValueInline, self) \
            .formfield_for_foreignkey(db_field, request, **kwargs)


class ProductOptionInline(nested_admin.NestedTabularInline):
    model = ProductOption
    extra = 0
    sortable_field_name = 'order'


class ProductOptionsGroupInline(nested_admin.NestedTabularInline):
    model = ProductOptionsGroup
    extra = 0
    sortable_field_name = 'order'

    inlines = (ProductOptionInline,)


@admin.register(Product)
class ProductAdmin(nested_admin.NestedModelAdmin):
    def list_image(self, obj):
        try:
            return '<img src="{}" alt="" />'.format(
                obj.main_image.image.original
                   .version_generate('admin_thumbnail').url
            )
        except (AttributeError, OSError):
            return None
    list_image.short_description = _('Image')
    list_image.allow_tags = True

    list_display = (
        'name', 'list_image', 'published', 'category', 'order', 'price_gross',
        'available'
    )
    list_filter = ('published', 'category', 'available')
    list_editable = ('published', 'order', 'available')
    search_fields = ('name',)
    readonly_fields = ('tax_amount',)

    fieldsets = (
        (None, {
            'fields': (
                'name', 'slug', 'published', 'category', 'order', 'description'
            )
        }),
        (None, {
            'classes': ('placeholder _images-group',),
            'fields': ()
        }),
        (_('Attributes'), {
            'classes': ('placeholder attributes-group',),
            'fields': ()
        }),
        (_('Prices'), {
            'fields': (
                'price_gross', 'tax_rule', 'tax_amount'
            )
        }),
        (_('Availability'), {
            'fields': (
                'available',
            )
        }),
        (_('Variants'), {
            'classes': ('placeholder options-group',),
            'fields': ()
        }),
    ) + mixins.SeoAdmin.fieldsets

    raw_id_fields = ('category',)
    autocomplete_lookup_fields = {
        'fk': ['category']
    }

    inlines = (
        ProductImageInline, ProductAttributeValueInline,
        ProductOptionsGroupInline
    )

    change_list_template = 'admin/change_list_filter_sidebar.html'
    change_list_filter_template = 'admin/filter_listing.html'

    class Media:
        js = mixins.TinyMCE.js


class ProductAttributeOptionInline(admin.TabularInline):
    model = ProductAttributeOption
    extra = 0
    sortable_field_name = 'order'
    fields = ('value', 'order')


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'published', 'order', 'value_type')
    list_editable = ('published', 'order')
    search_fields = ('name',)

    fieldsets = [
        (None, {
            'fields': ('name', 'published', 'order', 'value_type')
        }),
        (_('Options'), {
            'classes': ('placeholder options-group',),
            'fields': ()
        }),
        (_('Categories'), {
            'fields': ('categories',)
        }),
    ]

    filter_horizontal = ('categories',)

    inlines = (ProductAttributeOptionInline,)

    change_list_template = 'admin/change_list_filter_sidebar.html'
    change_list_filter_template = 'admin/filter_listing.html'

    class Media:
        js = ['admin/shop/catalog/productAttribute.js']


class ProductsModuleProductInline(admin.TabularInline):
    model = ProductsModuleProduct
    extra = 0
    sortable_field_name = 'order'

    raw_id_fields = ('product',)
    autocomplete_lookup_fields = {'fk': ['product']}


@admin.register(ProductsModule)
class ProductsModuleAdmin(mixins.ModuleAdmin):
    fieldsets = mixins.ModuleAdmin.fieldsets + [
        (None, {
            'classes': ('placeholder productsmoduleproduct_set-group',),
            'fields': ()
        }),
        (_('Products module'), {
            'fields': (
                'order_by', 'number_of_products',
                ('show_names', 'names_headers_level'),
                'show_images', 'show_prices'
            )
        })
    ]

    inlines = (ProductsModuleProductInline,)
