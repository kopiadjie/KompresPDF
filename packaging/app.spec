# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['../src/main.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Program Files (x86)\\gs\\gs10.07.0\\bin', 'gs\\bin'), ('C:\\Program Files (x86)\\gs\\gs10.07.0\\lib', 'gs\\lib'), ('C:\\Program Files (x86)\\gs\\gs10.07.0\\Resource', 'gs\\Resource'), ('C:\\Program Files (x86)\\gs\\gs10.07.0\\iccprofiles', 'gs\\iccprofiles'), ('../assets', 'assets')],
    hiddenimports=[],
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
    name='kompres pedeep',
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
    icon=['../assets/app_icon.ico'],
)
