FROM python:3.6.6-alpine3.8

EXPOSE 3031

RUN apk add --no-cache --virtual .build-deps \
    linux-headers \
    build-base

RUN mkdir -p /app

ADD requirements.txt /app

RUN pip install -r /app/requirements.txt \
    && apk del .build-deps

CMD [ "uwsgi", "--socket", "0.0.0.0:3031", \
               "--chdir", "/var/www/amoki-music", \
               "--wsgi-file", "/var/www/amoki-music/amoki_music/wsgi_django.py", \
               "--buffer-size", "32768"]
