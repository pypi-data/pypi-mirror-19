from django.shortcuts import get_object_or_404

from rest_framework import generics
from cms.common.utils import current_lang, served_langs

from .models import Category, ProductsModule
from .serializers import CategoriesModuleSerializer, ProductsModuleSerializer


class CategoriesModuleView(generics.ListAPIView):
    queryset = Category.objects.filter(published=True, level=0)
    serializer_class = CategoriesModuleSerializer


class ProductsModuleView(generics.RetrieveAPIView):
    queryset = ProductsModule.objects.filter(published=True)
    serializer_class = ProductsModuleSerializer
    lookup_field = 'template_id'

    def get_object(self):
        queryset = self.get_queryset()
        filters = {}
        filters[self.lookup_field] = self.kwargs[self.lookup_field]
        try:
            filters['language'] = current_lang()
            obj = queryset.get(**filters)
        except ProductsModule.DoesNotExist:
            del filters['language']
            filters['language__in'] = served_langs()
            obj = get_object_or_404(queryset, **filters)
        return obj
