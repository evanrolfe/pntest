import asyncio
import os
import signal
from sys import argv
import zmq.asyncio
import threading
import simplejson as json
import time

from proxy import Proxy
from proxy_events import ProxyEvents

PROXY_ZMQ_PORT = 5556
TIMEOUT_AFTER_SECONDS_NO_POLL = 3

port_num = int(argv[1])
client_id = int(argv[2])
print(f'Proxy server starting, port {port_num}, client_id {client_id}..')

# 1. Start mitmproxy
proxy_events = ProxyEvents(client_id)
proxy = Proxy(proxy_events, port_num)
loop = asyncio.get_event_loop()
proxy_thread = threading.Thread(target=proxy.run_in_thread, args=(loop, proxy.master))
proxy_thread.start()

# 2. Connect to the main process via ZMQ
print('connecting ZMQ Server...')
queue = asyncio.Queue()
context = zmq.Context()
socket = context.socket(zmq.DEALER)
socket.setsockopt_string(zmq.IDENTITY, str(client_id))
socket.connect("tcp://localhost:%s" % PROXY_ZMQ_PORT)
proxy_events.set_socket(socket)

socket.send_string(json.dumps({'type': 'connected'}))

# 3. Listen to messages from the Router
last_poll_at = int(time.time())

poll = zmq.Poller()
poll.register(socket, zmq.POLLIN)

while True:
    sockets = dict(poll.poll(1000))

    diff = int(time.time()) - last_poll_at
    # If the src/__main__.py process has stopped, then the proxy should kill itself
    if diff >= TIMEOUT_AFTER_SECONDS_NO_POLL:
        print(f'[Proxy] last poll was {diff} secs ago! Shutting down..')
        os.kill(os.getpid(), signal.SIGTERM)

    if sockets:
        message_raw = socket.recv()
        message = json.loads(message_raw)

        if message['type'] in ['forward', 'forward_and_intercept']:
            proxy_events.forward_flow(message)
        elif message['type'] == 'drop':
            proxy_events.drop_flow(message)
        elif message['type'] == 'forward_all':
            proxy_events.forward_all()
        elif message['type'] == 'enable_intercept':
            proxy_events.set_intercept_enabled(message['value'])
        elif message['type'] == 'poll':
            # print(f'Received poll at {datetime.datetime.now().time()}')
            last_poll_at = int(time.time())


proxy_thread.join()
