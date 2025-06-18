import random

import requests
from django.conf import settings
from sms_gateway.smsc.smsc_api import *


def generate_sms_code():
    code = str(random.randint(100000, 999999))

    return code


def send_sms_code(cpn, code):
    login = settings.OTP_LOGIN
    password = settings.OTP_PASSWORD
    senderid = settings.OTP_SENDER_ID
    url = settings.OTP_HOST

    payload = f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
            <soapenv:Header/>
            <soapenv:Body>
            <tem:SendSMSService___SendMessage>
            <tem:login>{login}</tem:login>
            <tem:password>{password}</tem:password>
            <tem:sms>
            <tem:recepient>{cpn}</tem:recepient>
            <tem:senderid>{senderid}</tem:senderid>
            <tem:msg>Код активации {code}\nссылка на сайт https://qorgau-city.kz/</tem:msg>
            <tem:msgtype>0</tem:msgtype>
            <tem:scheduled></tem:scheduled>
            <tem:UserMsgID>1</tem:UserMsgID>
            <tem:prioritet>0</tem:prioritet>
            </tem:sms>
            </tem:SendSMSService___SendMessage>
            </soapenv:Body>
            </soapenv:Envelope>"""
    headers = {
        'SOAPAction': 'urn:SendSMSLib-SendSMSService#SendMessage',
        'User-Agent': 'Apidog/1.0.0 (https://apidog.com)',
        'Content-Type': 'text/xml'
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    return response


def smsc_send_sms_code(cpn, code):
    smsc = SMSC()
    smsc.send_sms(str(cpn), str(code), sender=settings.SMSC_OTP_SENDER_ID)
