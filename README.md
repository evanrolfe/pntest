# PnTest

Frontend GUI application based on python3.6 and PySide2.

### Install for development

```
cd pntest
virtualenv -p /usr/bin/python3.6 venv
source venv/bin/activate
pip install -r requirements.txt
```

### Develop
Run the app:
```
python src/__main__.py
```

Compile Qt assets to python with:
```
./scripts/compile_assets.sh
```

Compile Qt UI files to python with:
```
./scripts/compile_views.sh
```

### Build
```
pyinstaller --name="pntest" --windowed ./src/__main__.py --onedir --paths=/home/evan/Code/pntest/src --paths=/home/evan/Code/pntest/venv/lib/python3.6/site-packages/
```

### Pip Dependencies
- orator
- PySide2
- requests

### Notes
Icons come from:
https://icons8.com/icon/set/console/dusk
https://www.flaticon.com/search?word=terminal
