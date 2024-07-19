import uuid

from django.db import models
from django.utils import timezone


class ChatUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    username = models.CharField(max_length=255, unique=True, null=True, verbose_name="Имя пользователя")
    first_name = models.CharField(max_length=255, unique=True, null=True, verbose_name="Имя", default="-")
    last_name = models.CharField(max_length=255, unique=True, null=True, verbose_name="Фамилия", default="-")
    user_id = models.IntegerField(null=False, verbose_name="ID пользователя")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username if self.username else self.first_name

    def message_count(self):
        today = timezone.now().date()
        return self.messages.filter(created_at__date=today).count()

    message_count.short_description = "Количество сообщений"


class ChatMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(ChatUser, related_name="messages", on_delete=models.CASCADE, verbose_name="Пользователь")
    created_at = models.DateTimeField(auto_now_add=True)
