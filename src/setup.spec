# -*- mode: python ; coding: utf-8 -*-
import sys
import os


PATH = os.path.dirname(os.path.abspath("__file__"))

block_cipher = None


added_files = [
	(os.path.join('data', 'images'), 'images'),
	(os.path.join('data', 'music'),  'music'),
	(os.path.join('data', 'sounds'), 'sounds'), 
	(os.path.join('data', 'fonts'),  'fonts'),
	(os.path.join('languages'),      'languages')
]



a = Analysis(['__main__.py'],
	     pathex=[PATH],
             binaries=[],
             datas=added_files,
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
          console=True)
