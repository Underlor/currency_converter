#!/bin/sh

set -e
./manage.py migrate

exec uwsgi --http :${LISTEN_PORT} --module currency_converter.wsgi
