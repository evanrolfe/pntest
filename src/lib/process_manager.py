import subprocess
import signal
import atexit
import os
import sys

CHROMIUM_COMMAND = 'chromium-browser --no-sandbox --noerrdialogs --user-data-dir=/home/evan/Code/pntest/include/chromium-profile' # noqa
PROXY_COMMAND = f'{sys.executable} /home/evan/Code/pntest/src/proxy'

class ProcessManager:
    def __init__(self):
        self.processes = []

        atexit.register(self.on_exit)
        signal.signal(signal.SIGTERM, self.on_exit)
        signal.signal(signal.SIGINT, self.on_exit)

    def on_exit(self):
        print("ProcessManager closing all processes...")
        for process in self.processes:
            os.kill(process.pid, signal.SIGTERM)

    def launch_browser(self):
        process = subprocess.Popen(
            CHROMIUM_COMMAND.split(' '),
            preexec_fn=os.setsid
        )
        self.processes.append(process)

    def launch_proxy(self, listen_port):
        process = subprocess.Popen(
            PROXY_COMMAND.split(' '),
            preexec_fn=os.setsid
        )
        self.processes.append(process)
