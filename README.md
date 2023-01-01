# PnTest

[![PnTest](https://circleci.com/gh/evanrolfe/pntest.svg?style=shield)](https://app.circleci.com/pipelines/github/evanrolfe/pntest) ![](https://img.shields.io/badge/python-3.11-blue) ![](https://img.shields.io/badge/Qt-6-blue)

An HTTP (and Websockets) proxy for performing penetration tests against web applications and APIs.

![](./screenshot.png)

## Key Features

- Detects which browsers you have installed and launches it pre-configured for PnTest to intercept HTTPS requests
- Open multiple instances of the same browser in isolated-environments so you can keep multiple sessions active at the same time
- Uses the browser's API to grab the rendered HTML allowing you to view what you actually see in the browser
- Crawl SPAs (i.e. React sites) as well as traditional web applications
- Intercept and modify requests and responses

## Install

(TODO)

## Develop

Setup your dev environment:

Linux:
```bash
$ git clone git@github.com:evanrolfe/pntest.git
$ cd pntest
$ virtualenv -p /usr/bin/python3.9 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ pip install -r dev-requirements.txt

```
Mac:
```bash
$ git clone git@github.com:evanrolfe/pntest.git
$ cd pntest
$ pip3.11 install virtualenv
$ python3.11 -m virtualenv -p /usr/local/bin/python3.11 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ pip install -r dev-requirements.txt
```

Always run `source venv/bin/activate` at the start to load the virtual env, then start the app in developer mode:
```bash
$ bin/dev
```

Compile Qt UI files to python with: (requires pyqt6rc which should be installed outside of the venv because of version conflicts)
```bash
$ bin/compile_views
```

Run the linter with `flake8`.

## Test
Run the tests with:
```
$ bin/test test/unit
$ bin/test test/integration
```

## Build
First build the proxy, copy it to include, then build the final binary:
```
$ bin/build
```
Which outputs a binary to `dist/pntest/`.

(Mac) run `bin/build_dmg`

## Notes
Icons come from:
https://icons8.com/icon/set/console/dusk
https://www.flaticon.com/search?word=terminal

To get `bin/build` to work you need to change `venv/lib/python3.9/site-packages/_pyinstaller_hooks_contrib/hooks/stdhooks/hook-pendulum.py` from:
```python
datas = collect_data_files("pendulum.locales", include_py_files=True)
hiddenimports = collect_submodules("pendulum.locales")

```
to this:
```python
datas = collect_data_files("pendulum", include_py_files=True)
hiddenimports = collect_submodules("pendulum")
```

## Generating certificate authority and importing to browsers:
**Create Certificate authority**

1. Generate the CA private key:
```
$ openssl genpkey -algorithm RSA -out include/rootKey.pem -pkeyopt rsa_keygen_bits:4096
```
2. Generate a cert and sign it with the root key
```
$ openssl req -new -key include/rootKey.pem -days 5480 -extensions v3_ca -batch -out include/rootCA.csr -utf8 -subj '/C=UK/O=pntest/OU=pntest'
$ openssl x509 -req -sha256 -days 3650 -in include/rootCA.csr -signkey include/rootKey.pem -extfile include/openssl.rootCA.cnf -out include/rootCA.pem
```
3. Create the necessary cert for [mitmproxy](https://docs.mitmproxy.org/stable/concepts-certificates/#using-a-custom-server-certificate) :
```
$ cat include/rootKey.pem include/rootCA.pem > include/mitmproxy-ca.pem
```

**Create a client cert to be used by mitmproxy**

Firefox does not allow you to use CA certs as the server cert, if you do it will give you an CA_CERT_USED_AS_END_ENTITY error. So we generate an end-entity cert which will be used by mitmproxy.
1. Create the client private key
```
$ openssl genrsa -out include/clientCert.key 2048
```
2. Generate a client cert and sign it with the client private key
```
$ openssl req -new -key include/clientCert.key -out include/clientCert.csr -subj '/C=UK/O=pntest/OU=pntest'
$ openssl x509 -req -in include/clientCert.csr -CA include/rootCA.pem -CAkey include/rootKey.pem -CAcreateserial -out include/clientCert.crt -days 500 -sha256 -extfile include/openssl.ss.cnf
```
3. Create the necessary cert for mitmproxy
```
$ cat include/clientCert.key include/clientCert.crt > include/mitmproxy-client.pem
```

**Import to browsers**

[Chrome/Chromium] No more action needed as chrome is started using the `--ignore-certificate-errors-spki-list` option.

[Firefox] Generate the cert9.db file with the certificate imported:

1. Start firefox from pntest, you'll get a cert error on https sites

2. Import the certiciate (settins -> certificates -> import -> select include/rootCA.pem -> Trust CA to identify web sites & Trust CA to identify email users)

3. Locate the cert9.db file in the firefox profile i.e. `~/Library/Preferences/pntest/firefox-profile-8080/cert9.db` (Mac) and copy it to `include/cert9.db`
