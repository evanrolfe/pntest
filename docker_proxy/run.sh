#!/bin/bash
echo "Docker proxy config:"
echo "CLIENT_ID=$CLIENT_ID"
echo "ZMQ_SERVER=$ZMQ_SERVER"
echo "WEB_UI_PORT=$WEB_UI_PORT"
echo "WEB_UI_PORT_DNS=$WEB_UI_PORT_DNS"
echo "PROXY_PORT=$PROXY_PORT"
echo "PROXY_PORT_DNS=$PROXY_PORT_DNS"

# Route all outgoing traffic to mitmproxy on port $PROXY_PORT, but dont apply iptables rules to mitmproxyuser
iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 1:65535 -j REDIRECT --to-port $PROXY_PORT
iptables -t nat -A PREROUTING -i eth0 -p udp --dport 53 -j REDIRECT --to-port $PROXY_PORT_DNS
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

# while true; do sleep 1000; done
mitmdump -s /app/mitmproxy/addon.py -p $PROXY_PORT --mode transparent - --client-id $CLIENT_ID --zmq-server $ZMQ_SERVER &
mitmweb --web-port $WEB_UI_PORT_DNS --web-host 0.0.0.0 --mode dns@$PROXY_PORT_DNS &
wait
