# -*- mode: python ; coding: utf-8 -*-
import sys
import os


PATH = os.path.dirname(os.path.abspath("__file__"))

block_cipher = None


added_files = [
	('assets/images', 'assets/images' ),
	('assets/sounds', 'assets/sounds' ),
	('assets/music', 'assets/music' ),
	('assets/fonts', 'assets/fonts' ),
	('data/languages', 'data/languages' ),
	('data/guns', 'data/guns' ),
	('data/player_tanks', 'data/player_tanks' ),
	('data/bubbles', 'data/bubbles' ),
	('data/bullets', 'data/bullets' ),
	('data/enemies', 'data/enemies' ),
	('data/shapes', 'data/shapes' ),
	('data/superpowers/disassemble', 'data/superpowers/disassemble' ),
	('data/superpowers/seekers', 'data/superpowers/seekers' ),

]



a = Analysis(['__main__.py'],
	         pathex=[PATH],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['numpy', 'pandas', 'scipy'],
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
          name='Bubble Tanks 2',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False)
