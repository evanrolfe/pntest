# import rpyc
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

# If the src/__main__.py process has stopped, then the proxy should kill itself
def start_polling(socket):
    while True:
        try:
            socket.send_string(json.dumps({'type': 'poll'}))
            time.sleep(1)
        except zmq.error.Again as ex:
            print(ex)
            print('[Proxy] closing process...')
            os.kill(os.getpid(), signal.SIGTERM)

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

# 3. Listen to messages from the Router
while True:
    message_raw = socket.recv()
    message = json.loads(message_raw)
    print(f'Received message: {message["type"]}')

    if message['type'] in ['forward', 'forward_and_intercept']:
        proxy_events.forward_flow(message)
    elif message['type'] == 'drop':
        proxy_events.drop_flow(message)
    elif message['type'] == 'forward_all':
        proxy_events.forward_all()

# 3. Poll the ZMQ server regularly to ensure the program hasn't stopped running
# poll_socket = context.socket(zmq.REQ)
# poll_socket.RCVTIMEO = 1000
# poll_socket.connect("tcp://localhost:%s" % PROXY_ZMQ_PORT)
# start_polling(poll_socket)

proxy_thread.join()
