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
    sender = UserSerializer(read_only=True)

    # Explicitly declare message_body as CharField
    message_body = serializers.CharField(max_length=1000)

    # SerializerMethodField to provide a preview of the message content
    preview = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at', 'preview']

    def get_preview(self, obj):
        """
        Return the first 50 characters of the message body as a preview.
        """
        return obj.message_body[:50]

    def validate_message_body(self, value):
        """
        Validate that the message body is not empty or just whitespace.
        """
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("Message body cannot be empty.")
        return value


# Serializer for the Conversation model
class ConversationSerializer(serializers.ModelSerializer):
    # Nested users participating in the conversation
    participants = UserSerializer(many=True, read_only=True)

    # Nested messages within the conversation
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']
