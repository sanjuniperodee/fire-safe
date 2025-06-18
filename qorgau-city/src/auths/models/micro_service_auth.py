import logging

import jwt
from django.conf import settings
from rest_framework import authentication
from rest_framework import exceptions

logger = logging.getLogger(__name__)

JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 60 * 60  # 1 hour

SECRET_KEY = settings.MICROSERVICE_JWT_SECRET_KEY
ALLOWED_SERVICES = settings.MICROSERVICE_ALLOWED_SERVICES


def validate_jwt_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload['service'], payload['secret_key']
    except jwt.ExpiredSignatureError:
        logger.warning("JWT token has expired")
        raise exceptions.AuthenticationFailed('JWT token has expired')
    except jwt.InvalidTokenError as e:
        logger.warning(f"Invalid JWT token: {str(e)}")
        raise exceptions.AuthenticationFailed('Invalid JWT token')


class MicroserviceJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            logger.warning("No Authorization header found")
            return None

        try:
            auth_type, jwt_token = auth_header.split()
            if auth_type.lower() != 'bearer':
                logger.warning(f"Invalid auth type: {auth_type}")
                raise exceptions.AuthenticationFailed('Invalid token type')
        except ValueError:
            logger.warning("Invalid Authorization header format")
            raise exceptions.AuthenticationFailed('Invalid token header')

        service_name, secret_key = validate_jwt_token(jwt_token)
        logger.info(f'service_name in micro_service_auth: {service_name}')
        logger.info(f'service_name in secret_key: {secret_key}')

        if service_name not in ALLOWED_SERVICES:
            raise exceptions.AuthenticationFailed('Unknown service. It is not in Allowed Services')
        if not service_name and secret_key == SECRET_KEY:
            logger.warning("JWT token secret key validation failed")
            raise exceptions.AuthenticationFailed('Invalid or expired token(secret key mismatch)')

        logger.info(f"Successfully authenticated service: {service_name}")
        return (service_name, None)
