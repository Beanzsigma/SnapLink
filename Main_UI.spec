# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Main_UI.py'],
    pathex=[],
    binaries=[],
    datas=[('bgminimal.gif', '.'), ('fileimg1.png', '.'), ('icosnap.ico', '.'), ('Syncopate-Regular.ttf', '.'), ('SpaceX.ttf', '.')],
    hiddenimports=['plyer.platforms.win.notification'],
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
    name='Main_UI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icosnap.ico'],
)
