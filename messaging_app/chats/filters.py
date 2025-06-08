import django_filters
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()

class MessageFilter(django_filters.FilterSet):
    # Filter by participant username in the conversation
    participant = django_filters.CharFilter(field_name='conversation__participants__username', lookup_expr='icontains')

    # Filter by message sent_at range
    sent_at__gte = django_filters.IsoDateTimeFilter(field_name='sent_at', lookup_expr='gte')
    sent_at__lte = django_filters.IsoDateTimeFilter(field_name='sent_at', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['participant', 'sent_at__gte', 'sent_at__lte']
