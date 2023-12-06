from django import forms

class MpesaExpressForm(forms.Form):
    amount = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    account_reference = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    transaction_description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

class B2CForm(forms.Form):
    amount = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    remarks = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    occasion = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

class C2BRegisterURLsForm(forms.Form):
    pass

class C2BSimulateTransactionForm(forms.Form):
    amount = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    bill_reference = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

class TransactionStatusForm(forms.Form):
    transaction_id = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

class AccountBalanceForm(forms.Form):
    pass

class ReversalForm(forms.Form):
<<<<<<< HEAD
<<<<<<< HEAD
    transaction_id = forms.CharField()
    amount = forms.IntegerField()
    remarks = forms.CharField()
    occasion = forms.CharField()
=======
=======
>>>>>>> origin/alter
    transaction_id = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    amount = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    remarks = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    occasion = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
<<<<<<< HEAD
>>>>>>> 3f0fe0a (db)
=======
>>>>>>> origin/alter
