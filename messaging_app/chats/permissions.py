from rest_framework import permissions
from .models import Conversation, Message


class IsParticipantOfConversation(permissions.BasePermission):
    """Custom permission to:
        - Allow only authenticated users
        - Allows only conversation participants to access messages and conversation
    """

    def has_permission(self, request, view):
        """Authenticate to access any view"""
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Tie messages to conversations"""
        if isinstance(obj, Conversation):
            is_participant = request.user in obj.participants.all()
        if isinstance(obj, Message):
            is_participant = request.user in obj.conversation.participants.all()

        # SAFE_METHODS are GET, HEAD, OPTIONS - always allowed for participants
        if request.method in permissions.SAFE_METHODS:
            return is_participant

        # Allow PUT, PATCH, DELETE only for participants
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return is_participant

        return False
