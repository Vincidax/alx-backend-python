# chats/serializers.py

from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model with full_name and validations.
    """
    full_name = serializers.SerializerMethodField()
    username = serializers.CharField(max_length=150)
    email = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'full_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def get_full_name(self, obj: User) -> str:
        return f"{obj.first_name} {obj.last_name}".strip()

    def validate_email(self, value: str) -> str:
        if not value:
            raise serializers.ValidationError("Email cannot be empty")
        if not value[0].isalpha():
            raise serializers.ValidationError("Email must start with a letter")
        if value[0].isupper():
            raise serializers.ValidationError("Email must start with a lowercase letter")
        if '@' not in value:
            raise serializers.ValidationError("Email must contain '@'")
        if not value.endswith('.com'):
            raise serializers.ValidationError("Email must end with .com")
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate_username(self, value: str) -> str:
        if not value:
            raise serializers.ValidationError("Username cannot be empty")
        if not value[0].isalpha():
            raise serializers.ValidationError("Username must start with a letter")
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_password(self, value: str) -> str:
        validate_password(value)
        return value

    def create(self, validated_data: dict) -> User:
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message model.
    """
    sender = UserSerializer(read_only=True)
    content = serializers.CharField(max_length=1000)
    conversation = serializers.PrimaryKeyRelatedField(queryset=Conversation.objects.all())

    class Meta:
        model = Message
        fields = ['id', 'content', 'sender', 'conversation', 'created_at']


class MessageNestedSerializer(serializers.ModelSerializer):
    """
    Nested serializer for messages inside a conversation.
    """
    sender = serializers.SlugRelatedField(slug_field='username', read_only=True)
    content = serializers.CharField(max_length=1000)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'created_at']


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for Conversation model with nested messages.
    """
    participants = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all()
    )
    messages = MessageNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'messages', 'created_at']
