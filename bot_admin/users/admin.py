from django.contrib import admin

from users.models import ChatUser, ChatMessage

class MessageInline(admin.StackedInline):
    model = ChatMessage
    extra = 1

class ChatUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'user_id', 'message_count')
    list_filter = ('username',)
    search_fields = ('username',)
    inlines = [MessageInline]


admin.site.register(ChatUser, ChatUserAdmin)
admin.site.register(ChatMessage)
