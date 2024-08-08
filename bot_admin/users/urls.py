from django.urls import path, include

from bot_admin.users.views import user_message_view

urlpatterns = [
    path('stats', user_message_view)
]