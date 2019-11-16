import json

import pytest
from django.urls import reverse

from converter.models import USDCurrencyPair
from converter.tasks import parse_exchange_rates_task


@pytest.mark.django_db
def test_parse_and_create_currency_pairs(mock_request_get_currency):
    """
        Test parsing and creating currency pairs
    """
    parse_exchange_rates_task()
    assert USDCurrencyPair.objects.count() == 171


@pytest.mark.django_db
@pytest.mark.parametrize(
    'from_code, to_code, amount, result',
    [
        ('EUR', 'RUB', 1, 70.44982102421228),
        ('EUR', 'RUB', 10, 704.4982102421228),
        ('EUR', 'CZK', 1, 25.592156230004054),
        ('EUR', 'CZK', 0.5, 12.796078115002027),
        ('CZK', 'CZK', 1, 1),
        ('CZK', 'EUR', 1, 0.03907447231146578),
        ('USD', 'EUR', 1, 0.904871),
        ('EUR', 'USD', 1, 1.1051299024943888),
    ],
)
def test_converter_api(currency_pairs, client, from_code, to_code, amount, result):
    response = client.get(reverse('convert'), {'from': from_code, 'to': to_code, 'amount': amount})
    response_data = json.loads(response.content)

    print(response_data)
    assert response.status_code == 200
    assert response_data.get('response') == result


@pytest.mark.parametrize(
    'amount',
    [
        (0,),
        (-1,),
        ('I am not an integer :)',),
        ('',),
    ],
)
def test_bad_amount_api(client, amount):
    response = client.get(reverse('convert'), {'from': 'USD', 'to': 'USD', 'amount': amount})
    response_data = json.loads(response.content)

    assert response.status_code == 400
    assert response_data.get('error')


@pytest.mark.django_db
@pytest.mark.parametrize(
    'from_code, to_code',
    [
        ("US", "EU"),
        ("UST", "EU1"),
        ("", ""),
    ],
)
def test_bad_currency_code_api(client, from_code, to_code):
    response = client.get(reverse('convert'), {'from': from_code, 'to': to_code, 'amount': 1})
    response_data = json.loads(response.content)

    assert response.status_code == 400
    assert response_data.get('error')
