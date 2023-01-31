#!/bin/bash
echo "Docker proxy config:"
echo "CLIENT_ID=$CLIENT_ID"
echo "ZMQ_SERVER=$ZMQ_SERVER"

# Dont apply iptables rules to mitmproxyuser
iptables -t nat -A OUTPUT -m owner ! --uid-owner mitmproxyuser -p tcp --dport 80 -j REDIRECT --to-port 8080
iptables -t nat -A OUTPUT -m owner ! --uid-owner mitmproxyuser -p tcp --dport 443 -j REDIRECT --to-port 8080

# Prevent an infinite loop by running mitmproxy as the mitmprpoxyuser whos traffic is not redirected by
# while true; do sleep 1000; done
su mitmproxyuser -c "mitmdump -s /app/mitmproxy/addon.py -p 8080 --mode transparent --showhost - --client-id $CLIENT_ID --zmq-server $ZMQ_SERVER"
