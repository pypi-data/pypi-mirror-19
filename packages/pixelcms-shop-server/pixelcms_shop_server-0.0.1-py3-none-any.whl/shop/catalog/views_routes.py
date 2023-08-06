from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


@api_view()
def category_view(request, slug, pk):
    category = get_object_or_404(
        Category,
        published_with_parents=True,
        slug=slug,
        pk=pk
    )
    return Response({
        'component_name': 'ShopCategory',
        'component_data': CategorySerializer(
            category, context={'request': request}
        ).data,
        'meta': category.meta
    })


@api_view()
def product_view(request, slug, pk):
    product = get_object_or_404(
        Product,
        published=True,
        category__published_with_parents=True,
        slug=slug,
        pk=pk
    )
    return Response({
        'component_name': 'ShopProduct',
        'component_data': ProductSerializer(
            product, context={'request': request}
        ).data,
        'meta': product.meta
    })
