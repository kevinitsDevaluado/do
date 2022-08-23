#!/bin/bash

NAME="ftv"
DJANGODIR=$(dirname $(dirname $(cd `dirname $0` && pwd)))
SOCKFILE=/tmp/gunicorn-ftv.sock
LOGDIR=${DJANGODIR}/logs/gunicorn.log
USER=kevinits
GROUP=kevinits
NUM_WORKERS=5
DJANGO_SETTINGS_MODULE=config.production
DJANGO_WSGI_MODULE=config.wsgi

rm -frv $SOCKFILE
echo "Iniciando la aplicación $NAME con el usuario `whoami`"

exec ${DJANGODIR}/env/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=$LOGDIR
