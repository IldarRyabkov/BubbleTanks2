# -*- mode: python ; coding: utf-8 -*-
import sys
import os


PATH = os.path.dirname(os.path.abspath("__file__"))

block_cipher = None



a = Analysis(['__main__.py'],
	     pathex=[PATH],
             binaries=[],
             datas=[('data\\images', 'images'), ('data\\music', 'music'), ('data\\sounds', 'sounds'), ('data\\fonts', 'fonts')],
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
          name='Underwater Battles',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False)
