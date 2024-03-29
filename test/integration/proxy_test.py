# import signal
# import time
# import requests
# from requests.adapters import HTTPAdapter
# import pytest
# import pytestqt
# from pytestqt.qtbot import QtBot
# from pytest_httpserver import HTTPServer
# import os
# import asyncio
# import websockets
# import websocket
# from PyQt6 import QtCore
# from lib.browser_launcher.detect import Browser

# from lib.paths import get_app_path
# from lib.process_manager import ProxyMessageReceiver
# from proxy.common_types import SettingsJson
# from ui.widgets.main_window import MainWindow
# from models.client import Client
# from models.http_flow import HttpFlow
# from repos.client_repo import ClientRepo


# async def ws_handler(websocket, path):
#     data = await websocket.recv()
#     reply = f"Data recieved as:  {data}!"
#     print(reply)
#     await websocket.send(reply)

# @pytest.fixture(scope="class")
# def proxy(request):
#     print("Starting proxy for testing..")

#     # Determine paths
#     app_path = get_app_path()
#     src_path = os.path.join(app_path, 'src')
#     request.cls.process_manager = ProxyMessageReceiver(src_path)

#     # Launch a proxy
#     request.cls.client = Client(
#         title = 'test',
#         type = 'anything',
#         proxy_port = 8010,
#     )
#     ClientRepo().save(request.cls.client)

#     settings: SettingsJson = {
#         "display_filters": {
#             "host_list": [],
#             "host_setting": "",
#             "path_list": [],
#             "path_setting": "",
#         },
#         "capture_filters": {
#             "host_list": ["localhost"],
#             "host_setting": "include",
#             "path_list": [],
#             "path_setting": "",
#         },
#         "proxy": {"ports_available": [8000]},
#     }
#     client_info: Browser = {
#         'name': 'anything',
#         'commands': [],
#         'regex': r'',
#         'type': 'anything',
#         'command': None,
#         'version': None
#     }
#     request.cls.process_manager.launch_client(request.cls.client, client_info, settings) # type:ignore

#     # TODO: Make this wait for proxy_started signal instead of using time.sleep, the only issue is that
#     # I dont know how this fixture will be able to access qtbot.
#     # This time.sleep is not long enough for this to work on CircleCI, which is why this whole test
#     # is commented out. If this can wait for a signal then we can enable this test on circleCI again.
#     time.sleep(2)
#     # # Make the HTTP request, while waiting for the signals to be verified
#     # with qtbot.waitSignal(request.cls.process_manager.proxy_started, timeout=2000):
#     #     pass

#     yield

#     # Shut down the proxy
#     print("Finished testing proxy, closing proxy..")
#     request.cls.process_manager.close_proxy(request.cls.client) # type:ignore
#     request.cls.process_manager.on_exit()

# @pytest.mark.usefixtures("proxy")
# class TestProxy:
#     process_manager: ProxyMessageReceiver
#     client: Client

#     flow_signals: list[HttpFlow]

#     def capture_flow_signal(self, flow: HttpFlow):
#         self.flow_signals.append(flow)
#         return True

#     def test_proxy_request_response(self, database, qtbot: QtBot, httpserver: HTTPServer):
#         # Setup mock server to make a request to
#         httpserver.expect_request("/proxy_test").respond_with_data("helloworld")

#         # Prepare an HTTP request through the proxy
#         print("---------------------> Requesting via port ", self.client.proxy_port)
#         proxies = {
#             'http': f'http://localhost:{self.client.proxy_port}',
#             'https': f'http://localhost:{self.client.proxy_port}',
#         }
#         http_session = requests.Session()
#         # http_session.mount('http://localhost', HTTPAdapter(max_retries=0))
#         # http_session.mount('https://localhost', HTTPAdapter(max_retries=0))

#         request = requests.Request('GET', httpserver.url_for('/proxy_test'))
#         prepped_request = http_session.prepare_request(request)

#         # Verify both proxy_request and proxy_response signals were emitted by the proxy
#         signals = [self.process_manager.proxy_request, self.process_manager.proxy_response]
#         self.flow_signals = []
#         verifiers = [self.capture_flow_signal, self.capture_flow_signal]

#         # Make the HTTP request, while waiting for the signals to be verified
#         with qtbot.waitSignals(signals, timeout=2000, check_params_cbs=verifiers):
#             http_session.send(prepped_request, timeout=2, proxies=proxies)

#         assert len(self.flow_signals) == 2
#         assert self.flow_signals[0].request.get_url() == httpserver.url_for('/proxy_test')
#         assert self.flow_signals[1].response is not None
#         assert self.flow_signals[1].response.status_code == 200

# #     def test_proxy_request_response_with_capture_filters(self, database, qtbot: QtBot, httpserver: HTTPServer):
# #         # Setup mock server to make a request to
# #         httpserver.expect_request("/proxy_test2").respond_with_data("helloworld2")

# #         # Set capture filters
# #         settings: SettingsJson = {
# #             "display_filters": {
# #                 "host_list": [],
# #                 "host_setting": "",
# #                 "path_list": [],
# #                 "path_setting": "",
# #             },
# #             "capture_filters": {
# #                 "host_list": ["localhost"],
# #                 "host_setting": "include",
# #                 "path_list": [],
# #                 "path_setting": "",
# #             },
# #             "proxy": {"ports_available": [8000]},
# #         }
# #         self.process_manager.set_settings(settings)

# #         # Prepare an HTTP request through the proxy
# #         proxies = {
# #             'http': f'http://localhost:{self.client.proxy_port}',
# #             'https': f'http://localhost:{self.client.proxy_port}',
# #         }
# #         http_session = requests.Session()

# #         # Request 1
# #         request_localhost = requests.Request('GET', httpserver.url_for('/proxy_test2'))
# #         prepped_request_localhost = http_session.prepare_request(request_localhost)

# #         # Request 2
# #         request_google = requests.Request('GET', 'http://www.google.com')
# #         prepped_request_google = http_session.prepare_request(request_google)

# #         # Verify both flow_created and flow_updated signals were sent by the proxy
# #         signals = [self.process_manager.proxy_request, self.process_manager.proxy_response]

# #         # Verify request to localhost emits signals:
# #         self.flow_signals = []
# #         verifiers = [self.capture_flow_signal, self.capture_flow_signal]

# #         # Make the HTTP request, while waiting for the signals to be verified
# #         with qtbot.waitSignals(signals, timeout=2000, check_params_cbs=verifiers):
# #             http_session.send(prepped_request_localhost, timeout=5, proxies=proxies)

# #         assert len(self.flow_signals) == 2
# #         assert self.flow_signals[0].request.get_url() == httpserver.url_for('/proxy_test2')
# #         assert self.flow_signals[1].response is not None
# #         assert self.flow_signals[1].response.status_code == 200

# #         # Verify request to google.com does not emit signals:
# #         self.flow_signals = []
# #         verifiers = [self.capture_flow_signal, self.capture_flow_signal]

# #         # Make the HTTP request, while waiting for the signals to be verified
# #         try:
# #             with qtbot.waitSignals(signals, timeout=2000, check_params_cbs=verifiers):
# #                 http_session.send(prepped_request_google, timeout=5, proxies=proxies)
# #         except:
# #             # This will raise an pytestqt.exceptions.TimeoutError, which means no signals were emitted
# #             pass

# #         assert len(self.flow_signals) == 0

# #     # TODO:
# #     # def test_proxy_websocket(self, database, qtbot: QtBot):
# #     #     print("[Test] Starting websockets server...")
# #     #     start_server = websockets.serve(ws_handler, "localhost", 8000)  # type: ignore
# #     #     asyncio.get_event_loop().run_until_complete(start_server)
# #     #     print("[Test] websockets server started")

# #     #     ws = websocket.WebSocket()
# #     #     ws.connect(
# #     #         "ws://localhost:8000/",
# #     #         http_proxy_host="localhost",
# #     #         http_proxy_port="8010",
# #     #         proxy_type="http",
# #     #         http_no_proxy=["x"]
# #     #     )
# #     #     print("connected")
# #     #     ws.send("Hello, World")
# #     #     result =  ws.recv()
# #     #     print("Received '%s'" % result)
# #     #     ws.close()

# #     #     assert 1 == 1
