import django_filters

from .models import UserEvent

class EventFilter(django_filters.FilterSet):

    class Meta:
        model = UserEvent
        fields = {'name': ['icontains'], 'category': ['exact'], 'neighbourhood': ['exact']}
