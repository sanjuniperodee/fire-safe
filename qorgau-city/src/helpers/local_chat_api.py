from django.contrib.auth import get_user_model
from chats.models import ChatRoom, Message
from statements.models import Statement
from objects.models import Complaint
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


def create_statement_chat_room(
        phone_1, phone_2,
        categories=None, location="",
        author_name="", provider_name="",
        statement_provider_id=0,
        statement_id=None
):
    """
    Создать комнату чата для заявления
    
    Args:
        phone_1: телефон инициатора
        phone_2: телефон получателя
        categories: категории (список)
        location: местоположение
        author_name: имя автора
        provider_name: имя провайдера
        statement_provider_id: ID statement_provider (для совместимости)
        statement_id: ID заявления
        
    Returns:
        int: ID созданной комнаты чата
    """
    try:
        logger.info(f"Creating statement chat room between {phone_1} and {phone_2}")
        
        # Найти пользователей по телефонам
        try:
            initiator = User.objects.get(phone=phone_1)
            logger.info(f"Found initiator: {initiator.id} ({initiator.phone})")
        except User.DoesNotExist:
            logger.error(f"Initiator with phone {phone_1} not found")
            raise ValueError(f"User with phone {phone_1} not found")
            
        try:
            receiver = User.objects.get(phone=phone_2)
            logger.info(f"Found receiver: {receiver.id} ({receiver.phone})")
        except User.DoesNotExist:
            logger.warning(f"Receiver with phone {phone_2} not found, setting to None")
            receiver = None
            
        # Получить заявление если указан ID
        statement = None
        if statement_id:
            try:
                statement = Statement.objects.get(id=statement_id)
                logger.info(f"Found statement: {statement.id}")
            except Statement.DoesNotExist:
                logger.warning(f"Statement with ID {statement_id} not found")
                pass
        
        # Создать комнату чата
        # Ensure we have valid names with multiple fallbacks
        final_author_name = (
            author_name 
            or (initiator.first_name if initiator.first_name else None)
            or (initiator.last_name if initiator.last_name else None)
            or (initiator.organization_name if hasattr(initiator, 'organization_name') and initiator.organization_name else None)
            or initiator.phone 
            or f"User-{initiator.id}"
        )
        
        final_provider_name = (
            provider_name 
            or (receiver.first_name if receiver and receiver.first_name else None)
            or (receiver.last_name if receiver and receiver.last_name else None)
            or (receiver.organization_name if receiver and hasattr(receiver, 'organization_name') and receiver.organization_name else None)
            or (receiver.phone if receiver else None)
            or f"Provider-{receiver.id if receiver else 'Unknown'}"
        )
        
        logger.info(f"Creating chat room with author_name='{final_author_name}', provider_name='{final_provider_name}'")
        
        chat_room = ChatRoom.objects.create(
            initiator=initiator,
            receiver=receiver,
            conversation_type='statement',
            location=location or '',
            provider_name=final_provider_name,
            categories=categories or [],
            author_name=final_author_name,
            statement=statement,
            status='OPENED'
        )
        
        logger.info(f"Created statement chat room {chat_room.id} between {phone_1} and {phone_2}")
        return chat_room.id
        
    except ValueError as e:
        # Re-raise ValueError for missing users
        logger.error(f"ValueError in create_statement_chat_room: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in create_statement_chat_room: {e}")
        import traceback
        traceback.print_exc()
        raise


def create_complaint_chat_room(phone_1, phone_2, complaint_id=0):
    """
    Создать комнату чата для жалобы
    
    Args:
        phone_1: телефон инициатора
        phone_2: телефон получателя  
        complaint_id: ID жалобы
        
    Returns:
        int: ID созданной комнаты чата
    """
    try:
        # Найти пользователей по телефонам
        initiator = User.objects.get(phone=phone_1)
        try:
            receiver = User.objects.get(phone=phone_2)
        except User.DoesNotExist:
            receiver = None
            
        # Получить жалобу если указан ID
        complaint = None
        if complaint_id:
            try:
                complaint = Complaint.objects.get(id=complaint_id)
            except Complaint.DoesNotExist:
                pass
        
        # Создать комнату чата
        chat_room = ChatRoom.objects.create(
            initiator=initiator,
            receiver=receiver,
            conversation_type='complaint',
            complaint=complaint,
            status='OPENED'
        )
        
        logger.info(f"Created complaint chat room {chat_room.id} between {phone_1} and {phone_2}")
        return chat_room.id
        
    except User.DoesNotExist:
        logger.error(f"User with phone {phone_1} not found")
        raise ValueError(f"User with phone {phone_1} not found")
    except Exception as e:
        logger.error(f"Failed to create complaint chat room: {e}")
        raise


def change_statement_status(statement_provider_id, status):
    """
    Изменить статус заявления (заглушка для совместимости)
    
    Args:
        statement_provider_id: ID statement_provider
        status: новый статус
        
    Returns:
        str: статус
    """
    # Эта функция должна быть реализована в зависимости от логики StatementProvider
    logger.info(f"Changing statement provider {statement_provider_id} status to {status}")
    return status


def delete_complaint_chat_room(complaint_conversation_id):
    """
    Удалить комнату чата жалобы
    
    Args:
        complaint_conversation_id: ID комнаты чата
        
    Returns:
        bool: True если удаление прошло успешно
    """
    try:
        chat_room = ChatRoom.objects.get(id=complaint_conversation_id, conversation_type='complaint')
        chat_room.delete()
        logger.info(f"Deleted complaint chat room {complaint_conversation_id}")
        return True
    except ChatRoom.DoesNotExist:
        logger.error(f"Complaint chat room {complaint_conversation_id} not found")
        raise ValueError(f"Complaint chat room {complaint_conversation_id} not found")
    except Exception as e:
        logger.error(f"Failed to delete complaint chat room: {e}")
        raise


def register_user_to_chat(phone, password):
    """
    Регистрация пользователя в чате (заглушка для совместимости)
    Теперь чат интегрирован в основную систему, поэтому регистрация не нужна
    
    Args:
        phone: телефон пользователя
        password: пароль пользователя
        
    Returns:
        str: ключ регистрации (None для локального чата)
    """
    # Для локального чата регистрация не нужна
    logger.info(f"Local chat registration for {phone} - no action needed")
    return None 