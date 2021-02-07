# PnTest

An HTTP (and Websockets) proxy for performing penetration tests against web applications, with advanced capabilities for handling single-page-applications. This repo contains the frontend GUI application based on python3.6 and PySide2.

![](./screenshot.png)

## Key Features

- Detects which browsers you have installed and launches it pre-configured for PnTest to intercept HTTPS requests
- Open multiple instances of the same browser in isolated-environments so you can keep multiple sessions active at the same time
- Uses the browser's API to grab the rendered HTML allowing you to view what you actually see in the browser
- Crawl SPAs (i.e. React sites) as well as traditional web applications
- Intercept and modify requests and responses

## Install
Clone pntest and pntest-core, then build the `pntest-core` and `node_sqlite3.node` binaries and copy them to `pntest/include`:
```bash
$ git clone git@github.com:evanrolfe/pntest.git
$ git clone git@github.com:evanrolfe/pntest-core.git
$ cd pntest-core
$ npm install
$ ./scripts/build.sh
$ cp dist/pntest-core ../pntest/include/pntest-core
$ cp dist/node_sqlite3.node ../pntest/include/node_sqlite3.node
```

Setup pntest virtual environment:
```bash
$ cd pntest
$ virtualenv -p /usr/bin/python3.6 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Develop
Run the app:
```bash
$ python src
```

Compile Qt assets to python with:
```bash
$ ./scripts/compile_assets.sh
```

Compile Qt UI files to python with:
```bash
$ ./scripts/compile_views.sh
```

Run the linter with `flake8`.

## Test

Todo.

## Build
```
$ ./scripts/build.sh
```
Which outputs a binary to `dist/pntest`.

## Notes
Pip packages used:
- orator
- PySide2
- requests

Icons come from:
https://icons8.com/icon/set/console/dusk
https://www.flaticon.com/search?word=terminal
