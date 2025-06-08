from rest_framework import permissions
from .models import Conversation, Message

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation
    to view, send, update, or delete messages.
    """

    def has_permission(self, request, view):
        # Only authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Determine if obj is a Message or a Conversation
        if isinstance(obj, Message):
            conversation = obj.conversation
        elif isinstance(obj, Conversation):
            conversation = obj
        else:
            return False

        # Only allow participants to interact
        return request.user in conversation.participants.all()
