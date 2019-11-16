#!/bin/sh

exec celery -A currency_converter beat -l info
