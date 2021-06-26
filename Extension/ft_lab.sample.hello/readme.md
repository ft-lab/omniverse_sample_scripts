# ft_lab.sample.hello

"ft_lab.sample.hello" is a simple sample to learn the structure of Extension.    
The original is "omni.example.hello".    

## Extension Structure

"ft_lab.sample.hello" Extension.     

```
[ft_lab.sample.hello]
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
            [hello]
                __init__.py
                hello.py
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
ft_lab.sample.hello
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
"omni.kit.test" = {}

# Main python module this extension provides.
[[python.module]]
name = "ft_lab.sample.hello"
```

## ft_lab.sample.hello

For "ft_lab.sample.hello", create a folder for "ft_lab/sample/hello".     
```
[ft_lab]
    [sample]
        [hello]
            __init__.py
            hello.py
```

### __init__.py

Import the Main file (hello.py).     

```
from .hello import *
```

### hello.py

Specify the method to call when the Extension starts and ends.     
```
import omni.ext

class HelloExtension(omni.ext.IExt):
    # Call startup.
    def on_startup(self, ext_id):
        print("[ft_lab.sample.hello] HelloExtension startup")

    # Call shutdown.
    def on_shutdown(self):
        print("[ft_lab.sample.hello] HelloExtension shutdown")
```

## Install the Extension in Omniverse Create

Let's say you have Omniverse Create installed on "pkg/create-2021.1.1".     
Extension is stored in "pkg/create-2021.1.1/_build/kit_release/_exts".    

Copy the "ft_lab.sample.hello" that you created here.     
You can do this while Omniverse Create is running.     

Select "Window"-"Extensions" from the main menu.     

You can find the Extension you created by searching for "sample".     
![extension_cap_01.jpg](../images/extension_cap_01.jpg)    



