from pxr import Usd, UsdGeom, CameraUtil, UsdShade, Sdf, Gf, Tf
import omni.ext
import omni.ui
from omni.ui import color as cl
from omni.ui import scene as sc
import omni.kit

# Kit104 : Get active viewport window.
active_vp_window = omni.kit.viewport.utility.get_active_viewport_window()
viewport_api = active_vp_window.viewport_api

# Get Viewport window title.
print("Viewport window : " + active_vp_window.name)

# Get camera path ("/OmniverseKit_Persp" etc).
cameraPath = viewport_api.camera_path.pathString
print("cameraPath : " + cameraPath)

# Resolution.
resolution = viewport_api.resolution
print("Resolution : " + str(resolution[0]) + " x " + str(resolution[1]))

# Stage (Usd.Stage).
print(viewport_api.stage)

# Projection matrix (Gf.Matrix4d).
print(viewport_api.projection)

# Transform matrix (Gf.Matrix4d).
print(viewport_api.transform)

# View matrix (Gf.Matrix4d).
print(viewport_api.view)


