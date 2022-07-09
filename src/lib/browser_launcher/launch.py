import subprocess
import os
from pathlib import Path
import shutil

from lib.paths import get_app_config_path, get_include_path
from lib.cert_utils import generate_hpkp_from_pem_certificate

DEFAULT_CHROME_OPTIONS = [
    '--enable-pinch',
    '--disable-sync',
    '--no-default-browser-check',
    '--disable-restore-session-state',
    '--disable-web-security',
    '--disable-features=IsolateOrigins,site-per-process',
    '--disable-site-isolation-trials',
    '-test-type',
    '--no-sandbox',
    '--no-default-browser-check',
    '--disable-popup-blocking',
    '--disable-translate',
    '--disable-default-apps',
    '--disable-sync',
    '--enable-fixed-layout',
    '--no-first-run',
    '--disable-setuid-sandbox',
    '--noerrdialogs http://pntest'
]

def launch_chrome_or_chromium(client, browser_command: str) -> subprocess.Popen:
    options = get_options_chrome_or_chromium(client)
    process = subprocess.Popen(
        [browser_command] + options + ['http://pntest'],
        preexec_fn=os.setsid
    )
    return process

def launch_firefox(client, browser_command: str) -> subprocess.Popen:
    options = get_options_firefox(client, browser_command)

    process = subprocess.Popen(
        browser_command.split(' ') + options,
        preexec_fn=os.setsid
    )
    return process

def get_options_chrome_or_chromium(client):
    ca_pem = Path(f'{get_include_path()}/mitmproxy-ca.pem').read_text()
    spki = generate_hpkp_from_pem_certificate(ca_pem)

    print(f"[BrowserLauncher] include_path: {get_include_path()}")
    print(f"[BrowserLauncher] spki: {spki}")

    proxy_options = [
        f'--proxy-server=127.0.0.1:{client.proxy_port}',
        '--proxy-bypass-list=<-loopback>',
        f'--ignore-certificate-errors-spki-list={spki}'
    ]

    user_data_dir_options = [
        f'--user-data-dir={get_app_config_path()}/{client.type}-profile'
    ]

    return DEFAULT_CHROME_OPTIONS + proxy_options + user_data_dir_options

def get_options_firefox(client, browser_command):
    profile_path = f'{get_app_config_path()}/{client.type}-profile-{client.proxy_port}'
    profile_name = f'pntest-{client.proxy_port}'

    if not os.path.isdir(profile_path):
        print(f'[BrowserLauncher] creating firefox profile in {profile_path}')
        subprocess.run([browser_command, '-CreateProfile', f'{profile_name} {profile_path}'])
        configure_firefox_profile(client, profile_path)

    return ['-P', profile_name]

def configure_firefox_profile(client, profile_path):
    proxy_host = '"127.0.0.1"'

    prefs = [
        '"network.proxy.http", ' + proxy_host,
        '"network.proxy.http_port", ' + str(client.proxy_port),
        '"network.proxy.ssl", ' + proxy_host,
        '"network.proxy.ssl_port", ' + str(client.proxy_port),
        '"network.proxy.type", 1',
        '"browser.cache.disk.capacity", 0',
        '"browser.cache.disk.smart_size.enabled", false',
        '"browser.cache.disk.smart_size.first_run", false',
        '"browser.sessionstore.resume_from_crash", false',
        '"browser.startup.page", 0',
        '"browser.shell.checkDefaultBrowser", false',
        '"network.proxy.allow_hijacking_localhost", true',
        '"browser.startup.page", 1',
        '"browser.startup.homepage", "http://pntest"'
    ]

    prefs_str = ''.join([f'user_pref({pref});\n' for pref in prefs])
    pref_file = os.path.join(profile_path, 'user.js')

    with open(pref_file, 'a+') as file:
        file.write(prefs_str)

    cert9_file = f'{get_include_path()}/cert9.db'
    shutil.copyfile(cert9_file, f'{profile_path}/cert9.db')
