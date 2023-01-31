# Creates a docker image for the docker proxy node
FROM python:3.11
LABEL maintainer="Bruno Amaro Almeida | brunoamaro.com"

WORKDIR /app
ADD ./docker_proxy /app

ENV CLIENT_ID=1
ENV ZMQ_SERVER=host.docker.internal:5556

RUN apt-get update
RUN apt-get upgrade -qy
RUN apt-get install iptables curl python3-dev -qy

ADD ./src/mitmproxy /app/mitmproxy
# VOLUME ["/app/mitmproxy"]
RUN pip install -r /app/requirements.txt

RUN useradd --create-home mitmproxyuser
ENTRYPOINT /bin/bash run.sh
