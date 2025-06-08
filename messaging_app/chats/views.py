from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, retrieving, and creating Conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with specified participants.
        Expects a list of user IDs in 'participants' field.
        """
        participants = request.data.get('participants')
        if not participants or not isinstance(participants, list):
            return Response(
                {"error": "Participants must be a list of user IDs."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        conversation = Conversation.objects.create()
        # Add participants (users) to the conversation
        conversation.participants.set(participants)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, retrieving, and creating Messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new message in an existing conversation.
        Expects 'conversation' ID and 'message_body' in the request data.
        The sender is set as the logged-in user.
        """
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

        # Assuming the user is authenticated and request.user is the sender
        sender = request.user

        # Create and save the message
        message = Message.objects.create(
            sender=sender,
            conversation_id=conversation_id,
            message_body=message_body
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)