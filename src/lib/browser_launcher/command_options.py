from pathlib import Path
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
    '--noerrdialogs https://pntest'
]

def get_options_chrome_or_chromium(client):
    ca_pem = Path(f'{get_include_path()}/mitmproxy-ca.pem').read_text()
    spki = generate_hpkp_from_pem_certificate(ca_pem)

    print(f"[BrowserLauncher] include_path: {get_include_path()}")
    print(f"[BrowserLauncher] spki: {spki}")

    proxy_options = [
        f'--proxy-server=127.0.0.1:{client.proxy_port}',
        '--proxy-bypass-list="<-loopback>"',
        f'--ignore-certificate-errors-spki-list={spki}',

    ]

    user_data_dir_options = [
        f'--user-data-dir={get_app_config_path()}/{client.type}-profile'
    ]

    return DEFAULT_CHROME_OPTIONS + proxy_options + user_data_dir_options

def get_options_firefox(client):
    profile_options = [
        f'--profile {get_app_config_path()}/{client.type}-profile'
    ]

    return profile_options
