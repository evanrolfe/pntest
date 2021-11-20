import subprocess
import re
import platform

BROWSERS = [
    {
        'name': 'chrome',
        'command': 'google-chrome',
        'regex': r'Google Chrome (.+)',
        'type': 'chrome',
    },
    {
        'name': 'chromium',
        'command': 'chromium',
        'regex': r'Chromium ([0-9,\.]+) (.+)',
        'type': 'chrome',
    },
    {
        'command': 'firefox',
        'name': 'firefox',
        'regex': r'Mozilla Firefox (.+)',
        'type': 'firefox',
    },
]

def check_which(browser):
    try:
        result = subprocess.run([browser['command'], '--version'], stdout=subprocess.PIPE)
    except FileNotFoundError:
        return None

    output = result.stdout.decode().strip()
    matches = re.match(browser['regex'], output)

    if matches:
        browser['version'] = matches[1]

    return browser

def check(browser):
    pltfrm = platform.system()

    if pltfrm == "Windows":
        print("Your system is Windows")
    elif pltfrm == "Darwin":
        print("Your system is Mac")
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
