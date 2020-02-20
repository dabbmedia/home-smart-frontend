#!/bin/bash
cd /usr/share/nginx/html
uwsgi -s /tmp/home_smart.sock --manage-script-name --mount /=home_smart:create_app --chdir=/usr/share/nginx/html --master
# uwsgi --ini /usr/share/uwsgi.ini
nginx -s reload