# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['src/__main__.py'],
             pathex=['/home/evan/Code/pntest/src', '/home/evan/Code/pntest/venv/lib/python3.9/site-packages/', '/home/evan/Code/pntest'],
             binaries=[('include/pntest_proxy', 'include/'), ('include/cert9.db', 'include/'), ('include/rootCA.csr', 'include/'), ('include/rootCA.key', 'include/')],
             datas=[('src/style/dark.qss', 'style/'), ('src/style/dark_theme.qss', 'style/'), ('src/style/light.qss', 'style/')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='pntest',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
