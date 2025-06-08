from rest_framework import permissions
from .models import Conversation, Message

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation
    to send, view, update, or delete messages.
    """

    def has_permission(self, request, view):
        # Only allow authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Determine conversation from object
        if isinstance(obj, Message):
            conversation = obj.conversation
        elif isinstance(obj, Conversation):
            conversation = obj
        else:
            return False

        # Allowed methods for participants only
        if request.method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
            return request.user in conversation.participants.all()

        # Deny all other cases
        return False
