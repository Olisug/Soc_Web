from django.contrib import admin

from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'reciever', 'message_time')
    search_fields = ('sender__username',)
    ordering = ('sender', 'reciever', 'message_time')