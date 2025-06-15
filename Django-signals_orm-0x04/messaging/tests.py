from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory
from .utils import get_thread

class MessagingSignalTestCase(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='sender', password='pass')
        self.receiver = User.objects.create_user(username='receiver', password='pass')

    def test_notification_created_on_message(self):
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Hello!"
        )
        notification = Notification.objects.get(message=message)
        self.assertEqual(notification.user, self.receiver)

    def test_user_deletion_cleans_related_data(self):
        # Send a message
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content='Initial Message'
        )

        # Edit message to trigger MessageHistory
        message.content = 'Edited Message'
        message.save()

        # Check message, notification, and message history exist
        self.assertTrue(Message.objects.filter(sender=self.sender).exists())
        self.assertTrue(Notification.objects.filter(user=self.receiver).exists())
        self.assertTrue(MessageHistory.objects.filter(message=message).exists())

        # Store user ID for query after deletion
        sender_id = self.sender.id

        # Delete user
        self.sender.delete()

        # Confirm user is deleted
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=sender_id)

        # Confirm all related data is deleted
        self.assertFalse(Message.objects.filter(sender_id=sender_id).exists())
        self.assertFalse(Notification.objects.filter(user_id=sender_id).exists())
        self.assertFalse(MessageHistory.objects.filter(message__sender_id=sender_id).exists())


    def test_threaded_messages(self):
        root = Message.objects.create(sender=self.sender, receiver=self.receiver, content="Root message")

        reply1 = Message.objects.create(sender=self.receiver, receiver=self.sender, content="Reply 1", parent_message=root)
        reply2 = Message.objects.create(sender=self.sender, receiver=self.receiver, content="Reply 2", parent_message=reply1)
        reply3 = Message.objects.create(sender=self.receiver, receiver=self.sender, content="Reply 3", parent_message=reply2)

        thread = get_thread(root)

        messages_in_thread = [msg for msg, depth in thread]

        self.assertIn(reply1, messages_in_thread)
        self.assertIn(reply2, messages_in_thread)
        self.assertIn(reply3, messages_in_thread)
        self.assertEqual(len(thread), 4)

