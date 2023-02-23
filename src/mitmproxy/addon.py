"""
Basic skeleton of a mitmproxy addon.

Run as follows: mitmproxy -s anatomy.py
"""
import os
import pathlib
import signal
import zmq
from typing import Any, cast, Optional
import simplejson as json
from pathlib import Path
import time
import threading
from mitmproxy.http import Headers, Response as MitmResponse, HTTPFlow as MitmHTTPFlow
from common_types import ProxyRequest, ProxyResponse, ProxyWebsocketMessage
from home_page_html import HOME_PAGE_HTML
from sys import argv
from argparse import ArgumentParser

TIMEOUT_AFTER_SECONDS_NO_POLL = 3

# Example of argv:
#
# [
#   '/Users/evan/Code/pntest/venv/bin/mitmdump',
#   '-s',
#   '/Users/evan/Code/pntest/src/mitmproxy/addon.py',
#   '-p',
#   '8080',
#   '--set',
#   'confdir=./include',
#   '--set',
#   'client_certs=./include/mitmproxy-client.pem',
# ]

arg_parser = ArgumentParser()
arg_parser.add_argument('-p', '--port')
arg_parser.add_argument('--client-id')
arg_parser.add_argument('--zmq-server')
args, _ = arg_parser.parse_known_args(argv)

class ProxyHttpFlow(MitmHTTPFlow):
    intercept_response: bool

class ProxyEventsAddon:
    settings: Optional[dict[str,Any]]
    client_id: int
    recording_enabled: bool
    intercept_enabled: bool
    intercepted_flows: list[ProxyHttpFlow]
    socket: zmq.Socket

    def __init__(self, client_id: int):
        current_path = pathlib.Path(__file__).parent.resolve()

        self.client_id = client_id
        self.intercepted_flows = []
        self.settings = None
        self.intercept_enabled = False
        self.recording_enabled = True

    def zmq_connect(self):
        print("[ZMQClient] starting...")

        # Connect to the ZMQ server
        context = zmq.Context()
        self.socket = context.socket(zmq.DEALER)
        self.socket.setsockopt_string(zmq.IDENTITY, str(self.client_id))
        self.socket.connect("tcp://%s" % args.zmq_server)

        # Let em know we've started
        self.socket.send_string(json.dumps({'type': 'started'}))

        # Listen to messages from the server
        listen_thread = threading.Thread(target=self.zmq_listen, daemon=True)
        listen_thread.start()

        print("[ZMQClient] listening...")

    def zmq_listen(self):
        poll = zmq.Poller()
        poll.register(self.socket, zmq.POLLIN)
        last_poll_at = int(time.time())

        while True:
            sockets = dict(poll.poll(1000))

            diff = int(time.time()) - last_poll_at
            # If the src/__main__.py process has stopped, then the proxy should kill itself
            if diff >= TIMEOUT_AFTER_SECONDS_NO_POLL:
                print(f'[Proxy] last poll was {diff} secs ago! Shutting down..')
                os.kill(os.getpid(), signal.SIGTERM)

            if sockets:
                message_raw = self.socket.recv()

                # ZMQ typing is not accurate here
                if type(message_raw) is not bytes:
                    raise Exception(f'[Proxy] Could not parse message of type {type(message_raw)}')

                message_raw_str = message_raw.decode('utf-8')
                message = json.loads(message_raw)

                if message['type'] in ['forward', 'forward_and_intercept']:
                    self.forward_flow(message)

                elif message['type'] == 'drop':
                    self.drop_flow(message)

                elif message['type'] == 'forward_all':
                    self.forward_all()

                elif message['type'] == 'enable_intercept':
                    self.set_intercept_enabled(message['value'])

                elif message['type'] == 'enable_recording':
                    self.set_recording_enabled(message['value'])

                elif message['type'] == 'set_settings':
                    self.set_settings(message['value'])

                elif message['type'] == 'poll':
                    last_poll_at = int(time.time())

    # ---------------------------------------------------------------------------
    # Actions:
    # ---------------------------------------------------------------------------
    def forward_flow(self, message):
        type = message['type']
        modified_flow = message['flow']

        print(f'[Proxy] {type} flow {modified_flow["uuid"]}')
        flow = self.intercepted_flows.pop(0)

        # Overwrite the MitmProxy flow with the values of the Pntest Flow:
        if flow.websocket:
            flow.websocket.messages[-1].content = modified_flow['websocket_messages'][-1]['content'].encode()

        elif flow.response:
            flow.response.status_code = modified_flow['response']['status_code']
            flow.response.headers = self.__convert_headers_for_mitm(modified_flow['response']['headers'])
            flow.response.content = modified_flow['response']['content'].encode()

        else:
            flow.request.path = modified_flow['request']['path']
            flow.request.method = modified_flow['request']['method']
            flow.request.host = modified_flow['request']['host']
            flow.request.port = modified_flow['request']['port']
            flow.request.headers = self.__convert_headers_for_mitm(modified_flow['request']['headers'])
            flow.request.content = modified_flow['request']['content'].encode()
            flow.intercept_response = (message['type'] == 'forward_and_intercept')

        flow.resume()

    def forward_all(self):
        for flow in self.intercepted_flows:
            print(f'[Proxy] forwarding flow {flow.id}')
            flow.intercept_response = False
            flow.resume()

    def drop_flow(self, message):
        type = message['type']
        modified_flow = message['flow']

        print(f'[Proxy] {type} flow {modified_flow["uuid"]}')
        flow = self.intercepted_flows.pop(0)
        flow.kill()

    def intercept_flow(self, flow):
        flow.intercept()
        self.intercepted_flows.append(flow)

    def set_intercept_enabled(self, enabled: bool):
        self.intercept_enabled = enabled

    def set_recording_enabled(self, enabled: bool):
        self.recording_enabled = enabled

    def set_settings(self, settings):
        self.settings = settings

    # ---------------------------------------------------------------------------
    # MitmProxy Events:
    # ---------------------------------------------------------------------------
    def request(self, flow: MitmHTTPFlow):
        print('[Proxy] HTTP request')
        # The default homepage at http://pntest
        if flow.request.host == 'pntest':
            flow.response = MitmResponse.make(200, self.__proxy_home_page_html(), {"content-type": "text/html"})

        if not self.should_request_be_captured(flow):
            return

        request_state = cast(ProxyRequest, convert_dict_bytes_to_strings(flow.request.get_state()))
        request_state['flow_uuid'] = flow.id
        request_state['type'] = 'request'
        request_state['client_id'] = self.client_id
        request_state['intercepted'] = self.__should_intercept_request(flow)
        request_state['content'] = flow.request.text or ''
        # NOTE: WE have to re-write this when in docker_proxy because iptables intercepts this after the host
        # has been replaced with an ip address
        if flow.request.host_header:
            request_state['host'] = flow.request.host_header
        self.__send_message(request_state)

        if request_state['intercepted']:
            self.intercept_flow(flow)

    def response(self, flow: MitmHTTPFlow):
        print('[Proxy] HTTP response')
        intercept_response = getattr(flow, 'intercept_response', False)

        if flow is None:
            return

        if flow.response is None or not self.should_request_be_captured(flow):
            return

        response_state = cast(ProxyResponse, convert_dict_bytes_to_strings(flow.response.get_state()))
        response_state['flow_uuid'] = flow.id
        response_state['type'] = 'response'
        response_state['intercepted'] = intercept_response

        # NOTE: Even though it breaks the type-checking, we convert this to a string so it can be sent
        # over zmq, then in ProxyZmqServer we decode base64 and decode back to raw bytes
        # TODO: Have a seperate ProxyResponseZmq type with content: str
        if flow.response.content is None:
            response_state['content'] = '' # type:ignore
        else:
            response_state['content'] = flow.response.content.hex() # type:ignore

        self.__send_message(response_state)

        if intercept_response:
            self.intercept_flow(flow)

    def websocket_message(self, flow: MitmHTTPFlow):
        print('[Proxy] websocket message')
        if flow.websocket is None or self.recording_enabled == False:
            return

        message = flow.websocket.messages[-1]
        direction = 'outgoing' if message.from_client else 'incoming'

        message_state: ProxyWebsocketMessage = {
            'type': 'websocket_message',
            'flow_uuid': flow.id,
            'direction': direction,
            'content': message.content.decode(),
            'intercepted': self.__should_intercept_request(flow)
        }
        self.__send_message(message_state)

        if message_state['intercepted']:
            flow.intercepted_message = message  # type: ignore
            self.intercept_flow(flow)

    # ---------------------------------------------------------------------------
    # Private methods:
    # ---------------------------------------------------------------------------
    def __should_intercept_request(self, flow):
        return self.intercept_enabled

    def __convert_headers_for_mitm(self, headers):
        headers_obj = json.loads(headers)
        headers_list = []

        for key, value in headers_obj.items():
            header = (key.encode(), value.encode())
            headers_list.append(header)

        return Headers(headers_list)

    def __send_message(self, message):
        try:
            self.socket.send_string(json.dumps(message))
        except UnicodeDecodeError:
            print(f'ERROR => Could not send message for flow {message["flow_uuid"]}')
            return

    def should_request_be_captured(self, flow: MitmHTTPFlow) -> bool:
        if self.recording_enabled == False:
            return False

        if self.settings is None:
            return True

        # Check host
        host_list = self.settings['capture_filters']['host_list']
        has_hosts = len(host_list) > 0
        host_setting = self.settings['capture_filters']['host_setting']

        if flow.request.host in host_list and host_setting == 'exclude' and has_hosts:
            return False

        if flow.request.host not in host_list and host_setting == 'include' and has_hosts:
            return False

        return True

    def __proxy_home_page_html(self) -> str:
        html = HOME_PAGE_HTML

        html = html.replace('{{client_id}}', str(self.client_id))
        html = html.replace('{{proxy_port}}', args.port)
        return html

def convert_dict_bytes_to_strings(d):
    new_d = {}
    for key, value in d.items():
        if type(value) is bytes and key != 'content':
            new_d[key] = value.decode()
        elif key == 'headers':
            new_d[key] = convert_headers_bytes_to_strings(value)
        else:
            new_d[key] = value

    return new_d

def convert_headers_bytes_to_strings(headers):
    new_headers = []
    for header in headers:
        new_header = (header[0].decode(), header[1].decode())
        new_headers.append(new_header)

    return new_headers

proxy_events = ProxyEventsAddon(int(args.client_id))
proxy_events.zmq_connect()

addons = [proxy_events]
