# Creates a docker image for the docker proxy node
# We opted for the python slim base image instead of alpine, because alpine does not support
# python wheels and so all packages need to be built from source which results in a much bigger image.
FROM python:3.11-slim

WORKDIR /app
ADD ./docker_proxy /app

ENV CLIENT_ID=1
ENV ZMQ_SERVER=host.docker.internal:5556

RUN apt-get update
RUN apt-get upgrade -qy
RUN apt-get install iptables curl -qy

ADD ./src/mitmproxy /app/mitmproxy
# # VOLUME ["/app/mitmproxy"]
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

RUN useradd --create-home mitmproxyuser
ENTRYPOINT /bin/bash run.sh
