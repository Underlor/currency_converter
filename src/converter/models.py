from django.db import models


class USDCurrencyPair(models.Model):
    currency_code = models.CharField(max_length=3, unique=True)
    currency_amount = models.FloatField()
