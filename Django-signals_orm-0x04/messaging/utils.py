def get_thread(root_message):
    thread = []

    def fetch_replies(message, depth=0):
        # append the current message and depth
        thread.append((message, depth))
        # fetch all replies to the current message
        replies = message.replies.all().select_related('sender', 'receiver')
        for reply in replies:
            fetch_replies(reply, depth=depth+1)  # recursive call with incremented depth

    fetch_replies(root_message, depth=0)  # initial call with root depth 0
    return thread
