from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class ChatRoom(models.Model):
    CONVERSATION_TYPES = [
        ('statement', 'Statement'),
        ('complaint', 'Complaint'),
        ('general', 'General'),
    ]
    
    STATUS_CHOICES = [
        ('OPENED', 'Opened'),
        ('IN_WORK', 'In Work'),
        ('COMPLETED', 'Completed'),
        ('ARCHIVED', 'Archived'),
    ]
    
    name = models.CharField(max_length=255, blank=True)
    initiator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='initiated_chats')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_chats', null=True, blank=True)
    conversation_type = models.CharField(max_length=20, choices=CONVERSATION_TYPES, default='general')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPENED')
    location = models.CharField(max_length=255, blank=True)
    provider_name = models.CharField(max_length=255, blank=True)
    categories = models.JSONField(default=list, blank=True)
    author_name = models.CharField(max_length=255, blank=True, default='User')
    is_statement_owner = models.BooleanField(default=False)
    
    # Добавляем связь с заявкой
    statement = models.ForeignKey(
        'statements.Statement', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='chat_rooms'
    )
    
    # Добавляем связь с жалобой
    complaint = models.ForeignKey(
        'objects.Complaint', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='chat_rooms'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"Chat {self.id} - {self.conversation_type}"
    
    @property
    def last_message(self):
        return self.messages.order_by('-timestamp').first()


class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"Message from {self.sender.phone} in {self.chat_room}"


class MessageAttachment(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='chat_attachments/')
    filename = models.CharField(max_length=255)
    file_size = models.IntegerField()
    content_type = models.CharField(max_length=100)
    
    def __str__(self):
        return f"Attachment: {self.filename}" 