from datetime import datetime

import requests
from celery import shared_task
from django.conf import settings

from converter.models import USDCurrencyPair


class ApiError(Exception):
    pass


@shared_task
def parse_exchange_rates_task():
    response = requests.get(settings.EXCHANGE_RATE_URL, params={'app_id': settings.APP_ID})
    response_data = response.json()

    if response_data.get('error'):
        raise ApiError(response_data.get('message'))

    for curr_code, rate in response_data.get('rates').items():
        USDCurrencyPair.objects.update_or_create(currency_code=curr_code, currency_amount=rate)

    USDCurrencyPair.objects.update_or_create(currency_code='USD', currency_amount=1)

    return f"Data updated {datetime.utcfromtimestamp(response_data.get('timestamp'))}"
