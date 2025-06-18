import requests
import jwt
from datetime import datetime, timedelta
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# TODOS: Доработать Endpoint "Откликнуться". [DONE].

# TODOS: Провайдер после нажатия "Откликнуться" к определенному заказу больше не может второй раз откликаться. [DONE]

# TODOS: 1. Добавить Endpoint чтобы изменить статус переписки на "В работе".
#       Для того чтобы это произошло переписка должна иметь статус "Открыто".
#       Собственник имеет два выбора: Принять, Отказать.(Реализуется со стороны фронтэнда)    [DONE]
#       2. Собственник выбирает Принять:
#                                      a. Статус переписки меняется на "В работе": statements/response/status_in_work.
#                                      b. !!! Собственник больше не может принять провайдеров на этот заказ. !!!
#                                      Это мы можем контролировать добавляя поле статус для заказа. [DONE]
#       3. Собственник выбирает Отказать:
#                                       Статус переписки меняется на "В архиве" для провайдера: statements/response/archive_for_provider.
#                                       [DONE]
#
#
# TODOS: 1. Добавить Endpoint чтобы изменить статус переписки на "Выполнено". Для того чтобы это произошло
#       переписка должна иметь статус "В работе".
#       2. Провайдер отправляет запрос что работа выполнена на Endpoint: statements/response/status_completed_request_provider.
#                                       a. Будет создана "запрос на Выполнено".
#                                       b. Собственник принимает запрос имеет два выбора:
#                                       Принимать Работу, Не Принимать Работу(Таким образом отправить на переделку).
#                                           b-1. Когда принимается Работа статус созданного "запроса на Выполнено" будет True
#                                                и статус переписки поменяется на "Выполнено". [DONE]
#                                           b-2. Когда не принимается Работа статус созданного "запроса на Выполнено" будет False
#                                                и "запрос на Выполнено" удалится. [DONE]



JWT_SECRET_KEY = settings.MICROSERVICE_JWT_SECRET_KEY
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 60 * 60  # 1 hour

#SECRET_KEY = settings.MICROSERVICE_JWT_SECRET_KEY
THIS_SERVICE_NAME = settings.THIS_SERVICE_NAME


# API endpoints
API_BASE_URL = 'https://chapi.qorgau-city.kz/api/v1'
REGISTER_CHAT_URL = f'{API_BASE_URL}/auth/registration/'

# START_CHAT_URL = f'{API_BASE_URL}/conversations/start/'
START_STATEMENT_CALL_CHAT_URL = f'{API_BASE_URL}/conversations/statement/start/'
START_COMPLAINT_CHAT_URL = f'{API_BASE_URL}/conversations/complaint/start/'
CHANGE_STATEMENT_STATUS_URL = f'{API_BASE_URL}/conversations/update_statement_status/'

DELETE_COMPLAINT_CHAT_ROOM = f'{API_BASE_URL}/conversations/delete'


def generate_jwt_token():
    payload = {
        'service': THIS_SERVICE_NAME,
        'secret_key': JWT_SECRET_KEY,
        'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    jwt_token = jwt.encode(payload, JWT_SECRET_KEY, JWT_ALGORITHM)
    return jwt_token


def register_to_chat(phone, password):
    registration_key = None
    data = {
        "phone": phone,
        "password1": password,
        "password2": password
    }
    response = requests.post(REGISTER_CHAT_URL, json=data)
    # print(f'response is: {response.json()}')
    if response.status_code == 201:
        registration_key = response.json()['key']
    else:
        pass
        # raise Exception(f"Failed to register user to chat: {response.text}")
    return registration_key


def create_statement_chat_room(
        login_jwt_token,
        phone_1, phone_2,
        categories, location,
        author_name, provider_name,
        statement_provider_id=0,
):
    headers = {
        "Authorization": f"Bearer {login_jwt_token}",
        'Content-Type': 'application/json',
    }
    data = {
        "phone_1": phone_1,
        "phone_2": phone_2,
        "categories": categories,
        "location": location,
        "author_name": author_name,
        "provider_name": provider_name,
        "statement_provider_id": statement_provider_id,
    }

    response = requests.post(START_STATEMENT_CALL_CHAT_URL, json=data, headers=headers)
    # print(f'response is: {response.text}')
    # print(f'response code is {response.status_code}')

    if response.status_code == 201: # 200
        response_data = response.json()
        return response_data.get('id')
    raise Exception(f"Failed to create chat room: {response.text}")


def create_complaint_chat_room(login_jwt_token, phone_1, phone_2, complaint_id=0):
    headers = {
        "Authorization": f"Bearer {login_jwt_token}",
        'Content-Type': 'application/json',
    }
    data = {
        "phone1": phone_1,
        "phone2": phone_2,
        "complaint_id": complaint_id,
    }

    response = requests.post(START_COMPLAINT_CHAT_URL, json=data, headers=headers)
    # print(f'response is: {response.text}')
    # print(f'response code is {response.status_code}')

    if response.status_code == 201: # 200
        response_data = response.json()
        return response_data.get('id')
    raise Exception(f"Failed to create chat room: {response.text}")


def change_status_statement_provider(login_jwt_token, statement_provider_id, status):
    url = f'{CHANGE_STATEMENT_STATUS_URL}{statement_provider_id}/'

    headers = {
        "Authorization": f"Bearer {login_jwt_token}",
        'Content-Type': 'application/json',
    }
    data = {
        "status": status,
    }

    response = requests.patch(url, json=data, headers=headers)
    # print(f'response is: {response.text}')
    # print(f'response code is {response.status_code}')

    if response.status_code == 200:
        return response.json().get('status')
    raise Exception(f"Failed to change statement provider status: {response.text}")


def delete_complaint_chat_room(login_jwt_token, complaint_conversation_id):
    url = f'{DELETE_COMPLAINT_CHAT_ROOM}/{complaint_conversation_id}/'

    headers = {
        "Authorization": f"Bearer {login_jwt_token}",
        'Content-Type': 'application/json',
    }

    response = requests.delete(url, headers=headers)
    print(f'response is: {response.text}')
    print(f'response code is {response.status_code}')

    if response.status_code == 204:  # Successful deletion
        return True
    raise Exception(f"Failed to delete statement chat room: {response.text}")


# def create_chat_room(login_jwt_token, inspector_phone, conversation_type='UNKNOWN', complaint_id=0):
#     headers = {
#         "Authorization": f"Bearer {login_jwt_token}",
#         'Content-Type': 'multipart/form-data'
#     }
#     data = {
#         "phone": inspector_phone,
#         "conversation_type": conversation_type,
#         "statement_id": complaint_id,
#     }
#     response = requests.post(SERVER_START_CHAT_URL, json=data, headers=headers)
#     print(f'response is: {response.text}')
#     chat_room_id = response.json().get('id')
#     if response.status_code == 200:
#         return chat_room_id
#     else:
#         raise Exception(f"Failed to create chat room: {response.text}")
