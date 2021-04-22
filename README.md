# PnTest

An HTTP (and Websockets) proxy for performing penetration tests against web applications, with advanced capabilities for handling single-page-applications. This repo contains the frontend GUI application based on Python 3.9 and PySide2.

![](./screenshot.png)

## Key Features

- Detects which browsers you have installed and launches it pre-configured for PnTest to intercept HTTPS requests
- Open multiple instances of the same browser in isolated-environments so you can keep multiple sessions active at the same time
- Uses the browser's API to grab the rendered HTML allowing you to view what you actually see in the browser
- Crawl SPAs (i.e. React sites) as well as traditional web applications
- Intercept and modify requests and responses

## Install
```bash
$ git clone git@github.com:evanrolfe/pntest.git
$ cd pntest
$ virtualenv -p /usr/bin/python3.9 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Develop
Run the app in developer mode:
```bash
$ bin/dev
```

Compile Qt assets to python with:
```bash
$ bin/compile_assets
```

Compile Qt UI files to python with:
```bash
$ bin/compile_views
```

Run the linter with `flake8`.

## Test
Run the test suite with:
```
$ bin/test
```

## Build
First build the proxy, copy it to include, then build the final binary:
```
$ bin/build_proxy
$ mv dist/pntest_proxy include/pntest_proxy
$ bin/build
```
Which outputs a binary to `dist/pntest/`.

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
