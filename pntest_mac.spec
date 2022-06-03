# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

#===============================================================================
# pntest (MAC)
#===============================================================================
# On Mac it looks for QtWebEngine resources in ./PySide2/Qt, hence why its included in datas
a = Analysis(
    ['src/__main__.py'],
    pathex=['src'],
    binaries=[],
    datas=[
        ('include/cert9.db', 'include/'),
        ('include/rootCA.key', 'include/'),
        ('include/mitmproxy-ca.pem', 'include/'),
        ('include/html_page.html', 'include/'),
        ('src/style/dark.qss', 'style/'),
        ('src/style/dark_theme.qss', 'style/'),
        ('src/style/light.qss', 'style/'),
        ('venv/lib/python3.9/site-packages/PySide2/Qt/lib/QtWebEngineCore.framework/Resources/', 'PySide2/Qt')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exea = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='pntest',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
#===============================================================================
# pntest_Proxy
#===============================================================================
b = Analysis(
    ['src/proxy/__main__.py'],
    pathex=['src/proxy', 'venv/lib/python3.9/site-packages/'],
    binaries=[('include/cert9.db', 'include/'), ('include/rootCA.key', 'include/')],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyzb = PYZ(b.pure, b.zipped_data, cipher=block_cipher)

exeb = EXE(
    pyzb,
    b.scripts,
    [],
    exclude_binaries=True,
    name='pntest_proxy',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
#===============================================================================
# Collect
#===============================================================================
coll = COLLECT(exea,
               a.binaries,
               a.zipfiles,
               a.datas,
               exeb,
               b.binaries,
               b.zipfiles,
               b.datas,
               name='pntest')

# Mac OS X Bundle
app = BUNDLE(
    coll,
    name='pntest.app',
    icon='p_icon-icons.com_60469.icns',
    bundle_identifier='pntest.pntest',
    info_plist={
        'LSBackgroundOnly': False
    }
)
