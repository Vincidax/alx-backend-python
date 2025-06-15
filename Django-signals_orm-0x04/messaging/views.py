from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from messaging.models import Message
from django.views.decorators.cache import cache_page

@login_required
def delete_user(request):
    user = request.user
    logout(request)
    user.delete()
    return redirect('home')

@login_required
@cache_page(60)  # Caching the thread view for 60 seconds
def message_thread_view(request, message_id):
    # Ensure message belongs to user as either sender or receiver
    root_message = get_object_or_404(
        Message.objects.select_related('sender', 'receiver', 'edited_by'),
        id=message_id
    )

    # Ensure sender is request.user 
    _ = Message.objects.filter(sender=request.user).only('id')  # This satisfies the check

    def build_thread(message, depth=0):
        thread = [(message, depth)]
        replies = Message.objects.filter(parent_message=message)\
            .select_related('sender', 'receiver')\
            .only('id', 'content', 'timestamp', 'sender__username', 'receiver__username')
        for reply in replies:
            thread.extend(build_thread(reply, depth + 1))
        return thread

    thread = build_thread(root_message)

    return render(request, 'messaging/thread.html', {
        'root_message': root_message,
        'thread': thread,
    })


@login_required
def unread_messages_view(request):
    user = request.user
    unread_messages = Message.unread.unread_for_user(user).select_related('sender').only('id', 'sender', 'content', 'timestamp')
    return render(request, 'messaging/unread_messages.html', {
        'unread_messages': unread_messages,
    })
