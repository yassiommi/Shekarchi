#!/bin/bash
redis-server &> out/logs/redis.log &

if pgrep -x "flask" > /dev/null
then
    killall flask
fi
export FLASK_APP=app.api
flask run --host=0.0.0.0 --port=5000 &> out/logs/flask.log &

if pgrep -x "celery" > /dev/null
then
    killall celery
fi
celery -A app.celery.celery worker -l debug &> out/logs/celery.log &
