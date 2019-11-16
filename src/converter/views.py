from celery.result import AsyncResult
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
from django.views import View

from converter.models import USDCurrencyPair
from converter.tasks import parse_exchange_rates_task


class IndexView(View):
    def get(self, request, *args, **kwargs):
        urls = {
            'convert': {
                'url': reverse('convert'),
                'description': {
                    'text': 'Currency converter.',
                    'params': {
                        'from': 'The base ("from") currency (3-letter code)',
                        'to': 'The base ("to") currency (3-letter code)',
                        'amount': 'The value to be converted',
                    }
                }
            },
            'force_update': {
                'url': reverse('force_update'),
                'description': {
                    'text': 'Force update exchange course.',
                }
            }
        }
        return JsonResponse({'api': urls}, json_dumps_params={'indent': 4})


class ForceUpdateView(View):
    def get(self, request, *args, **kwargs):
        parse_exchange_rates_task.apply()
        return JsonResponse({'success': 'true'})


class ConvertView(View):
    def get(self, request, *args, **kwargs):
        from_code = request.GET.get('from')
        to_code = request.GET.get('to')
        amount = request.GET.get('amount')

        if not (from_code or to_code or amount):
            return JsonResponse({'error': 'Invalid request'}, status=400)

        try:
            amount = float(amount)
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Bad "amount" value'}, status=400)

        if amount <= 0:
            return JsonResponse({'error': 'Amount must be more then 0'}, status=400)

        try:
            from_currency_amount = USDCurrencyPair.objects.get(currency_code=from_code).currency_amount
        except USDCurrencyPair.DoesNotExist:
            return JsonResponse({'error': 'Invalid "from" currency code'}, status=400)
        try:
            to_currency_amount = USDCurrencyPair.objects.get(currency_code=to_code).currency_amount
        except USDCurrencyPair.DoesNotExist:
            return JsonResponse({'error': 'Invalid "to" currency code'}, status=400)

        response = to_currency_amount / from_currency_amount * amount

        return JsonResponse({
            "request": {
                "amount": amount,
                "from": from_code,
                "to": to_code
            },
            "response": response
        })
