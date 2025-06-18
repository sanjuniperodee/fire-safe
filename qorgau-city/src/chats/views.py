from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import ChatRoom, Message
from .serializers import (
    ChatRoomSerializer, 
    ChatRoomListSerializer, 
    MessageSerializer,
    StartConversationSerializer
)

User = get_user_model()


class ChatRoomViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ChatRoomListSerializer
        return ChatRoomSerializer
    
    def get_queryset(self):
        user = self.request.user
        queryset = ChatRoom.objects.filter(
            Q(initiator=user) | Q(receiver=user)
        ).select_related('initiator', 'receiver').prefetch_related('messages')
        
        # Фильтрация по статусу
        status_filter = self.request.query_params.get('statement_status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
            
        return queryset
    
    @action(detail=False, methods=['post'], url_path='statement/start')
    def start_statement_conversation(self, request):
        """Начать разговор для заявления"""
        serializer = StartConversationSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            
            # Попытаться найти пользователя по телефону
            try:
                receiver = User.objects.get(phone=phone)
            except User.DoesNotExist:
                receiver = None
            
            chat_room = ChatRoom.objects.create(
                initiator=request.user,
                receiver=receiver,
                conversation_type='statement',
                author_name=f"{request.user.first_name} {request.user.last_name}".strip()
            )
            
            serializer = ChatRoomSerializer(chat_room)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'], url_path='statement')
    def get_statement_conversation(self, request, pk=None):
        """Получить разговор для заявления"""
        try:
            chat_room = self.get_queryset().get(pk=pk, conversation_type='statement')
            serializer = ChatRoomSerializer(chat_room)
            return Response(serializer.data)
        except ChatRoom.DoesNotExist:
            return Response(
                {'error': 'Conversation not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['get'], url_path='complaint')
    def get_complaint_conversation(self, request, pk=None):
        """Получить разговор для жалобы"""
        try:
            chat_room = self.get_queryset().get(pk=pk, conversation_type='complaint')
            serializer = ChatRoomSerializer(chat_room)
            return Response(serializer.data)
        except ChatRoom.DoesNotExist:
            return Response(
                {'error': 'Conversation not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'], url_path='statement')
    def list_statement_conversations(self, request):
        """Список всех разговоров для заявлений"""
        queryset = self.get_queryset().filter(conversation_type='statement')
        serializer = ChatRoomListSerializer(queryset, many=True)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        chat_room_id = self.request.query_params.get('chat_room')
        if chat_room_id:
            return Message.objects.filter(
                chat_room_id=chat_room_id,
                chat_room__in=ChatRoom.objects.filter(
                    Q(initiator=self.request.user) | Q(receiver=self.request.user)
                )
            ).select_related('sender', 'chat_room')
        return Message.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user) 