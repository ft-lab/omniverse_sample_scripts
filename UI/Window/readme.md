# Window

## Overview

Create window.    

## [CreateNewWindow.py](./CreateNewWindow.py)    

Create new window.    
![CreateNewWindow.png](./images/CreateNewWindow.png)    

## [ImageWindow.py](./ImageWindow.py)    

View image.     
![ImageWindow.png](./images/ImageWindow.png)    

The image will search for "kit_release/_build/windows-x86_64/release".      
To specify the absolute path in Extension, specify as follows.      

```
from pathlib import Path

IMAGE_PATH = Path(__file__).parent.parent.joinpath("images")

imagePath = f"{IMAGE_PATH}/xxxx.png"

omni.ui.Image(imagePath, width=64, height=64, fill_policy=omni.ui.FillPolicy.PRESERVE_ASPECT_FIT, alignment=omni.ui.Alignment.LEFT_CENTER)

```

## [InputField.py](./InputField.py)    

A sample input field using omni.ui.StringField.     
![InputField.png](./images/InputField.png)    
