import django_filters
from django.db.models import Q

from .models import Property


class PropertyFilter(django_filters.FilterSet):
    class Meta:
        model = Property
        fields = {"id": ["exact"], "available": ["exact"], "source": ["iexact"]}

    current_properties = django_filters.CharFilter(method="current_properties_filter")

    def current_properties_filter(self, queryset, _, value):
        last_update_date = Property.objects.latest("update_date").update_date
        if value == "true":
            return queryset.filter(update_date=last_update_date)
        else:
            return queryset.filter(~Q(update_date=last_update_date))
