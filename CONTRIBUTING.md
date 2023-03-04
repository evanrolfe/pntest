# Contributing

## Setup Dev Environment

Requires Python 3.11.

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

Compile Qt UI files to python with:
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

## Build & Package (Mac .dmg)
1. Run `bin/build_mac` this outputs to `./dist/pntest.app`

2. Codesign with: `codesign --deep --force --verbose --options=runtime --sign "Evan Rolfe" ./dist/pntest.app/`

3. Package to dmg with: `bin/build_dmg`

4. Notarize the dmg: `xcrun notarytool submit ./dist/pntest.dmg --keychain-profile "PnTest" --wait`

5. Staple the dmg: `xcrun stapler staple ./dist/pntest.dmg`

## Build & Package (Linux .deb)
TODO

## Build & Package (Linux .rpm)
TODO

## Distribute the Docker Image
1. Build the image: `bin/build_docker`

2. Push the image to DockerHub: `bin/docker_push`

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

## Apple Developer ID Guide

**Code Sign**
Once you have the app built to `./dist/pntest.app`, you need to codesign that dir.

1. In Apple Developer Portal, create a "Developer ID Application" certificate with type Previous-Sub-CA. You'll need to follow the steps to export a CSR from keychain.

2. Download the certificate, double click it to import it to keychain (login). It should have trust set to system defaults.

3. Verify the certificate has been imported with `security find-identity -p basic -v`.

4. `security unlock-keychain login.keychain`

5. codesign --deep --force --verbose --options=runtime --sign "Evan Rolfe" ./dist/pntest.app/

(You may need to enter a password, and then click "Always Allow")

**Package**
Run `bin/build_dmg` which outputs to `./dist/pntest.dmg`.

**Notarize**

0. Install xcode and the command line tools

1. Create an application-specific password at https://appleid.apple.com/account/manage

2. Get the team id with `xcrun altool --list-providers -u '<email>' -p '<password>'`

3. Run: `xcrun notarytool store-credentials --apple-id '<email>' --password '<password>' --team-id '<teamid>'` and enter the name PnTest

4. Notarize the dmg: `xcrun notarytool submit ./dist/pntest.dmg --keychain-profile "PnTest" --wait`

5. Check the full details: `xcrun notarytool log a736f95b-fb72-4cc1-917c-1bc4e2eea740 --keychain-profile "PnTest" apple_dev.json`

**Staple**

The final step, run: `xcrun stapler staple ./dist/pntest.dmg`.

## Notes
Icons come from:
https://icons8.com/icon/set/console/dusk
https://www.flaticon.com/search?word=terminal
