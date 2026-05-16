# -*- mode: python ; coding: utf-8 -*-
import os

font_files = [
    (os.path.join('data', f), 'data')
    for f in [
        'Times New Roman.ttf',
        'Times New Roman Bold.ttf',
        'Times New Roman Bold Italic.ttf',
        'Times New Roman Italic.ttf',
    ]
]

image_files = [
    (os.path.join('data', 'images', f), os.path.join('data', 'images'))
    for f in [
        'High Voice.png',
        'Medium Voice.png',
        'Low Voice.png',
    ]
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=font_files + image_files,
    hiddenimports=['charset_normalizer'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
