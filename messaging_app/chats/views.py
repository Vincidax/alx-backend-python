from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from django.shortcuts import get_object_or_404


class ConversationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    serializer_class = ConversationSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['participants__username']
    ordering_fields = ['created_at']

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        participants = request.data.get('participants')
        if not participants or not isinstance(participants, list):
            return Response(
                {"error": "Participants must be a list of user IDs."},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.participants.add(request.user)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    serializer_class = MessageSerializer

    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['sent_at']

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.validated_data.get("conversation")
        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("You are not a participant in this conversation.")
        serializer.save(sender=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user not in instance.conversation.participants.all():
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user not in instance.conversation.participants.all():
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
