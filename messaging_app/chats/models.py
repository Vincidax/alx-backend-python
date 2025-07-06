import uuid
from django.db import models
from django.conf import settings


class User(models.Model):
    """
    Model representing a user in the chat application.
    """
    user_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    second_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    is_muted = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default=False)
    is_starred = models.BooleanField(default=False)

    def __str__(self):
        """Return string representation of the user."""
        return self.username


class Conversation(models.Model):
    """
    Model representing a conversation between users.
    """
    conversation_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    name = models.CharField(max_length=255, blank=True, null=True)
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_group = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    is_muted = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default=False)
    is_starred = models.BooleanField(default=False)
    is_forwarded = models.BooleanField(default=False)
    forwarded_from = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='forwarded_conversations'
    )

    def __str__(self):
        """Return string representation of the number
           of participants in a single conversation.
        """
        return f"Conversation {self.id} with {self.participants.count()} participants"


class Message(models.Model):
    """
    Model representing a message in a conversation.
    """
    message_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages'
    )
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_edited = models.BooleanField(default=False)
    edited_content = models.TextField(null=True, blank=True)
    edited_timestamp = models.DateTimeField(null=True, blank=True)
    is_pinned = models.BooleanField(default=False)
    is_starred = models.BooleanField(default=False)
    is_forwarded = models.BooleanField(default=False)
    forwarded_from = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='forwarded_messages'
    )
