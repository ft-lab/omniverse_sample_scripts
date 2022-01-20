# ft_lab.sample.callDLL

"ft_lab.sample.hello" はExtensionからC言語のDLLを呼び出す簡単なサンプルです。    

## Extensionの構成

"ft_lab.sample.callDLL" Extensionの構成です。     

```
[ft_lab.sample.callDLL]
    [bin]
        [win]
            [x64]
                OmniverseSimpleDLL.dll ... dll(Win 64bit).

    [config]
        extension.toml

    [data]
        icon.png      ... Icon file (256 x 256 pixel).
        preview.png

    [docs]
        CHANGELOG.md
        index.rst
        README.md

    [ft_lab]
        [sample]
            [callDLL]
                __init__.py
                callDLL.py

    [build]
        [OmniverseSimpleDLL]  ... DLL source project for VS2017.
```

[build]フォルダは説明のために入れていますが、Extensionの構成としては不要な要素です。    
削除しても問題ありません。      

## data/icon.png

アイコンファイル(256 x 256 pixel)。    
"config/extension.toml"から参照されます。    

## data/preview.png

ExtensionウィンドウのOVERVIEWで表示される画像です。      
"config/extension.toml"から参照されます。    

## docs

ドキュメント。     

|ファイル名|説明|     
|---|---|     
|index.rst|ドキュメントの構造を記載したファイル。|     
|README.md|OVERVIEWに表示される内容。|     
|CHANGELOG.md|CHANGELOGに表示される内容。|     

### index.rst

```
ft_lab.sample.callDLL
###########################

.. toctree::
   :maxdepth: 1

   README
   CHANGELOG
```
## config/extension.toml

"extension.toml"はExtentionの設定を記載します。     

```
[package]
# Version.
version = "0.0.1"

# Authors.
authors = ["ft-lab"]

# The title and description.
title = "Calling function from dll"
description="This is sample of calling function from dll using Python's LoadLibrary."

# Path (relative to the root) or content of readme markdown file for UI.
readme  = "docs/README.md"

# URL of the extension source repository.
repository = ""

# One of categories for UI.
category = "Example"

# Keywords for the extension
keywords = ["kit", "example"]

# ChangeLog.
changelog="docs/CHANGELOG.md"

# Preview image.
preview_image = "data/preview.png"

# Icon image (256x256).
icon = "data/icon.png"

# We only depend on testing framework currently:
[dependencies]

# Main python module this extension provides.
[[python.module]]
name = "ft_lab.sample.callDLL"

# Load native library.
[[native.library]]
path = "bin/win/x64/OmniverseSimpleDLL.dll"
```

[[native.library]]にDLLを参照するための相対パスを指定します（DLLファイル名も含む）。     
上記の場合は、Extension実行時に自動的に"bin/win/x64/"がdllの検索パスとして参照されます。     

## ft_lab.sample.callDLL

"ft_lab.sample.callDLL"内は、"ft_lab/sample/callDLL"の階層でフォルダを構成します。     

```
[ft_lab]
    [sample]
        [callDLL]
            __init__.py
            callDLL.py
```

### __init__.py

開始するメインファイル (callDLL.py)のインポートを指定します.     

```
from .callDLL import *
```

### callDLL.py

Extensionの開始時と終了時に呼び出すメソッドを指定します。     
"dll = cdll.LoadLibrary(r"OmniverseSimpleDLL.dll")"の指定によりDLLが読み込まれます。     

```
import omni.ext

from ctypes import *

# Load library.
# Add the search path for [[native.library]] to "config/extension.toml".
dll = cdll.LoadLibrary(r"OmniverseSimpleDLL.dll")

# ----------------------------------------------------.
# Call external function.
# ----------------------------------------------------.
def callExtFunc():
    if dll == None:
        return

    v = dll.ext_add(3, 8)
    print("dll.ext_add(3, 8) : " + str(v))

    v2 = dll.ext_sub(3, 8)
    print("dll.ext_sub(3, 8) : " + str(v2))

# ----------------------------------------------------.
class CallDLLExtension(omni.ext.IExt):
    def on_startup(self, ext_id):
        print("[ft_lab.sample.callDLL] HelloExtension startup")
        callExtFunc()

    def on_shutdown(self):
        print("[ft_lab.sample.callDLL] HelloExtension shutdown")
```

"ext_add"、"ext_sub"がDLLに定義されている外部関数になります。     

## Omniverse CreateにExtensionを入れる

Omniverse Createが"pkg/create-2021.3.8"にインストールされているとします。     
このとき、開発者が作成したExtensionを"pkg/create-2021.3.8/exts"に入れます。     

作成した"ft_lab.sample.callDLL"をフォルダごと"pkg/create-2021.3.8/exts"に格納します。      
Omniverse Createを起動したままでもExtensionを所定のフォルダに入れると、自動的にExtensionが認識されます。     

メインメニューの"Window"-"Extensions" を選択し、Extensionsウィンドウを表示します。     

Extensionのリストで"Calling function from dll"が存在するのを確認できました。     

![extension_cap_02.jpg](../images/extension_cap_02.jpg)    



