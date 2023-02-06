#!/bin/bash
echo "Docker proxy config:"
echo "CLIENT_ID=$CLIENT_ID"
echo "ZMQ_SERVER=$ZMQ_SERVER"

sysctl -w net.ipv4.ip_forward=1
sysctl -w net.ipv6.conf.all.forwarding=1
sysctl -w net.ipv4.conf.all.send_redirects=0

# Route all outgoing traffic to mitmproxy on port 8080, but dont apply iptables rules to mitmproxyuser
iptables -t nat -A OUTPUT -m owner ! --uid-owner mitmproxyuser -p tcp --dport 1:65535 -j REDIRECT --to-port 8080

# Prevent an infinite loop by running mitmproxy as the mitmprpoxyuser whos traffic is not redirected by
su mitmproxyuser -c "mitmdump -s /app/mitmproxy/addon.py -p 8080 --mode transparent --showhost - --client-id $CLIENT_ID --zmq-server $ZMQ_SERVER"
# while true; do sleep 1000; done
