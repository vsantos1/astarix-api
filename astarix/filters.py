from django_filters import rest_framework as filters
from .models import Pixel,GameMap

class PixelFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    agent = filters.CharFilter(lookup_expr='icontains')
    sent_by = filters.CharFilter(lookup_expr='icontains')
    description = filters.CharFilter(lookup_expr='icontains')
    approved = filters.BooleanFilter(lookup_expr='exact')

    class Meta:
        model = Pixel
        fields = ['title','description','agent','sent_by','approved']

class MapFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    game = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = GameMap
        fields = ['name','game']