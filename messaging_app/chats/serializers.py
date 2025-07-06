from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    """
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_full_name(self, obj: User) -> str:
        """ Returns the full name of the user by combining first and last names."""
        return f"{obj.first_name} {obj.last_name}".strip()

    def validate_email(self, value: str) -> str:
        """ Validates that the email ends with '.com' """
        if not value.endswith('.com'):
            raise serializers.ValidationError("Email must end with .com")
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        if not value:
            raise serializers.ValidationError("Email cannot be empty")
        if value[0].isupper():
            raise serializers.ValidationError("Email must start with an lowercase letter")
        if not value[0].isalpha():
            raise serializers.ValidationError("Email must start with a letter")
        if '@' not in value:
            raise serializers.ValidationError("Email must contain '@'")
        return value

    def validate_username(self, value: str) -> str:
        """ Validates that the username is unique and not empty. """
        if not value:
            raise serializers.ValidationError("Username cannot be empty")
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        if not value[0].isalpha():
            raise serializers.ValidationError("Username must start with a letter")
        return value

    def create(self, validated_data: dict) -> User:
        """Overide create method to hash the password before saving."""
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for Conversation model.
    """
    participants = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), required=True
    )

    class Meta:
        model = Conversation
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message model.
    """
    sender = UserSerializer(read_only=True)
    conversation = serializers.PrimaryKeyRelatedField(
        queryset=Conversation.objects.all())

    class Meta:
        model = Message
        fields = '__all__'
