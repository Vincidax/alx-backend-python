from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from messaging.models import Message
from messaging.utils import get_thread

@login_required
def delete_user(request):
    user = request.user
    logout(request)
    user.delete()
    return redirect('home')

@login_required
def message_thread_view(request, message_id):
    root_message = get_object_or_404(
        Message.objects.select_related('sender', 'receiver', 'edited_by')
                       .prefetch_related('replies'),
        id=message_id
        sender=request.user
    )
    thread = get_thread(root_message)
    return render(request, 'messaging/thread.html', {
        'root_message': root_message,
        'thread': thread
    })

def build_thread(message, depth=0):
    thread = [(message, depth)]
    replies = message.replies.select_related('sender', 'receiver').all()
    for reply in replies:
        thread += build_thread(reply, depth + 1)
    return thread

def thread_view(request, message_id):
    root_message = Message.objects.select_related('sender', 'receiver').get(id=message_id)
    thread = build_thread(root_message)
    return render(request, 'messaging/thread.html', {
        'root_message': root_message,
        'thread': thread
    })

