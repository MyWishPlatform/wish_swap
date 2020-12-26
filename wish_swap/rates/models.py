from django.db import models
from wish_swap.settings import CRYPTOCOMPARE_API_KEY, CRYPTOCOMPARE_API_URL
import json
import requests


class WishCommission(models.Model):
    amount = models.DecimalField(max_digits=100, decimal_places=0, default=0)


class UsdRate(models.Model):
    ETH = models.FloatField()
    BNB = models.FloatField()
    datetime = models.DateTimeField(auto_now=True)

    def update(self):
        payload = {
            'fsym': 'USD',
            'tsyms': ['BNB', 'ETH'],
            'api_key': CRYPTOCOMPARE_API_KEY,
        }
        response = requests.get(CRYPTOCOMPARE_API_URL, params=payload)
        if response.status_code != 200:
            raise Exception(f'update rates: Cannon get rates')
        response_data = json.loads(response.text)

        self.ETH = response_data['ETH']
        self.BNB = response_data['BNB']
        self.save()
