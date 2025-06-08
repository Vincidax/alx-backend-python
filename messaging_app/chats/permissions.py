from rest_framework import permissions

class IsParticipant(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation
    to view or send messages in it.
    """

    def has_object_permission(self, request, view, obj):
        # obj can be a Conversation or Message instance
        # Check if request.user is part of the conversation participants
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        elif hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()
        return False
