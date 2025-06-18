from django.contrib import admin
from .models import ChatRoom, Message, MessageAttachment


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'conversation_type', 'status', 'initiator', 'receiver', 'created_at']
    list_filter = ['conversation_type', 'status', 'created_at']
    search_fields = ['initiator__phone', 'receiver__phone', 'location', 'provider_name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (None, {
            'fields': ('name', 'initiator', 'receiver', 'conversation_type', 'status')
        }),
        ('Additional Info', {
            'fields': ('location', 'provider_name', 'categories', 'author_name', 'is_statement_owner'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'chat_room', 'sender', 'text_preview', 'timestamp', 'is_read']
    list_filter = ['timestamp', 'is_read', 'chat_room__conversation_type']
    search_fields = ['text', 'sender__phone']
    readonly_fields = ['timestamp']
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Text Preview'


@admin.register(MessageAttachment)
class MessageAttachmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'message', 'filename', 'file_size', 'content_type']
    list_filter = ['content_type']
    search_fields = ['filename'] 