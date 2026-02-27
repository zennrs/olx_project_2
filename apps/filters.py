from django_filters import FilterSet, NumberFilter
from apps.models import Announcement


class AnnouncementFilterSet(FilterSet):

    min_price = NumberFilter(field_name='price', lookup_expr='gte')
    max_price = NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Announcement
        fields = ['min_price', 'max_price']
