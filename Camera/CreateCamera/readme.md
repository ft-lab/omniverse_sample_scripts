# CreateCamera

## Overview

Create camera.    

## [CreateCamera.py](./CreateCamera.py)    

Create and activate the camera.     
To activate the camera for a given path, do the following.     

```
# Camera path.
pathName = '/World/camera1'

# Active camera.
viewport = omni.kit.viewport.get_viewport_interface()
viewport.get_viewport_window().set_active_camera(pathName)
```

## [GetCurrentCamera.py](./GetCurrentCamera.py)    

Get active camera.     
