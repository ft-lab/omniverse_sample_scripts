from pxr import Usd, UsdGeom, CameraUtil, UsdShade, Sdf, Gf, Tf
import omni.kit

# Get viewport.
# Kit103 : changed from omni.kit.viewport to omni.kit.viewport_legacy
#viewport = omni.kit.viewport_legacy.get_viewport_interface()
#viewportWindow = viewport.get_viewport_window()

# Kit104 : changed from omni.kit.viewport_legacy to omni.kit.viewport.utility.get_active_viewport_window
import omni.kit.viewport.utility

# Get active viewport window.
active_vp_window = omni.kit.viewport.utility.get_active_viewport_window()
viewport_api = active_vp_window.viewport_api

# Get camera path ("/OmniverseKit_Persp" etc).
cameraPath = viewport_api.camera_path.pathString

print("Active camera path : " + cameraPath)

# Get stage.
stage = omni.usd.get_context().get_stage()

#time_code = omni.timeline.get_timeline_interface().get_current_time() * stage.GetTimeCodesPerSecond()
time_code = Usd.TimeCode.Default()

# Get active camera.
cameraPrim = stage.GetPrimAtPath(cameraPath)
if cameraPrim.IsValid():
    camera  = UsdGeom.Camera(cameraPrim)        # UsdGeom.Camera
    cameraV = camera.GetCamera(time_code)       # Gf.Camera
    print("Aspect : " + str(cameraV.aspectRatio))
    print("fov(H) : " + str(cameraV.GetFieldOfView(Gf.Camera.FOVHorizontal)))
    print("fov(V) : " + str(cameraV.GetFieldOfView(Gf.Camera.FOVVertical)))
    print("FocalLength : " + str(cameraV.focalLength))
    print("World to camera matrix : " + str(cameraV.transform))

    viewMatrix = cameraV.frustum.ComputeViewMatrix()
    print("View matrix : {viewMatrix}")

    viewInv = viewMatrix.GetInverse()

    # Camera position(World).
    cameraPos = viewInv.Transform(Gf.Vec3f(0, 0, 0))
    print(f"Camera position(World) : {cameraPos}")

    # Camera vector(World).
    cameraVector = viewInv.TransformDir(Gf.Vec3f(0, 0, -1))
    print(f"Camera vector(World) : {cameraVector}")

    projectionMatrix = cameraV.frustum.ComputeProjectionMatrix()
    print(f"Projection matrix : {projectionMatrix}")

    #cv = CameraUtil.ScreenWindowParameters(cameraV)
    #print(cv.screenWindow)
