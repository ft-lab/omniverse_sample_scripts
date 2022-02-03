# ft_lab.sample.loadStage

"ft_lab.sample.loadStage" は、あらかじめ用意したusdファイルを開くだけのExtensionです。    

## Extensionの構成

"ft_lab.sample.loadStage" Extensionの構成です。     

```
[ft_lab.sample.loadStage]
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
            [loadStage]
                __init__.py
                main.py
```

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
ft_lab.sample.loadStage
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
title = "Python Extension Example"
description="xxxxxx."

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
name = "ft_lab.sample.loadStage"
```

## ft_lab.sample.loadStage

"ft_lab.sample.loadStage"内は、"ft_lab/sample/loadStage"の階層でフォルダを構成します。     
```
[ft_lab]
    [sample]
        [loadStage]
            __init__.py
            main.py
```

### __init__.py

開始するメインファイル (hello.py)のインポートを指定します.     

```
from .main import *
```

### main.py

```python
from pathlib import Path

# Get USD file.
usdPath = Path(__file__).parent.joinpath("usd")
usdFile = f"{usdPath}/test.usd"

# Load stage.
omni.usd.get_context().open_stage(usdFile)
```

「Path(__file__)」で、main.py自身の絶対パスを返します。     
「parent」でその親のフォルダ、「joinpath("usd")」でusdフォルダ。     
この場合は、usdPathは「ft_lab/sample/loadStage/usd」のパスになります。     
usdFileは「ft_lab/sample/loadStage/usd/test.usd」となります。     
Extension内にusdファイルを入れている構成です。     

「omni.usd.get_context().open_stage(usdFile)」で指定のパスのファイルをステージとして読み込みます。     




