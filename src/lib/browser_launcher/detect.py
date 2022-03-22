import subprocess
import re
import platform
from copy import deepcopy

BROWSERS = [
    {
        'name': 'chrome',
        'commands': [
            'chrome',
            'google-chrome',
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        ],
        'regex': r'Google Chrome (.+)',
        'type': 'chrome',
    },
    {
        'name': 'chromium',
        'commands': ['chromium', 'chromium-browser'],
        'regex': r'Chromium ([0-9,\.]+) (.+)',
        'type': 'chrome',
    },
    {
        'name': 'firefox',
        'commands': [
            'firefox',
            '/Applications/Firefox.app/Contents/MacOS/firefox-bin'
        ],
        'regex': r'Mozilla Firefox (.+)',
        'type': 'firefox',
    },
]

def check_command(command):
    try:
        result = subprocess.run([command, '--version'], stdout=subprocess.PIPE)
        return result
    except FileNotFoundError:
        return None

def check_which(browser):
    browser_copy = deepcopy(browser)
    result = None

    for command in browser_copy['commands']:
        result = check_command(command)
        if result is not None:
            browser_copy['command'] = command
            break

    if result is None:
        return browser_copy

    output = result.stdout.decode().strip()
    matches = re.match(browser_copy['regex'], output)

    if matches:
        browser_copy['version'] = matches[1]

    del browser_copy['commands']
    return browser_copy

def check(browser):
    pltfrm = platform.system()

    if pltfrm == "Windows":
        print("Your system is Windows")
    elif pltfrm == "Darwin":
        print("Your system is Mac")
        return check_which(browser)
    else:
        print(f"Linux/Unidentified system {pltfrm}")
        return check_which(browser)

def detect_available_browsers():
    available_browsers = []

    for browser in BROWSERS:
        result = check(browser)

        if result:
            available_browsers.append(result)

    return available_browsers

print(detect_available_browsers())
