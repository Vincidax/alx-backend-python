from django.urls import path
from .views import delete_user
from .views import message_thread_view
urlpatterns = [
    path('delete-account/', delete_user, name='delete_account'),
    path('thread/<int:message_id>/', message_thread_view, name='message_thread'),
]
