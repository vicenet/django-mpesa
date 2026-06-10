# django-mpesa

Django integration with Safaricom's **Daraja API** for processing M-Pesa transactions — STK push, callbacks, and account balance queries.

## Features

- M-Pesa payment processing in sandbox or production
- Transaction result and queue timeout callbacks
- Account balance queries
- Configurable entirely through Django settings

## Setup

Add your Daraja API credentials to `settings.py`:

```python
# Environment: "sandbox" or "production"
MPESA_ENVIRONMENT = "sandbox"

# API credentials (from the Daraja developer portal)
MPESA_CONSUMER_KEY = "<your-consumer-key>"
MPESA_CONSUMER_SECRET = "<your-consumer-secret>"
MPESA_PASSKEY = "<your-passkey>"
MPESA_SHORT_CODE = "<your-shortcode>"

# Initiator credentials
MPESA_INITIATOR_NAME = "<initiator-username>"
MPESA_INITIATOR_PASSWORD = "<initiator-password>"

# Callback URLs
MPESA_RESULT_URL = "https://yourdomain.com/api/result/"
MPESA_QUEUE_TIMEOUT_URL = "https://yourdomain.com/api/timeout/"
MPESA_CALLBACK_URL = "https://yourdomain.com/api/callback/"

# Account balance callbacks
MPESA_ACCOUNT_BALANCE_TIMEOUT = "https://yourdomain.com/api/balance/timeout/"
MPESA_ACCOUNT_BALANCE_RESULT = "https://yourdomain.com/api/balance/result/"
```

## Getting Started

```bash
git clone https://github.com/vicenet/django-mpesa.git
cd django-mpesa
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Roadmap

- Styled UI for the payment flow
- Test coverage for callback handling

## License

MIT

---

Built by [Brian Gitau](https://github.com/vicenet)
