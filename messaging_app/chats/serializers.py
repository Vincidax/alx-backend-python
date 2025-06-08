from rest_framework import serializers
from .models import User, Conversation, Message

# Serializer for the custom User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Fields to be included in the serialized representation
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number']


# Serializer for the Message model
class MessageSerializer(serializers.ModelSerializer):
    # Represent the sender as a nested User object (read-only)
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        # Fields to serialize for each message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']


# Serializer for the Conversation model
class ConversationSerializer(serializers.ModelSerializer):
    # Include all participants in the conversation as nested user objects (read-only)
    participants = UserSerializer(many=True, read_only=True)

    # Include all related messages in the conversation as nested message objects (read-only)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        # Fields to include in the serialized conversation output
        fields = ['conversation_id', 'participants', 'messages', 'created_at']
