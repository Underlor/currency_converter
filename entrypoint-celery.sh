#!/bin/sh

exec celery -A currency_converter worker -l info
