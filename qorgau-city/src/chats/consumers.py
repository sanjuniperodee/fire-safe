import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from .models import ChatRoom, Message, MessageAttachment
from .serializers import MessageSerializer
import jwt
from django.conf import settings

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'
        self.user = await self.get_user_from_token()
        
        if not self.user or self.user.is_anonymous:
            print(f"User authentication failed for room {self.room_id}")
            await self.close()
            return
        
        # Проверить доступ к комнате
        has_access = await self.check_room_access()
        if not has_access:
            print(f"User {self.user.id} has no access to room {self.room_id}")
            await self.close()
            return
        
        # Присоединиться к группе комнаты
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        print(f"User {self.user.id} connected to room {self.room_id}")
        await self.accept()
    
    async def disconnect(self, close_code):
        # Покинуть группу комнаты
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(f"User disconnected from room {self.room_id}")
    
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
                print("No token found in query parameters")
                return None
            
            # Убрать URL encoding если есть
            import urllib.parse
            token_param = urllib.parse.unquote(token_param)
            
            # Убрать префикс "Bearer " если есть
            if token_param.startswith('Bearer '):
                token_param = token_param[7:]
            
            print(f"Attempting to decode token: {token_param[:50]}...")
            
            try:
                # Используем SIMPLE_JWT для декодирования токена
                from rest_framework_simplejwt.tokens import AccessToken
                
                # Создаем объект токена
                access_token = AccessToken(token_param)
                user_id = access_token['user_id']
                
                if user_id:
                    user = User.objects.get(id=user_id)
                    print(f"Successfully authenticated user: {user.phone}")
                    return user
                else:
                    print("No user_id found in token")
                    return None
                    
            except Exception as token_error:
                print(f"Token validation error: {token_error}")
                # Fallback: try manual decoding with SECRET_KEY
                try:
                    decoded_token = jwt.decode(
                        token_param, 
                        settings.SECRET_KEY, 
                        algorithms=['HS256']
                    )
                    user_id = decoded_token.get('user_id')
                    
                    if user_id:
                        user = User.objects.get(id=user_id)
                        print(f"Successfully authenticated user with fallback: {user.phone}")
                        return user
                    else:
                        print("No user_id found in fallback token")
                        return None
                        
                except Exception as fallback_error:
                    print(f"Fallback token validation also failed: {fallback_error}")
                    return None
                
        except Exception as e:
            print(f"Error getting user from token: {e}")
            return None
    
    @database_sync_to_async
    def check_room_access(self):
        """Проверить доступ пользователя к комнате"""
        try:
            chat_room = ChatRoom.objects.get(id=self.room_id)
            has_access = (chat_room.initiator == self.user or 
                         chat_room.receiver == self.user or
                         self.user.is_staff)
            print(f"Room access check for user {self.user.id}: {has_access}")
            return has_access
        except ChatRoom.DoesNotExist:
            print(f"ChatRoom {self.room_id} does not exist")
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