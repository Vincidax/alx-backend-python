from rest_framework.permissions import BasePermission

class IsParticipantOfConversation(BasePermission):
    """
    Allows access only to authenticated users who are participants of a conversation.
    """

    def has_permission(self, request, view):
        # Allow only authenticated users to access the view
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission:
        - For Conversation: check if the user is a participant
        - For Message: check if the user is a participant in the related conversation
        """
        if hasattr(obj, 'participants'):
            # obj is a Conversation
            return request.user in obj.participants.all()
        elif hasattr(obj, 'conversation'):
            # obj is a Message
            return request.user in obj.conversation.participants.all()
        return False
