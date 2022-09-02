from rest_framework import serializers
from main.models import User, UserEvent


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEvent
        fields = ['id', 'name', 'description', 'category', 'date', 'start_time', 'end_time', 'location', 'neighbourhood', 'created_by', 'attendees']