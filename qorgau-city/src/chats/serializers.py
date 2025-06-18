from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ChatRoom, Message, MessageAttachment

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone', 'email', 'first_name', 'last_name']


class MessageAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageAttachment
        fields = ['id', 'file', 'filename', 'file_size', 'content_type']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    attachments = MessageAttachmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'text', 'timestamp', 'sender', 'attachments', 'is_read']


class ChatRoomSerializer(serializers.ModelSerializer):
    initiator = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    last_message = MessageSerializer(read_only=True)
    message_set = MessageSerializer(source='messages', many=True, read_only=True)
    statement = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatRoom
        fields = [
            'id', 'name', 'initiator', 'receiver', 'conversation_type', 
            'status', 'location', 'provider_name', 'categories', 
            'author_name', 'is_statement_owner', 'created_at', 
            'updated_at', 'last_message', 'message_set', 'statement'
        ]
    
    def get_statement(self, obj):
        if obj.statement:
            return {
                'id': obj.statement.id,
                'status': getattr(obj.statement, 'status', 'OPENED'),
                'created_at': obj.statement.created_at,
                'updated_at': getattr(obj.statement, 'updated_at', obj.statement.created_at),
            }
        return None


class ChatRoomListSerializer(serializers.ModelSerializer):
    initiator = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    last_message = MessageSerializer(read_only=True)
    statement = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatRoom
        fields = [
            'id', 'name', 'initiator', 'receiver', 'conversation_type', 
            'status', 'location', 'provider_name', 'categories', 
            'author_name', 'is_statement_owner', 'created_at', 
            'updated_at', 'last_message', 'statement'
        ]
    
    def get_statement(self, obj):
        if obj.statement:
            return {
                'id': obj.statement.id,
                'status': getattr(obj.statement, 'status', 'OPENED'),
                'created_at': obj.statement.created_at,
                'updated_at': getattr(obj.statement, 'updated_at', obj.statement.created_at),
            }
        return None


class StartConversationSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)
    conversation_type = serializers.ChoiceField(
        choices=ChatRoom.CONVERSATION_TYPES, 
        default='general'
    ) 