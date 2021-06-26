# ft_lab.sample.callDLL

This is sample of calling function from dll using Python's LoadLibrary.     

## Extension Structure

"ft_lab.sample.callDLL" Extension.     

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

## data/icon.png

Icon file(256 x 256 pixel).    
It is referenced by "config/extension.toml".    

## data/preview.png

Image displayed in OVERVIEW in the Extension window.     
It is referenced by "config/extension.toml".    

## docs

Documents.     

|File name|Description|     
|---|---|     
|index.rst|A file describing the structure of the document.|     
|README.md|Description displayed in the OVERVIEW.|     
|CHANGELOG.md|Description displayed in CHANGELOG.|     

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

"extension.toml" is a configuration file.     

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
"omni.kit.test" = {}

# Main python module this extension provides.
[[python.module]]
name = "ft_lab.sample.callDLL"

# Load native library.
[[native.library]]
path = "bin/win/x64/OmniverseSimpleDLL.dll"
```

Set the path of the dll to be referenced in [[native.library]].     


## ft_lab.sample.callDLL

For "ft_lab.sample.callDLL", create a folder for "ft_lab/sample/callDLL".     
```
[ft_lab]
    [sample]
        [callDLL]
            __init__.py
            callDLL.py
```

### __init__.py

Import the Main file (callDLL.py).     

```
from .callDLL import *
```

### callDLL.py

Specify the method to call when the Extension starts and ends.     
Load the dll with "dll = cdll.LoadLibrary(r"OmniverseSimpleDLL.dll")".     


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

## Install the Extension in Omniverse Create

Let's say you have Omniverse Create installed on "pkg/create-2021.1.1".     
Extension is stored in "pkg/create-2021.1.1/_build/kit_release/_exts".    

Copy the "ft_lab.sample.callDLL" that you created here.     
You can do this while Omniverse Create is running.     

Select "Window"-"Extensions" from the main menu.     

You can find the Extension you created by searching for "sample".     
![extension_cap_02.jpg](../images/extension_cap_02.jpg)    



