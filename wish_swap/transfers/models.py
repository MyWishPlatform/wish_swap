from django.db import models
from wish_swap.payments.models import Payment


class Transfer(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    address = models.CharField(max_length=50)
    tx_hash = models.CharField(max_length=100)
    tx_error = models.TextField(default='')
    currency = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=100, decimal_places=0)
    status = models.CharField(max_length=50, default='WAITING FOR TRANSFER')
