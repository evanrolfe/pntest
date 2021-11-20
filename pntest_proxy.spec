# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['src/proxy/__main__.py'],
             pathex=['/home/evan/Code/pntest/src/proxy', '/home/evan/Code/pntest/venv/lib/python3.9/site-packages/', '/home/evan/Code/pntest'],
             binaries=[('include/cert9.db', 'include/'), ('include/rootCA.key', 'include/')],
             datas=[],
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
          name='pntest_proxy',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
