# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


b = Analysis(
    ['src/proxy/__main__.py'],
    pathex=['/Users/evan/Code/pntest/src/proxy', '/Users/evan/Code/pntest/venv/lib/python3.9/site-packages/'],
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
pyz = PYZ(b.pure, b.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
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
coll = COLLECT(
    exe,
    b.binaries,
    b.zipfiles,
    b.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='pntest_proxy',
)
