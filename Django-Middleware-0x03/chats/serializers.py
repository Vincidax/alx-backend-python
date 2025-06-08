from rest_framework import serializers
from .models import User, Conversation, Message

# Serializer for the custom User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number']


# Serializer for the Message model
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    message_body = serializers.CharField(max_length=1000)
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
    # Read-only nested user details
    participants = UserSerializer(many=True, read_only=True)

    # Accept user UUIDs for creating conversation
    participants_ids = serializers.ListField(
        child=serializers.UUIDField(), write_only=True
    )

    # Read-only nested messages
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'participants_ids', 'messages', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']

    def create(self, validated_data):
        participant_ids = validated_data.pop('participants_ids', [])
        users = User.objects.filter(user_id__in=participant_ids)

        if users.count() != len(participant_ids):
            raise serializers.ValidationError("One or more participant IDs are invalid.")

        conversation = Conversation.objects.create()
        conversation.participants.set(users)
        return conversation
