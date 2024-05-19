from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Conversation, Chat


class ChatSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source="sender.full_name", read_only=True)
    receiver = serializers.CharField(source="receiver.full_name", read_only=True)
    receiver_id = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all(), write_only=True, source='receiver')
    conversation = serializers.CharField(source='conversation.id', read_only=True)

    class Meta:
        model = Chat
        fields = ["id", "sender", "receiver", "receiver_id", "conversation", "text", "delivered", "created_at"]
