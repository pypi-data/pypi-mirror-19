from decimal import Decimal

from django.test import TestCase
from django.core.urlresolvers import reverse

from rest_framework.test import APIClient

from shop.catalog.models import Category, Product
from shop.sale.models import Cart
from shop import settings as shop_settings


def _create_test_catalog(self):
    self.c1 = Category.objects.create(name='Clothes')
    self.c2 = Category.objects.create(name='Not here yet', published=False)
    self.c3 = Category.objects.create(
        name='Not here yer child', parent=self.c2
    )
    self.p1 = Product.objects.create(
        name='Lorem ipsum',
        category=self.c1,
        price_gross=Decimal('100.00')
    )
    self.p2 = Product.objects.create(
        name='Dolor sit amet',
        category=self.c1,
        price_gross=Decimal('110.00')
    )
    # unpublished
    self.p3 = Product.objects.create(
        name='Not published',
        published=False,
        category=self.c1,
        price_gross=Decimal('120.00')
    )
    # in unpublished category
    self.p4 = Product.objects.create(
        name='Category not published',
        category=self.c2,
        price_gross=Decimal('130.00')
    )
    # in category which has unpublished parent
    self.p5 = Product.objects.create(
        name='Root category not published',
        category=self.c3,
        price_gross=Decimal('140.00')
    )
    # unavailable
    self.p6 = Product.objects.create(
        name='Sold out',
        category=self.c1,
        price_gross=Decimal('150.00'),
        available=False
    )


class CatalogRoutes(TestCase):
    def setUp(self):
        self.client = APIClient()
        _create_test_catalog(self)

    def _get_category_route(self, category):
        return reverse('shop_routes:catalog:category', kwargs={
            'slug': category.slug,
            'pk': category.pk
        })

    def _get_product_route(self, product):
        return reverse('shop_routes:catalog:product', kwargs={
            'slug': product.slug,
            'pk': product.pk
        })

    def test_category_route_endpoint(self):
        res = self.client.get(self._get_category_route(self.c1))
        data = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('componentName'), 'ShopCategory')

        # unpublished
        res = self.client.get(self._get_category_route(self.c2))
        data = res.json()
        self.assertEqual(res.status_code, 404)

        # unpublished parent
        res = self.client.get(self._get_category_route(self.c3))
        data = res.json()
        self.assertEqual(res.status_code, 404)

    def test_product_route_endpoint(self):
        res = self.client.get(self._get_product_route(self.p1))
        data = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('componentName'), 'ShopProduct')

        res = self.client.get(self._get_product_route(self.p3))
        data = res.json()
        self.assertEqual(res.status_code, 404)

        res = self.client.get(self._get_product_route(self.p4))
        data = res.json()
        self.assertEqual(res.status_code, 404)

        res = self.client.get(self._get_product_route(self.p5))
        data = res.json()
        self.assertEqual(res.status_code, 404)


class AddToCart(TestCase):
    quest_cart_pk = None

    def setUp(self):
        self.client = APIClient()
        _create_test_catalog(self)

    def test_add_to_cart_as_guest(self):
        # add first product
        res = self.client.post(
            reverse('shop_api:sale:add_to_cart'),
            {
                'product': self.p1.pk,
                'quantity': 1
            }
        )
        data = res.json()
        cart_pk = data['pk']
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['productsCount'], 1)
        self.assertEqual(data['total'], str(self.p1.price_gross))
        cart = Cart.objects.get(pk=cart_pk)
        self.assertEqual(len(cart.products.all()), 1)

        # add the same product again (increase quantity)
        res = self.client.post(
            reverse(
                'shop_api:sale:add_to_cart_by_pk',
                kwargs={'cart_pk': cart_pk}
            ),
            {
                'product': self.p1.pk,
                'quantity': 1
            }
        )
        data = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['productsCount'], 2)
        self.assertEqual(data['total'], str(self.p1.price_gross * 2))
        cart = Cart.objects.get(pk=cart_pk)
        self.assertEqual(len(cart.products.all()), 1)

        # add another product
        res = self.client.post(
            reverse(
                'shop_api:sale:add_to_cart_by_pk',
                kwargs={'cart_pk': cart_pk}
            ),
            {
                'product': self.p2.pk,
                'quantity': 3
            }
        )
        data = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['productsCount'], 5)
        self.assertEqual(
            data['total'],
            str(self.p1.price_gross * 2 + self.p2.price_gross * 3)
        )
        cart = Cart.objects.get(pk=cart_pk)
        self.assertEqual(len(cart.products.all()), 2)

    def test_add_to_cart_unpublished(self):
        for p in [self.p3, self.p4, self.p5]:
            res = self.client.post(
                reverse('shop_api:sale:add_to_cart'),
                {
                    'product': p.pk,
                    'quantity': 1
                }
            )
            self.assertEqual(res.status_code, 400)

    def test_add_to_cart_unavailable(self):
            res = self.client.post(
                reverse('shop_api:sale:add_to_cart'),
                {
                    'product': self.p6.pk,
                    'quantity': 1
                }
            )
            self.assertEqual(res.status_code, 400)

    def test_quantity_limit(self):
        res = self.client.post(
            reverse('shop_api:sale:add_to_cart'),
            {
                'product': self.p1.pk,
                'quantity': shop_settings.SHOP_QUANTITY_LIMIT + 1
            }
        )
        self.assertEqual(res.status_code, 400)
