# Creates a docker image for the docker proxy node
FROM python:3.11-alpine3.17

WORKDIR /app
ADD ./docker_proxy /app

ENV CLIENT_ID=1
ENV ZMQ_SERVER=host.docker.internal:5556

RUN apk update && apk add iptables curl ca-certificates gcc libffi-dev python3-dev musl-dev openssl-dev g++  \
  libxml2-dev libxslt-dev libjpeg-turbo-dev zlib-dev tshark musl-dev rust cargo bash

ADD ./src/mitmproxy /app/mitmproxy
# VOLUME ["/app/mitmproxy"]
RUN pip install --upgrade pip

RUN pip install -r /app/requirements.txt

RUN adduser -D mitmproxyuser
ENTRYPOINT /bin/bash run.sh
