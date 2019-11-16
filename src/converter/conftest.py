from typing import List
from unittest import mock
import pytest
from django.conf import settings
import json as json_lib

from converter.models import USDCurrencyPair


def requests_get(*args, **kwargs):
    class FakeResponse:
        def __init__(self):
            with open(settings.BASE_DIR + '/converter/test_data/test_response.json') as file:
                self.content = file.read()

        def json(self, *args, **kwargs):
            return json_lib.loads(self.content)

    return FakeResponse()


@pytest.fixture()
def mock_request_get_currency():
    with mock.patch('requests.get', requests_get):
        yield


@pytest.fixture
@pytest.mark.django_db
def currency_pairs() -> List[USDCurrencyPair]:
    return [
        USDCurrencyPair.objects.create(
            currency_code='EUR',
            currency_amount=0.904871,
        ),
        USDCurrencyPair.objects.create(
            currency_code='CZK',
            currency_amount=23.1576,
        ),
        USDCurrencyPair.objects.create(
            currency_code='PLN',
            currency_amount=3.868084,
        ),
        USDCurrencyPair.objects.create(
            currency_code='RUB',
            currency_amount=63.748,
        ),
        USDCurrencyPair.objects.create(
            currency_code='USD',
            currency_amount=1,
        ),

    ]
