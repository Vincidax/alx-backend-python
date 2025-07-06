import django_filters
from .models import Message


class MessageFilter(django_filters.FilterSet):
    created_after = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='lte')
    sender = django_filters.CharFilter(field_name='sender__username', lookup_expr='iexact')
    conversation = django_filters.NumberFilter(field_name='conversation__conversation_id')

    class Meta:
        model = Message
        fields = ['sender', 'conversation', 'created_after', 'created_before']