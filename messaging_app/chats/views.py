from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipant

class ConversationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsParticipant]
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['participants__username']  # example, you can adjust
    ordering_fields = ['created_at']

    def create(self, request, *args, **kwargs):
        participants = request.data.get('participants')
        if not participants or not isinstance(participants, list):
            return Response(
                {"error": "Participants must be a list of user IDs."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsParticipant]
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['sent_at']

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        conversation_id = data.get('conversation')
        message_body = data.get('message_body')

        if not conversation_id:
            return Response(
                {"error": "Conversation ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not message_body or len(message_body.strip()) == 0:
            return Response(
                {"error": "Message body cannot be empty."},
                status=status.HTTP_400_BAD_REQUEST
            )

        sender = request.user

        message = Message.objects.create(
            sender=sender,
            conversation_id=conversation_id,
            message_body=message_body
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)