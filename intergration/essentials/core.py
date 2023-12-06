import base64
import datetime
import json
import os
import subprocess
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.primitives.serialization import load_der_public_key
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.backends import default_backend
import requests
from django.conf import settings
from django.utils import timezone
from .exceptions import *
from intergration.models import AccessToken

certificate_name = 'sandbox.cer'

class MpesaAPI:
    def __init__(self):
        self.short_code = self.mpesa_config('MPESA_SHORT_CODE')
        self.initiator_name = self.mpesa_config('MPESA_INITIATOR_NAME')
        self.encrypt_security_credential(self.mpesa_config('MPESA_INITIATOR_PASSWORD'))
        self.result_url = self.mpesa_config('MPESA_RESULT_URL')
        self.queue_timeout_url = self.mpesa_config('MPESA_QUEUE_TIMEOUT_URL')
        self.callback_url = self.mpesa_config('MPESA_CALLBACK_URL')
        self.mpesa_passkey = self.mpesa_config('MPESA_PASSKEY')
        self.balance_url = self.mpesa_config('MPESA_ACCOUNT_BALANCE_RESULT')
        self.balance_timeout = self.mpesa_config('MPESA_ACCOUNT_BALANCE_TIMEOUT')
        self.security_credential = self.calculate_security_credential()

    def mpesa_config(self, key):
        value = getattr(settings, key, None)
        if value is None:
            raise MpesaConfigurationException(f'Mpesa environment not configured properly - {key} not found')
        return value

    def timestamp(self):
        return timezone.now().strftime('%Y%m%d%H%M%S')

    def format_phone_number(self, phone_number):
        if len(phone_number) < 9:
            raise IllegalPhoneNumberException('Phone number too short')
        else:
            return '254' + phone_number[-9:]


    def encrypt_security_credential(self, credential):
        mpesa_environment = self.mpesa_config('MPESA_ENVIRONMENT')

        if mpesa_environment in ('development', 'sandbox', 'production'):
            certificate_name = mpesa_environment + '.cer'
        else:
            raise MpesaConfigurationException('Mpesa environment not configured properly - MPESA_ENVIRONMENT should be sandbox or production')

        certificate_path = os.path.join(settings.BASE_DIR, 'certs', certificate_name)
        return self.encrypt_rsa(certificate_path, credential)

    def encrypt_rsa(self, certificate_path, input):
        message = input.encode('ascii')
        with open(certificate_path, "rb") as cert_file:
            cert = load_pem_x509_certificate(cert_file.read(), default_backend())
            public_key = cert.public_key()
            encrypted = public_key.encrypt(
                message,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=SHA256()),
                    algorithm=SHA256(),
                    label=None
                )
            )

            output = base64.b64encode(encrypted).decode('ascii')

        return output

    def generate_access_token_request(self, consumer_key=None, consumer_secret=None):
        url = self.api_base_url() + 'oauth/v1/generate?grant_type=client_credentials'
        consumer_key = consumer_key if consumer_key is not None else self.mpesa_config('MPESA_CONSUMER_KEY')
        consumer_secret = consumer_secret if consumer_secret is not None else self.mpesa_config('MPESA_CONSUMER_SECRET')

        try:
            r = requests.get(url, auth=(consumer_key, consumer_secret))
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise MpesaConnectionError(str(e))

        return r

    def generate_access_token(self):
        r = self.generate_access_token_request()
        if r.status_code != 200:
            raise MpesaError('Unable to generate access token')

        token = r.json().get('access_token')

        AccessToken.objects.all().delete()
        access_token = AccessToken.objects.create(token=token)

        return access_token

    def mpesa_access_token(self):
        access_token = AccessToken.objects.first()
        if access_token is None:
            access_token = self.generate_access_token()
        else:
            delta = timezone.now() - access_token.created_at
            minutes = delta.total_seconds() // 60
            if minutes > 50:
                access_token = self.generate_access_token()

        return access_token.token

    def api_base_url(self):
        mpesa_environment = self.mpesa_config('MPESA_ENVIRONMENT')

        if mpesa_environment == 'development':
            return 'https://darajasimulator.azurewebsites.net/'
        elif mpesa_environment == 'sandbox':
            return 'https://sandbox.safaricom.co.ke/'
        elif mpesa_environment == 'production':
            return 'https://api.safaricom.co.ke/'
        else:
            raise MpesaConfigurationException('Mpesa environment not configured properly - MPESA_ENVIRONMENT should be sandbox or production')

    def api_call(self, endpoint, method='POST', payload=None):
        access_token = self.mpesa_access_token()
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        url = self.api_base_url() + endpoint

        try:
            if method == 'POST':
                response = requests.post(url, headers=headers, json=payload)
            elif method == 'GET':
                response = requests.get(url, headers=headers)
            else:
                raise MpesaConfigurationException(f'Invalid HTTP method: {method}')

            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise MpesaConnectionError(str(e))

        return response

    def calculate_security_credential(self):
        password = self.mpesa_config('MPESA_INITIATOR_PASSWORD')
        certificate_path = os.path.join(settings.BASE_DIR, 'certs', certificate_name)

        # Read the certificate
        with open(certificate_path, 'rb') as cert_file:
            cert_data = cert_file.read()

        # Load the PEM certificate
        cert = load_pem_x509_certificate(cert_data, default_backend())

        # Get the public key from the certificate
        public_key = cert.public_key()

        # Encrypt the password using the public key
        encrypted = public_key.encrypt(
            password.encode('utf-8'),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=SHA256()),
                algorithm=SHA256(),
                label=None
            )
        )

        # Base64 encode the encrypted data
        security_credential = base64.b64encode(encrypted).decode('utf-8')

        return security_credential
