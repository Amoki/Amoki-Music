FROM python:3.6-alpine

RUN apk add --no-cache --virtual .build-deps \
    linux-headers \
    build-base

RUN apk add --no-cache redis pcre-dev libressl-dev

RUN mkdir -p /app

ADD requirements.txt /app

RUN pip install -r /app/requirements.txt \
    && apk del .build-deps
