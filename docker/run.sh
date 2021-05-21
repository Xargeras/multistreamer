#!/usr/bin/env bash

cd /ps102_multistreamer/ || exit 1
python3 manage.py migrate
python3 manage.py collectstatic --noinput
daphne -b 0.0.0.0 -p 8082 --access-log /var/log/ps102_multistreamer/daphne_access.log multistreamer.asgi:application
