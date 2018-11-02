FROM python:3.6.6-alpine3.8

EXPOSE 3032

RUN apk add --no-cache --virtual .build-deps \
    linux-headers \
    build-base

RUN apk add --no-cache redis pcre-dev libressl-dev

RUN mkdir -p /app

ADD requirements.txt /app

RUN pip install -r /app/requirements.txt \
    && apk del .build-deps

CMD [ "uwsgi", "--http-socket", "0.0.0.0:3032", \
               "--chdir", "/var/www/amoki-music", \
               "--wsgi-file", "/var/www/amoki-music/amoki_music/wsgi_websocket.py", \
               "--gevent", "1000", \
               "--http-websockets"]
