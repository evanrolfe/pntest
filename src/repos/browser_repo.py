from __future__ import annotations
from entities.browser import Browser
from entities.client import Client
from lib.browser_launcher.launch_browser import launch_chrome_or_chromium, launch_firefox
from PyQt6 import QtCore

# TODO: This should be imported from teh file that defines the zmq server
ZMQ_SERVER_ADDR = "localhost:5556"

class BrowserRepo(QtCore.QObject):
    browsers: list[Browser]
    app_path: str
    thread_pool: QtCore.QThreadPool

    browser_exited = QtCore.pyqtSignal(object)

    # Singleton method stuff:
    __instance = None

    @staticmethod
    def get_instance() -> BrowserRepo:
        # Static access method.
        if BrowserRepo.__instance is None:
            BrowserRepo("")

        return BrowserRepo.__instance # type:ignore

    def __init__(self, app_path: str):
        super().__init__()

        self.procs = []
        self.app_path = app_path
        self.thread_pool = QtCore.QThreadPool()

        # Virtually private constructor.
        if BrowserRepo.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            BrowserRepo.__instance = self
    # /Singleton method stuff

    def launch_browser(self, client: Client, browser_command: str) -> Browser:
        if client.type in ['chrome', 'chromium']:
            browser = Browser(lambda: launch_chrome_or_chromium(client, browser_command))
        elif client.type == 'firefox':
            browser = Browser(lambda: launch_firefox(client, browser_command))
        else:
            raise Exception("client is not a browser")

        browser.signals.exited.connect(self.browser_exited)
        self.thread_pool.start(browser)

        return browser

    def close_browser(self, browser: Browser):
        browser.kill()
