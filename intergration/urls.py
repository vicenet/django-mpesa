from django.urls import path
from . import views

urlpatterns = [
    path('mpesa_express/', views.mpesa_express, name='mpesa_express'),
    path('b2c/', views.b2c, name='b2c'),
    path('c2b_register_urls/', views.c2b_register_urls, name='c2b_register_urls'),
    path('c2b/simulate/', views.c2b_simulate_transaction, name='c2b_simulate'),
    path('callback/',views.callback,name='callback'),
    path('account_balance/', views.account_balance, name='account_balance'),
    path('transaction_status/', views.transaction_status, name='transaction_status'),
    path('reversal/', views.reversal, name='reversal'),
]
