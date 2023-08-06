from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from django.core.urlresolvers import reverse

from autoslug import AutoSlugField
from mptt.models import MPTTModel, TreeForeignKey
from filebrowser.fields import FileBrowseField
from cms.common import mixins, utils

from shop.config.models import TaxRule


HEADERS_LEVEL_CHOICES = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
)


class Category(MPTTModel, mixins.Seo):
    name = models.CharField(_('name'), max_length=255)
    slug = AutoSlugField(
        _('slug'), populate_from='name', editable=True, blank=True
    )
    published = models.BooleanField(_('published'), default=True)
    published_with_parents = models.BooleanField(
        _('published with parents'), default=True
    )
    parent = TreeForeignKey(
        'self', verbose_name=_('parent'), null=True, blank=True,
        related_name='_subcategories', db_index=True
    )
    order = models.PositiveSmallIntegerField(_('order'), default=0)
    level = models.PositiveSmallIntegerField(default=0)

    image = FileBrowseField(_('image'), max_length=255, null=True, blank=True)
    thumbnail = FileBrowseField(
        _('thumbnail'), max_length=255, null=True, blank=True
    )
    description = models.TextField(_('description'), default='', blank=True)

    class Meta:
        app_label = 'shop'
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    class MPTTMeta:
        order_insertion_by = ('order',)

    def save(self, *args, **kwargs):
        if self.parent:
            parents_published = self.parent.published_with_parents
        else:
            parents_published = True
        self.published_with_parents = self.published and parents_published
        try:
            orig = Category.objects.get(pk=self.pk)
        except Category.DoesNotExist:
            orig = None
        super(Category, self).save(*args, **kwargs)
        if orig:
            if orig.published != self.published:
                for c in self.get_descendants():
                    c.save()
            # delete all CartProduct objects if category is unpublished
            if not self.published_with_parents and orig.published_with_parents:
                from shop.sale.models import CartProduct
                CartProduct.objects.filter(product__category=self).delete()
        self.__class__.objects.rebuild()

    def __str__(self):
        return self.name

    @staticmethod
    def autocomplete_search_fields():
        return ('name__icontains',)

    @property
    def route(self):
        return '/s/c/{},{}'.format(self.slug, self.pk)

    @property
    def meta(self):
        return utils.generate_meta(
            title=self.meta_title_override or self.name,
            title_suffix=self.meta_title_site_name_suffix,
            description=self.meta_description_override,
            robots=self.meta_robots_override
        )

    @property
    def breadcrumbs(self):
        output = [{
            'name': self.name,
            'route': self.route
        }]
        parent = self.parent
        while parent:
            output.append({
                'name': parent.name,
                'route': parent.route
            })
            parent = parent.parent
        return reversed(output)

    def get_image(self, request, version=None):
        try:
            if version:
                image = self.image.original.version_generate(version).url
            else:
                image = self.image.url
            return request.build_absolute_uri(image)
        except (AttributeError, OSError):
            return None

    def get_thumbnail_or_image(self, request, version=None):
        image = self.thumbnail or self.image
        try:
            if version:
                image = image.original.version_generate(version).url
            else:
                image = image.url
            return request.build_absolute_uri(image)
        except (AttributeError, OSError):
            return None

    @property
    def subcategories(self):
        return self._subcategories.filter(published_with_parents=True)

    @property
    def products(self):
        categories_pks = [self.pk]
        categories_pks += self.get_descendants() \
            .filter(published_with_parents=True) \
            .values_list('pk', flat=True)
        return Product.objects.filter(
            published=True, category__in=categories_pks
        )

    @property
    def product_attributes(self):
        return self._product_attributes.filter(published=True)


class Product(mixins.Seo):
    name = models.CharField(_('name'), max_length=255)
    slug = AutoSlugField(
        _('slug'), populate_from='name', editable=True, blank=True
    )
    published = models.BooleanField(_('published'), default=True)
    category = models.ForeignKey(
        Category, verbose_name=_('category'), related_name='_products'
    )
    order = models.PositiveSmallIntegerField(_('order'), default=0)
    description = models.TextField(_('description'), default='', blank=True)

    _attributes = models.ManyToManyField(
        'ProductAttribute', verbose_name=_('attributes'), blank=True,
        through='ProductAttributeValue'
    )

    price_gross = models.DecimalField(
        _('gross price'), max_digits=18, decimal_places=2, blank=True,
        validators=[validators.MinValueValidator(0)]
    )
    tax_rule = models.ForeignKey(
        TaxRule, verbose_name=_('tax rule'), null=True, blank=True
    )
    tax_amount = models.DecimalField(
        _('tax amount'), max_digits=18, decimal_places=2, blank=True
    )
    available = models.BooleanField('available', default=True)

    class Meta:
        app_label = 'shop'
        ordering = ('category', 'order',)
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def save(self, *args, **kwargs):
        if self.tax_rule:
            self.tax_amount = (
                self.price_gross -
                self.price_gross / (self.tax_rule.rate / 100 + 1)
            )
        else:
            self.tax_amount = 0
        try:
            orig = Product.objects.get(pk=self.pk)
        except Product.DoesNotExist:
            orig = None
        super(Product, self).save(*args, **kwargs)
        if orig:
            from shop.sale.models import CartProduct
            if (
                (not self.published and orig.published) or
                (not self.available and orig.available)
            ):
                # delete all CartProduct objects if product is unpublished or
                # unavailable
                CartProduct.objects.filter(product=self).delete()
            elif self.price_gross != orig.price_gross:
                # recalculate cart if product changed
                for cart_product in CartProduct.objects.filter(product=self):
                    cart_product.save()

    def __str__(self):
        return self.name

    @staticmethod
    def autocomplete_search_fields():
        return ('name__icontains',)

    @property
    def route(self):
        return '/s/p/{},{}'.format(self.slug, self.pk)

    @property
    def meta(self):
        return utils.generate_meta(
            title=self.meta_title_override or self.name,
            title_suffix=self.meta_title_site_name_suffix,
            description=self.meta_description_override,
            robots=self.meta_robots_override
        )

    @property
    def breadcrumbs(self):
        output = [{
            'name': self.name,
            'route': self.route
        }]
        parent = self.category
        while parent:
            if parent.route:
                output.append({
                    'name': parent.name,
                    'route': parent.route
                })
            parent = parent.parent
        return reversed(output)

    @property
    def images(self):
        return self._images.filter(published=True)

    @property
    def main_image(self):
        return self.images.first()

    @property
    def required_options(self):
        return self.options.filter(required=True)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='_images')
    image = FileBrowseField(_('image'), max_length=255)
    published = models.BooleanField(_('published'), default=True)
    order = models.PositiveSmallIntegerField(_('order'), default=0)

    class Meta:
        app_label = 'shop'
        ordering = ('order',)
        verbose_name = _('image')
        verbose_name_plural = _('images')

    def get_image(self, request, version=None):
        try:
            if version:
                image = self.image.original.version_generate(version).url
            else:
                image = self.image.url
            return request.build_absolute_uri(image)
        except (AttributeError, OSError):
            return None


class ProductAttribute(models.Model):
    PRODUCTS_ATTRIBUTE_VALUE_TYPE_CHOICES = (
        ('options', _('Options')),
        ('text', _('Text'))
    )
    name = models.CharField(_('name'), max_length=255)
    published = models.BooleanField(_('published'), default=True)
    order = models.PositiveSmallIntegerField(_('order'), default=0)
    value_type = models.CharField(
        _('value type'), max_length=255,
        choices=PRODUCTS_ATTRIBUTE_VALUE_TYPE_CHOICES, default='options'
    )
    categories = models.ManyToManyField(
        Category, verbose_name=_('categories'),
        help_text=_(
            'Attribute will be available only for products in selected '
            'categories.'),
        blank=True, related_name='_product_attributes'
    )

    class Meta:
        app_label = 'shop'
        ordering = ('order',)
        verbose_name = _('product attribute')
        verbose_name_plural = _('product attributes')

    def __str__(self):
        return self.name


class ProductAttributeOption(models.Model):
    attribute = models.ForeignKey(
        ProductAttribute, verbose_name=_('attribute'), related_name='options'
    )
    value = models.CharField(_('value'), max_length=255)
    order = models.PositiveSmallIntegerField(_('order'), default=0)

    class Meta:
        app_label = 'shop'
        ordering = ('order',)
        unique_together = (('attribute', 'value'),)
        verbose_name = _('option')
        verbose_name_plural = _('options')

    def __str__(self):
        return self.value


class ProductAttributeValue(models.Model):
    product = models.ForeignKey(Product, related_name='attributes')
    attribute = models.ForeignKey(
        ProductAttribute, verbose_name=_('attribute')
    )
    option = models.ForeignKey(ProductAttributeOption, null=True, blank=True)
    text_value = models.CharField(
        _('text value'), max_length=255, null=True, blank=True
    )
    order = models.PositiveSmallIntegerField(_('order'), default=0)

    class Meta:
        app_label = 'shop'
        ordering = ('order',)
        unique_together = (('product', 'attribute'),)
        verbose_name = _('attribute')
        verbose_name_plural = _('attributes')

    def __str__(self):
        return self.attribute.name

    def save(self, *args, **kwargs):
        if self.attribute.value_type == 'options':
            self.text_value = None
        elif self.attribute.value_type == 'text':
            self.option = None
        super(ProductAttributeValue, self).save(*args, **kwargs)

    @property
    def value(self):
        if self.attribute.value_type == 'options':
            return self.option.value
        elif self.attribute.value_type == 'text':
            return self.text_value


class ProductOptionsGroup(models.Model):
    product = models.ForeignKey(Product, related_name='options')
    name = models.CharField(_('name'), max_length=255)
    order = models.PositiveSmallIntegerField(_('order'), default=0)
    required = models.BooleanField(_('required'), default=True)

    class Meta:
        app_label = 'shop'
        ordering = ('order',)
        unique_together = (('product', 'name'),)
        verbose_name = _('options group')
        verbose_name_plural = _('options groups')

    def save(self, *args, **kwargs):
        try:
            orig = ProductOptionsGroup.objects.get(pk=self.pk)
        except ProductOptionsGroup.DoesNotExist:
            orig = None
        super(ProductOptionsGroup, self).save(*args, **kwargs)
        from shop.sale.models import CartProduct
        if self.required and (orig and not orig.required or not orig):
            # group wasn't required but it is now or
            # new required group created
            # delete all related CartProducts
            for cart_product in CartProduct.objects \
                                           .filter(product=self.product):
                if not cart_product.validate_required_options():
                    cart_product.delete()

    def __str__(self):
        return self.name


class ProductOption(models.Model):
    group = models.ForeignKey(ProductOptionsGroup, related_name='options')
    name = models.CharField(_('name'), max_length=255)
    order = models.PositiveSmallIntegerField(_('order'), default=0)
    price_mod = models.DecimalField(
        _('price modification'), max_digits=18, decimal_places=2,
        null=True, blank=True
    )
    price_mod_percentage = models.BooleanField(_('percentage'), default=False)

    class Meta:
        app_label = 'shop'
        ordering = ('order',)
        unique_together = (('group', 'name'),)
        verbose_name = _('option')
        verbose_name_plural = _('options')

    def save(self, *args, **kwargs):
        try:
            orig = ProductOption.objects.get(pk=self.pk)
        except ProductOption.DoesNotExist:
            orig = None
        super(ProductOption, self).save(*args, **kwargs)
        if orig:
            if (
                self.price_mod != orig.price_mod or
                self.price_mod_percentage != orig.price_mod_percentage
            ):
                # recalculate cart if price_mod changed
                from shop.sale.models import CartProductOptionValue
                for cart_product_option_value in \
                        CartProductOptionValue.objects.filter(option=self):
                    cart_product_option_value.cart_product.save()

    def __str__(self):
        return self.name


class ProductsModule(mixins.Module):
    PRODUCTS_MODULE_ORDER_BY_CHOICES = (
        ('productsmoduleproduct__order', _('Order')),
        ('price_gross', _('Price - from lowest')),
        ('-price_gross', _('Price - from highest')),
        ('?', _('Random'))
    )

    _products = models.ManyToManyField(
        Product, through='ProductsModuleProduct', blank=True
    )
    order_by = models.CharField(
        _('order by'), max_length=255,
        choices=PRODUCTS_MODULE_ORDER_BY_CHOICES, default='order'
    )
    number_of_products = models.PositiveSmallIntegerField(
        _('number of products'), default=4
    )
    show_names = models.BooleanField(_('show names'), default=True)
    names_headers_level = models.CharField(
        _('names headers level'), max_length=1,
        choices=HEADERS_LEVEL_CHOICES, default='3'
    )
    show_images = models.BooleanField(_('show images'), default=True)
    show_prices = models.BooleanField(_('show prices'), default=True)

    class Meta(mixins.Module.Meta):
        app_label = 'shop'
        verbose_name = _('products module')
        verbose_name_plural = _('products modules')

    @property
    def products(self):
        return self._products.filter(
            published=True,
            category__published_with_parents=True
        ).order_by(self.order_by)[:self.number_of_products]


class ProductsModuleProduct(models.Model):
    module = models.ForeignKey(ProductsModule)
    product = models.ForeignKey(Product, verbose_name=_('product'))
    order = models.PositiveSmallIntegerField(_('order'), default=0)

    class Meta:
        app_label = 'shop'
        ordering = ('order',)
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        return self.product.name
