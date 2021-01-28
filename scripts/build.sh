rm -rf build/pntest/
rm -rf dist/pntest/

FILE="include/pntest-core"
if [ ! -f "$FILE" ]; then
    echo "ERROR: $FILE does not exist, you need to build this binary from the pntest-core repo and copy it here.";
    exit 1;
fi

FILE="include/node_sqlite3.node"
if [ ! -f "$FILE" ]; then
    echo "ERROR: $FILE does not exist, you need to build this binary from the pntest-core repo and copy it here.";
    exit 1;
fi

pyinstaller --name="pntest" --windowed ./src/__main__.py --onefile \
  --paths=/home/evan/Code/pntest/src \
  --paths=/home/evan/Code/pntest/venv/lib/python3.6/site-packages/ \
  --add-binary='include/pntest-core:include/' \
  --add-binary='include/node_sqlite3.node:include/' \
  --add-binary='include/cert9.db:include/' \
  --add-binary='include/rootCA.csr:include/' \
  --add-binary='include/rootCA.key:include/' \
  --add-data='src/style/dark.qss:style/' \
  --add-data='src/style/dark_theme.qss:style/' \
  --add-data='src/style/light.qss:style/' \
  --noupx
