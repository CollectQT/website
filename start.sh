#!/bin/sh

export PIXYWERK_CONFIG=/home/production/CollectQT/collectqt.conf
gunicorn -b 127.0.0.1:9001 -w 1 -t 1 --keep-alive=2 --graceful-timeout=2 -t 10 -w 2  --preload pixywerk.wsgi:do_werk

