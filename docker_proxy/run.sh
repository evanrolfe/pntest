#!/bin/bash
echo "Docker proxy config:"
echo "CLIENT_ID=$CLIENT_ID"
echo "ZMQ_SERVER=$ZMQ_SERVER"
echo "PROXY_PORT=$PROXY_PORT"

# Route all outgoing traffic to mitmproxy on port $PROXY_PORT, but dont apply iptables rules to mitmproxyuser
iptables -t nat -A OUTPUT -m owner ! --uid-owner mitmproxyuser -p tcp --dport 1:65535 -j REDIRECT --to-port $PROXY_PORT

# Prevent an infinite loop by running mitmproxy as the mitmprpoxyuser whos traffic is not redirected by
# while true; do sleep 1000; done
su mitmproxyuser -c "mitmdump -s /app/mitmproxy/addon.py -p $PROXY_PORT --mode transparent --showhost - --client-id $CLIENT_ID --zmq-server $ZMQ_SERVER"
