# Packaging for debian

1. After building copy: `cp dist/pntest dist/debian/pntest/usr/bin/pntest`

2. `cd dist/debian && dpkg-deb --build pntest`