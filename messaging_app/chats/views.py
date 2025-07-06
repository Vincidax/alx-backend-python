from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .permissions import IsParticipantOfConversation
from django_filters.rest_framework import DjangoFilterBackend
from .filters import MessageFilter
from .pagination import StandardResultsSetPagination


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User model.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    lookup_field = 'user_id'

    def perform_create(self, serializer: UserSerializer) -> None:
        """Override to set the user to the current user."""
        serializer.save()


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Conversation model.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'participants__username']
    lookup_field = 'conversation_id'
    ordering_fields = ['created_at', 'updated_at']

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj

    def retrieve(self, request, *args, **kwargs):
        conversation = self.get_object()
        if request.user not in conversation.paticipants.all():
            return Response(
                {"Detail": "You are not a participant of this conversation"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().retrieve(request, *args, **kwargs)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Message model.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    pagination_class = StandardResultsSetPagination
    search_fields = MessageFilter

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)

    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_create(self, serializer: MessageSerializer) -> None:
        """Override to set the sender to the current user."""
        user = self.request.user
        conversation = serializer.validated_data['conversation']
        if user not in conversation.participants.all():
            raise PermissionDenied('You are not allowed to send a message to this conversation')
        serializer.save(sender=user)

    @action(detail=False, methods=['get'])
    def custom_status(self, request: None) -> Response:
        """Example custom action using status."""
        return Response({'detail': 'Custom status OK'}, status=status.HTTP_200_OK)
