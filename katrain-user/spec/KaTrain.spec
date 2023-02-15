# -*- mode: python ; coding: utf-8 -*-
from kivy_deps import sdl2, glew
from kivymd import hooks_path as kivymd_hooks_path
import subprocess
import sys

block_cipher = None

#pyinstaller是python的一个第三方模块，使用它可以将python程序打包为可执行文件，
#实现打包后的程序在没有python环境的机器上也可以运行。
# pyinstaller spec/KaTrain.spec --noconfirm
# --upx-dir my

a = Analysis(
    ["..\\katrain\\__main__.py"],# 此列表存放项目设计的所有python脚本文件
    pathex=["C:\\Users\\sande\\Desktop\\katrain\\spec"],# 此列表为项目绝对路径
    binaries=[],
    # 此列表存放所有资源文件，每个文件是一个2元组元素
    datas=[
        ("..\\katrain\\gui.kv", "katrain"),
        ("..\\katrain\\popups.kv", "katrain"),
        ("..\\katrain\\config.json", "katrain"),
        ("..\\katrain\\KataGo", "katrain\\KataGo"),
        ("..\\katrain\\models", "katrain\\models"),
        ("..\\katrain\\sounds", "katrain\\sounds"),
        ("..\\katrain\img", "katrain\\img"),
        ("..\\katrain\\fonts", "katrain\\fonts"),
        ("..\\katrain\\i18n", "katrain\\i18n"),
    ],
    hiddenimports=["win32file", "win32timezone", "six"],  #  FileChooser in kivy loads win32file conditionally, mkl needs six
    hookspath=[kivymd_hooks_path],
    excludes=["scipy", "pandas", "numpy", "matplotlib", "docutils", "mkl"],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

print("SCRIPTS", len(a.scripts), "BIN", len(a.binaries), "ZIP", len(a.zipfiles), "DATA", len(a.datas))

EXCLUDE_SUFFIX = ["katago"]
EXCLUDE = ["KataGoData", "anim_", "screenshot_", "__pycache__"]
a.datas = [
    (ff, ft, tp)
    for ff, ft, tp in a.datas
    if not any(ff.endswith(suffix) for suffix in EXCLUDE_SUFFIX) and not any(kw in ff for kw in EXCLUDE)
]

print("DATA FILTERED", len(a.datas))

console_names = {True:"DebugKaTrain",False:"KaTrain"}

powershell = subprocess.Popen(["powershell"],  stdout=subprocess.PIPE, stdin=subprocess.PIPE)

# load and run script to buid VSVersionInfo object
sys.path.append(SPECPATH)
import file_version as versionModule


for console, name in console_names.items():


    pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
    exe = EXE(
        pyz,
        a.scripts,
        [],
        exclude_binaries=True,
        name=name,# 打包程序的名字
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        console=console,
        # 此处console=True表示，打包后的可执行文件双击运行时屏幕会出现一个cmd窗口，不影响原程序运行
        # 如果想要修改程序图标，使用在EXE()中加入 icon='xxxxx', 切记：绝对路径
        icon="..\\katrain\img\\icon.ico",
        version=versionModule.versionInfo,
    )

    coll = COLLECT(
        exe,
        a.binaries,
        a.zipfiles,
        a.datas,
        *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
        strip=False,
        upx=True,
        upx_exclude=[],
        name=name,
    )

    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
        debug=False,
        strip=False,
        upx=True,
        name=name,
        console=console,
        icon="..\\katrain\img\\icon.ico",
        version=versionModule.versionInfo,
    )
    powershell.stdin.write(f"Set-AuthenticodeSignature dist/{name}.exe -Certificate (Get-ChildItem Cert:\CurrentUser\My -CodeSigningCert)\n".encode('ascii'))
    powershell.stdin.write(f"Set-AuthenticodeSignature dist/{name}/{name}.exe -Certificate (Get-ChildItem Cert:\CurrentUser\My -CodeSigningCert)\n".encode('ascii'))
    powershell.stdin.flush()

#while True:
#    print(powershell.stdout.readline())