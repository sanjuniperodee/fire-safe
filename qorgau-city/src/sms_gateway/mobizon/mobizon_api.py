import requests
from django.conf import settings

from helpers.xml_parser import XmlParser

from sms_gateway.base_sms import BaseSmsGateway
from sms_gateway.mobizon.exception import MobizonApiException


class MobizonApi(BaseSmsGateway):
    api_server = settings.SMS_API_SERVER
    api_version = settings.SMS_API_VERSION
    api_key = settings.SMS_API_KEY
    format = settings.SMS_OUTPUT_FORMAT
    force_http = settings.SMS_FORCE_HTTP

    def call(self, provider: str, method: str, **kwargs):
        if not provider:
            raise MobizonApiException('You must provide "provider" parameter to MobizonApi::call.')
        if not method:
            raise MobizonApiException('You must provide "method" parameter to MobizonApi::call.')

        query_params = self._get_query_params(kwargs)
        url = self._get_sms_service_url(provider.lower(), method.lower())

        response = requests.get(url, params=query_params)
        if response.status_code != 200:
            raise ValueError(f"Request send sms failed: {response.status_code}")

        return self._decode(response)

    def get_balance(self, **kwargs):
        query_params = self._get_query_params(kwargs)
        url = self._get_sms_service_url('user', 'getownbalance')
        response = requests.get(url, params=query_params)
        if response.status_code != 200:
            raise ValueError(f"Request send sms failed: {response.status_code}")

        return self._decode(response)

    def _get_sms_service_url(self, provider: str, method: str) -> str:
        http = 'http' if self.force_http else 'https'

        return f"{http}://{self.api_server}/service/{provider}/{method}"

    def _get_query_params(self, params) -> dict:
        mobizon_params = MobizonApi.__get_default_params()

        return {**params, **mobizon_params}

    def _decode(self, response_data):
        match self.format:
            case 'json':
                return response_data.json()
            case 'xml':
                return XmlParser.parse_xml(response_data.text)
            case _:
                raise ValueError("Data does not match any specific(json, xml)")

    @classmethod
    def __get_default_params(cls) -> dict:
        return {
            'api': cls.api_version,
            'apiKey': cls.api_key,
            'output': cls.format
        }
