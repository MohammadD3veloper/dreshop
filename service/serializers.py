from rest_framework import serializers
from .models import Message


class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            'text',
            'to_supporter',
            'from_user',
            'date_send',
        ]
