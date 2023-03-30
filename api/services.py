from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from store_django.settings import PAGE_SIZE
from games.models import Game


class GamePagination(PageNumberPagination):
    page_size = PAGE_SIZE

    def get_paginated_response(self, data):
        return Response({
            'page_current_number': self.page.number,
            'page_count': self.page.paginator.num_pages,
            'games': data
        })


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class GameFilter(filters.FilterSet):
    name = CharFilterInFilter(field_name='name', lookup_expr='in')
    genres = CharFilterInFilter(field_name='genres__slug', lookup_expr='in')
    tags = CharFilterInFilter(field_name='tags__slug', lookup_expr='in')
    price = filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Game
        fields = ['genres', 'tags', 'price']
