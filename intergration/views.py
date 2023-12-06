import os
import base64
import datetime
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .essentials.core import MpesaAPI
from .models import *
from .forms import MpesaExpressForm, B2CForm, C2BRegisterURLsForm, C2BSimulateTransactionForm, TransactionStatusForm, AccountBalanceForm, ReversalForm

mpesa = MpesaAPI()

@csrf_exempt
def mpesa_express(request):
    business_short_code = os.getenv('MPESA_SHORT_CODE')
    passcode = os.getenv('MPESA_PASSKEY')

    current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    password = f'{business_short_code}{passcode}{current_time}'
    encoded_password = base64.b64encode(password.encode('utf-8')).decode('utf-8')
    if request.method == 'POST':
        form = MpesaExpressForm(request.POST)
        if form.is_valid():
            data = {
                'BusinessShortCode': business_short_code,
                'Password': encoded_password,
                'Timestamp': current_time,
                'TransactionType': 'CustomerPayBillOnline',
                'Amount': form.cleaned_data['amount'],
                'PartyA': mpesa.format_phone_number(form.cleaned_data['phone_number']),
                'PartyB': mpesa.short_code,
                'PhoneNumber': mpesa.format_phone_number(form.cleaned_data['phone_number']),
                'CallBackURL': mpesa.callback_url,
                'AccountReference': form.cleaned_data['account_reference'],
                'TransactionDesc': form.cleaned_data['transaction_description']
            }

            response = mpesa.api_call('mpesa/stkpush/v1/processrequest', payload=data)
            return JsonResponse(response.json())

    form = MpesaExpressForm()
    return render(request, 'intergration/mpesa_express.html', {'form': form})


@csrf_exempt
def b2c(request):
    if request.method == 'POST':
        form = B2CForm(request.POST)
        if form.is_valid():
            data = {
                'InitiatorName': mpesa.initiator_name,
                'SecurityCredential': mpesa.security_credential,
                'CommandID': 'BusinessPayment',
                'Amount': form.cleaned_data['amount'],
                'PartyA': mpesa.short_code,
                'PartyB': mpesa.format_phone_number(form.cleaned_data['phone_number']),
                'Remarks': form.cleaned_data['remarks'],
                'QueueTimeOutURL': mpesa.queue_timeout_url,
                'ResultURL': mpesa.result_url,
                'Occasion': form.cleaned_data['occasion']
            }

            response = mpesa.api_call('mpesa/b2c/v1/paymentrequest', payload=data)
            return JsonResponse(response.json())

    form = B2CForm()
    return render(request, 'intergration/b2c.html', {'form': form})


@csrf_exempt
def c2b_register_urls(request):
    if request.method == 'POST':
        form = C2BRegisterURLsForm(request.POST)
        if form.is_valid():
            data = {
                'ShortCode': mpesa.short_code,
                'ResponseType': 'Completed',
                'ConfirmationURL': mpesa.result_url,
                'ValidationURL': mpesa.result_url
            }

            response = mpesa.api_call('mpesa/c2b/v1/registerurl', payload=data)
            return JsonResponse(response.json())

    form = C2BRegisterURLsForm()
    return render(request, 'intergration/c2b_urls.html', {'form': form})


@csrf_exempt
def c2b_simulate_transaction(request):
    if request.method == 'POST':
        form = C2BSimulateTransactionForm(request.POST)
        if form.is_valid():
            data = {
                'ShortCode': mpesa.short_code,
                'CommandID': 'CustomerPayBillOnline',
                'Amount': form.cleaned_data['amount'],
                'Msisdn': mpesa.format_phone_number(form.cleaned_data['phone_number']),
                'BillRefNumber': form.cleaned_data['bill_reference']
            }

            response = mpesa.api_call('mpesa/c2b/v1/simulate', payload=data)
            return JsonResponse(response.json())

    form = C2BSimulateTransactionForm()
    return render(request, 'intergration/c2b_simulate.html', {'form': form})


@csrf_exempt
def transaction_status(request):
    if request.method == 'POST':
        form = TransactionStatusForm(request.POST)
        if form.is_valid():
            data = {
                'Initiator': mpesa.initiator_name,
                'SecurityCredential': mpesa.security_credential,
                'CommandID': 'TransactionStatusQuery',
                'TransactionID': form.cleaned_data['transaction_id'],
                'PartyA': mpesa.short_code,
                'IdentifierType': '4',
                'ResultURL': mpesa.result_url,
                'QueueTimeOutURL': mpesa.queue_timeout_url,
                'Remarks': '',
                'Occasion': ''
            }

            response = mpesa.api_call('mpesa/transactionstatus/v1/query', payload=data)
            return JsonResponse(response.json())

    form = TransactionStatusForm()
    return render(request, 'intergration/transaction_status.html', {'form': form})


@csrf_exempt
def account_balance(request):
    if request.method == 'POST':
        form = AccountBalanceForm(request.POST)
        if form.is_valid():
            data = {
                'Initiator': mpesa.initiator_name,
                'SecurityCredential': mpesa.security_credential,
                'CommandID': 'AccountBalance',
                'PartyA': '600995',
                'IdentifierType': '4',
                'Remarks': 'get balance information',
                'QueueTimeOutURL': os.getenv('MPESA_ACCOUNT_BALANCE_TIMEOUT'),
                'ResultURL': os.getenv('MPESA_ACCOUNT_BALANCE_RESULT')
            }

            response = mpesa.api_call('mpesa/accountbalance/v1/query', payload=data)
            return JsonResponse(response.json())

    form = AccountBalanceForm()
    return render(request, 'intergration/account_balance.html', {'form': form})


@csrf_exempt
def reversal(request):
    if request.method == 'POST':
        form = ReversalForm(request.POST)
        if form.is_valid():
            data = {
                'Initiator': mpesa.initiator_name,
                'SecurityCredential': mpesa.security_credential,
                'CommandID': 'TransactionReversal',
                'TransactionID': form.cleaned_data['transaction_id'],
                'Amount': form.cleaned_data['amount'],
                'ReceiverParty': '600981',
                'RecieverIdentifierType': '11',
                'ResultURL': 'https://mydomain.com/Reversal/result/',
                'QueueTimeOutURL': 'https://mydomain.com/Reversal/queue/',
                'Remarks': form.cleaned_data['remarks'],
                'Occasion': form.cleaned_data['occasion']
            }

            response = mpesa.api_call('mpesa/reversal/v1/request', payload=data)
            return JsonResponse(response.json())

    form = ReversalForm()
    return render(request, 'intergration/reversal.html', {'form': form})



@csrf_exempt
def callback(request):
    if request.method == 'POST':
        # Process the M-Pesa response here
        result_json = json.loads(request.body.decode('utf-8'))

        transaction_type = result_json.get('TransactionType')
        transaction_id = result_json.get('TransID')
        transaction_time = result_json.get('TransTime')
        transaction_amount = result_json.get('TransAmount')
        business_short_code = result_json.get('BusinessShortCode')
        bill_reference_number = result_json.get('BillRefNumber')
        invoice_number = result_json.get('InvoiceNumber')
        org_account_balance = result_json.get('OrgAccountBalance')
        third_party_trans_id = result_json.get('ThirdPartyTransID')
        msisdn = result_json.get('MSISDN')
        first_name = result_json.get('FirstName')
        middle_name = result_json.get('MiddleName')
        last_name = result_json.get('LastName')

        # Save the data to the database
        payment = Payment.objects.create(
            transaction_type=transaction_type,
            transaction_id=transaction_id,
            transaction_time=transaction_time,
            transaction_amount=transaction_amount,
            business_short_code=business_short_code,
            bill_reference_number=bill_reference_number,
            invoice_number=invoice_number,
            org_account_balance=org_account_balance,
            third_party_trans_id=third_party_trans_id,
            msisdn=msisdn,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name
        )

        # Prepare the JSON response
        response_data = {
            "ResultCode": "0",
            "ResultDesc": "Success"
        }
        response_json = json.dumps(response_data)

        # Return the JSON response
        return HttpResponse(response_json, content_type='application/json')

    return HttpResponse('Method not allowed', status=405)
