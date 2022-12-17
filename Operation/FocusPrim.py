# "omni.kit.viewport_legacy" is no longer available in kit104.
#import omni.kit.viewport_legacy
from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf
import omni.kit.commands

# Kit104 : changed from omni.kit.viewport_legacy to omni.kit.viewport.utility.get_active_viewport_window
import omni.kit.viewport.utility

# Get active viewport window.
active_vp_window = omni.kit.viewport.utility.get_active_viewport_window()
viewport_api = active_vp_window.viewport_api

# Get camera path ("/OmniverseKit_Persp" etc).
cameraPath = viewport_api.camera_path.pathString

# Get stage.
stage = omni.usd.get_context().get_stage()

#time_code = omni.timeline.get_timeline_interface().get_current_time() * stage.GetTimeCodesPerSecond()
time_code = Usd.TimeCode()

# Get active camera.
cameraPrim = stage.GetPrimAtPath(cameraPath)
if cameraPrim.IsValid():
    camera  = UsdGeom.Camera(cameraPrim)        # UsdGeom.Camera
    cameraV = camera.GetCamera(time_code)       # Gf.Camera

    # Aspect ratio.
    aspect = cameraV.aspectRatio

    # Taret prim path.
    targetPrimPath = "/World/Sphere"

    prim = stage.GetPrimAtPath(targetPrimPath)
    if prim.IsValid():
        # Set focus.
        omni.kit.commands.execute('FramePrimsCommand',
            prim_to_move=Sdf.Path(cameraPath),
            prims_to_frame=[targetPrimPath],
            time_code=time_code,
            usd_context_name='',
            aspect_ratio=aspect)


