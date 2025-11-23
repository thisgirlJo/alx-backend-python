from django_filters import rest_framework as filters
from .models import Message

class MessageFilter(filters.FilterSet):
    start_date = filters.DateTimeFilter(field_name="created_at", lookup_expr='gte')
    end_date = filters.DateTimeFilter(field_name="created_at", lookup_expr='lte')
    sender = filters.NumberFilter(field_name="sender__id")
    conversation = filters.NumberFilter(field_name="conversation__id")

    class Meta:
        model = Message
        fields = ['start_date', 'end_date', 'sender', 'conversation']