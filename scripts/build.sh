rm -rf build/pntest/
rm -rf dist/pntest/

FILE="include/pntest-backend"
if [ ! -f "$FILE" ]; then
    echo "ERROR: $FILE does not exist, you need to build this binary from the pntest-backend repo and copy it here.";
    exit 1;
fi

FILE="include/node_sqlite3.node"
if [ ! -f "$FILE" ]; then
    echo "ERROR: $FILE does not exist, you need to build this binary from the pntest-backend repo and copy it here.";
    exit 1;
fi

pyinstaller --name="pntest" --windowed ./src/__main__.py --onefile \
  --paths=/home/evan/Code/pntest/src \
  --paths=/home/evan/Code/pntest/venv/lib/python3.6/site-packages/ \
  --add-binary='include/pntest-backend:include/' \
  --add-binary='include/node_sqlite3.node:include/' \
  --noupx
