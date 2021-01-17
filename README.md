# PnTest

Frontend GUI application based on python3.6 and PySide2.

### Install

```
cd pntest
virtualenv -p /usr/bin/python3.6 venv
source venv/bin/activate
pip install -r requirements.txt
python src/__main__.py
```
### Build
```
pyinstaller --name="pntest" --windowed ./src/__main__.py --onedir --paths=/home/evan/Code/pntest/src --paths=/home/evan/Code/pntest/venv/lib/python3.6/site-packages/
```

### Pip Dependencies
- orator
- PySide2
- requests
