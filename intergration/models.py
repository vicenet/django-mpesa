from django.db import models

# Create your models here.
class AccessToken(models.Model):
	token = models.CharField(max_length=30)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		get_latest_by = 'created_at'

	def __str__(self):
		return self.token


class B2CTransaction(models.Model):
    transaction_id = models.CharField(max_length=100)
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
    receiver_party = models.CharField(max_length=100)
    transaction_completed_time = models.DateTimeField()

    def __str__(self):
        return self.transaction_id

class Payment(models.Model):
    transaction_type = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=100)
    transaction_time = models.CharField(max_length=100)
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
    business_short_code = models.CharField(max_length=100)
    bill_reference_number = models.CharField(max_length=100)
    invoice_number = models.CharField(max_length=100)
    org_account_balance = models.CharField(max_length=100)
    third_party_trans_id = models.CharField(max_length=100)
    msisdn = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.transaction_id} - {self.transaction_amount} - {self.transaction_time}'
