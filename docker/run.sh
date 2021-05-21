#!/usr/bin/env bash

cd /ps102_multistreamer/ || exit 1
python manage.py migrate
python manage.py collectstatic --noinput
daphne -b 0.0.0.0 -p 8082 --access-log /var/log/ps102_multistreamer/daphne_access.log multistreamer.asgi:application
