# import os
import random
import math
from django.core.files.storage import default_storage
from datetime import datetime, time, date, timedelta
from django.core.cache import cache

# from sms_gateway.mobizon.mobizon_api import MobizonApi
from helpers.logger import log_message
from sms_gateway.smsc.smsc_utils import generate_sms_code, smsc_send_sms_code


def convert_datetime(obj):
    if isinstance(obj, (time, date, datetime)):
        return obj.isoformat()
    return obj


def delete_file(file_path):
    try:
        if default_storage.exists(file_path):
            default_storage.delete(file_path)
    except Exception as e:
        print(f"Error deleting file: {e}")


def generate_activation_code():
    return str(random.randint(100000, 999999))


def generate_alphanumeric(length):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    digits = "0123456789"
    chars = letters + digits
    return ''.join(random.choice(chars) for _ in range(length))


def generate_doc_code():
    return f"{random.randint(10, 99)}-{random.randint(1000, 9999)}"


def upload_file_to_s3(folder, file, upload_filename):
    """Загружает файл в S3-хранилище"""
    # Проверяем размер файла
    file_size = file.size

    # Если файл больше 10 МБ, возвращаем ошибку
    max_file_size = 10 * 1024 * 1024  # 10 МБ в байтах
    if file_size > max_file_size:
        raise ValueError("Размер файла превышает максимально допустимый размер (10 МБ)")

    # Строим путь для сохранения
    file_path = f"{folder}/{upload_filename}"

    # Сохраняем файл
    file_name = default_storage.save(file_path, file)

    # Возвращаем URL файла
    return default_storage.url(file_name)


def get_average_rating(user):
    # Получаем все рейтинги для данного пользователя
    feedback_queryset = user.feedback_received.all()

    # Подсчитываем количество отзывов и сумму рейтингов
    total_feedback = feedback_queryset.count()

    if total_feedback == 0:
        return 0  # Если отзывов нет, возвращаем 0

    # Подсчитываем сумму рейтингов
    total_rating = sum(feedback.rating for feedback in feedback_queryset)

    # Возвращаем средний рейтинг, округленный до одного знака после запятой
    average_rating = total_rating / total_feedback
    return round(average_rating, 1)


def has_passed_30_minutes(time_str):
    try:
        time_obj = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
        current_time = datetime.now()
        time_difference = current_time - time_obj
        return time_difference >= timedelta(minutes=30)
    except:
        return True


def calculation_building_rating(python_list) -> int:
    fileIdsCount = 0
    for topic in python_list:
        if 'keys' in topic:
            keys = topic['keys']
            for key in keys:
                if len(key['fileIds']) > 0:
                    fileIdsCount += 1
        else:
            subs = topic['subParagraphs']
            for sub in subs:
                keys = sub['keys']
                for key in keys:
                    if len(key['fileIds']) > 0:
                        fileIdsCount += 1

    completionPercentage = (fileIdsCount / 166) * 100
    finalRating = None

    if 0 <= completionPercentage <= 33:
        finalRating = 3
    elif 33 < completionPercentage <= 66:
        finalRating = 2
    elif 66 < completionPercentage <= 100:
        finalRating = 1

    return finalRating


def send_sms_confirmation_code(phone):
    phone = phone.replace("+", "")
    # mobizon = MobizonApi()
    # activation_code = generate_activation_code()
    activation_code = generate_sms_code()

    cache_key = f'confirmation_code:{phone}'
    result = cache.set(cache_key, activation_code)
    log_message(f"cache_key {cache_key}, code {activation_code}, result {result}")

    params = {
        'recipient': phone,
        'text': f'Код подтверждения {activation_code}\nссылка на сайт https://qorgau-city.kz/',
    }
    # mobizon.call('message', 'sendSMSMessage', **params)
    # smsc_send_sms_code(phone.replace("+", ""), activation_code)

    log_message(str(params))
    
    # Возвращаем код для отладки (временно, пока SMS сервис не работает)
    return activation_code
