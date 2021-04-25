import subprocess
import os
from lib.browser_launcher.command_options import get_options_chrome_or_chromium, get_options_firefox

def launch_chrome_or_chromium(client, browser_command):
    options = get_options_chrome_or_chromium(client)

    process = subprocess.Popen(
        browser_command.split(' ') + options,
        preexec_fn=os.setsid
    )
    return process

def launch_firefox(client, browser_command):
    options = get_options_firefox(client)

    process = subprocess.Popen(
        browser_command.split(' ') + options,
        preexec_fn=os.setsid
    )
    return process
