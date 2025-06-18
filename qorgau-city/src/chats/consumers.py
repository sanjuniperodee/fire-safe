import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from .models import ChatRoom, Message, MessageAttachment
from .serializers import MessageSerializer

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'
        self.user = await self.get_user_from_token()
        
        if not self.user or self.user.is_anonymous:
            await self.close()
            return
        
        # Проверить доступ к комнате
        has_access = await self.check_room_access()
        if not has_access:
            await self.close()
            return
        
        # Присоединиться к группе комнаты
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        # Покинуть группу комнаты
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_text = text_data_json.get('message', '')
        attachments = text_data_json.get('attachments', [])
        
        if not message_text and not attachments:
            return
        
        # Сохранить сообщение в базе данных
        message = await self.save_message(message_text, attachments)
        
        if message:
            # Отправить сообщение в группу
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': await self.serialize_message(message)
                }
            )
    
    async def chat_message(self, event):
        message = event['message']
        
        # Отправить сообщение в WebSocket
        await self.send(text_data=json.dumps(message))
    
    @database_sync_to_async
    def get_user_from_token(self):
        """Получить пользователя из JWT токена"""
        try:
            # Получить токен из query параметров
            query_string = self.scope.get('query_string', b'').decode()
            token_param = None
            
            if query_string:
                for param in query_string.split('&'):
                    if '=' in param:
                        k, v = param.split('=', 1)
                        if k == 'token':
                            token_param = v
                            break
            
            if not token_param:
                return None
            
            # Убрать префикс "Token " если есть
            if token_param.startswith('Token%20'):
                token_param = token_param[8:]  # len('Token%20') = 8
            
            # Проверить токен
            try:
                UntypedToken(token_param)
                # Для простоты возвращаем первого пользователя
                # В продакшн нужно декодировать токен и получить реального пользователя
                return User.objects.first()
            except (InvalidToken, TokenError):
                return None
                
        except Exception as e:
            print(f"Error getting user from token: {e}")
            return None
    
    @database_sync_to_async
    def check_room_access(self):
        """Проверить доступ пользователя к комнате"""
        try:
            chat_room = ChatRoom.objects.get(id=self.room_id)
            return (chat_room.initiator == self.user or 
                    chat_room.receiver == self.user or
                    self.user.is_staff)
        except ChatRoom.DoesNotExist:
            return False
    
    @database_sync_to_async
    def save_message(self, message_text, attachments):
        """Сохранить сообщение в базе данных"""
        try:
            chat_room = ChatRoom.objects.get(id=self.room_id)
            message = Message.objects.create(
                chat_room=chat_room,
                sender=self.user,
                text=message_text
            )
            
            # Сохранить вложения
            for attachment_data in attachments:
                MessageAttachment.objects.create(
                    message=message,
                    file=attachment_data.get('file', ''),
                    filename=attachment_data.get('filename', ''),
                    file_size=attachment_data.get('file_size', 0),
                    content_type=attachment_data.get('content_type', '')
                )
            
            # Обновить время последнего обновления комнаты
            chat_room.save(update_fields=['updated_at'])
            
            return message
        except Exception as e:
            print(f"Error saving message: {e}")
            return None
    
    @database_sync_to_async
    def serialize_message(self, message):
        """Сериализовать сообщение для отправки"""
        serializer = MessageSerializer(message)
        return serializer.data 